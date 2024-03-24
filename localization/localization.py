import zmq
import json
import time
import math


ZMQ_PUB = "tcp://172.20.10.4:5556"
ZMQ_SUB = "tcp://172.20.10.4:5555"
UPDATE_RATE = 3  # Hz

class Localization:
    X_OFFSET = 1
    Y_OFFSET = 1
    def __init__(self, context) -> None:
        # State variables
        self.x = 0
        self.y = 0

        self.heading = 0
        self.heading_bias = 0

        self.vel_x = 0
        self.vel_y = 0

        ACCEL_AVG_WINDOW = 5
        self.accel_x = [0] * ACCEL_AVG_WINDOW
        self.accel_y = [0] * ACCEL_AVG_WINDOW
        self.accel_window_index = 0

        self.accel_x_bias = 0
        self.accel_y_bias = 0

        # Interprocess communication objects
        self.camera_sub: zmq.Socket = context.socket(zmq.SUB)
        self.camera_sub.setsockopt(zmq.CONFLATE, 1)
        self.camera_sub.connect(ZMQ_SUB)
        self.camera_sub.setsockopt(zmq.SUBSCRIBE, b"qr")

        self.imu_sub: zmq.Socket = context.socket(zmq.SUB)
        self.imu_sub.setsockopt(zmq.CONFLATE, 1)
        self.imu_sub.connect(ZMQ_SUB)
        self.imu_sub.setsockopt(zmq.SUBSCRIBE, b"imu")

        self.pose_pub: zmq.Socket = context.socket(zmq.PUB)
        self.pose_pub.connect(ZMQ_PUB)

        # Misc.
        self.prev_publish_time = time.time()
        self.prev_imu_update_time = time.time()

        self.calibrate_imu()

    def calibrate_imu(self):
        print("Waiting for sensor data...")
        time.sleep(5)
        print("Calibrating IMU ...")
        # determine bias in accelerometer and angle
        CALIBRATION_DURATION = 3
        X_EPSILON = 0.1
        Y_EPSILON = 0.1
        HEAD_EPSILON = 1

        prev_time = time.time()
        x_error = 0
        y_error = 0
        head_error = 0

        i = 0
        while True:
            i += 1
            topic, imu_msg = self.imu_sub.recv_string().split(' ', 1)
            imu_msg = json.loads(imu_msg)

            accel_x = imu_msg["accel_x"]
            accel_y = imu_msg["accel_y"]            

            heading = self.calculate_imu_heading(imu_msg["quat_real"], imu_msg["quat_i"], imu_msg["quat_j"], imu_msg["quat_k"])
            
            self.accel_x_bias = (self.accel_x_bias*(i-1) + accel_x) / i
            self.accel_y_bias = (self.accel_y_bias*(i-1) + accel_y) / i
            self.heading_bias = (self.heading_bias*(i-1) + heading) / i

            x_error = (x_error*(i-1) + (accel_x - self.accel_x_bias)) / i
            y_error = (y_error*(i-1) + (accel_y - self.accel_y_bias)) / i
            head_error = (head_error*(i-1) + (heading - self.heading_bias)) / i

            # error must be close enough to zero mean for long enough to complete calibration
            if (abs(x_error) < X_EPSILON and
                abs(y_error) < Y_EPSILON and
                abs(head_error) < HEAD_EPSILON):
                if (time.time() - prev_time) > CALIBRATION_DURATION:
                    print("IMU calibrated successfully")
                    return 
                continue

            prev_time = time.time() 

    def calculate_imu_heading(self, dqw, dqx, dqy, dqz):
        # https://github.com/adafruit/Adafruit_CircuitPython_BNO08x/blob/main/examples/bno08x_find_heading.py
        norm = math.sqrt(dqw * dqw + dqx * dqx + dqy * dqy + dqz * dqz)
        dqw = dqw / norm
        dqx = dqx / norm
        dqy = dqy / norm
        dqz = dqz / norm

        ysqr = dqy * dqy

        t3 = +2.0 * (dqw * dqz + dqx * dqy)
        t4 = +1.0 - 2.0 * (ysqr + dqz * dqz)
        yaw_raw = math.atan2(t3, t4)
        yaw = yaw_raw * 180.0 / math.pi

        return -yaw  # 0 -> 180 CCW, 0 -> -180 CW

    def update_pose(self):
        # Check for camera updates
        camera_heading = None
        try:
            topic, camera_msg = self.camera_sub.recv_string(flags=zmq.NOBLOCK).split(' ', 1)
            camera_msg = json.loads(camera_msg)

            if (camera_msg["pos_x"] is not None) and (camera_msg["pos_y"] is not None) and (camera_msg["angle"] is not None):
                self.x = camera_msg["pos_x"]
                self.y = camera_msg["pos_y"]
                camera_heading = camera_msg["angle"]

        except zmq.Again as e:
            pass
        
        # Check for IMU updates
        try:
            topic, imu_msg = self.imu_sub.recv_string(flags=zmq.NOBLOCK).split(' ', 1)
            imu_msg = json.loads(imu_msg)

            accel_x = imu_msg["accel_x"] - self.accel_x_bias
            accel_y = imu_msg["accel_y"] - self.accel_y_bias
            print(f"Accel_x: {accel_x}, Accel_y: {accel_y}")

            # heading calculation
            if (accel_x is not None and accel_y is not None):
                self.heading = self.calculate_imu_heading(imu_msg["quat_real"], imu_msg["quat_i"], imu_msg["quat_j"], imu_msg["quat_k"])
                if camera_heading is not None:
                    # update the heading correction factor
                    self.heading_bias = self.heading - camera_heading
                
                self.heading -= self.heading_bias  # fix to camera value (global absolute)

                # Maintain heading within specified range
                if self.heading > 180:
                    self.heading -= 360
                elif self.heading < -180:
                    self.heading += 360

                # dead reckoning
                t = time.time()
                dt = t - self.prev_imu_update_time
                self.prev_imu_update_time = t
                
                self.x += ((0.5*accel_x*dt*dt) + (self.vel_x*dt))
                self.y += ((0.5*accel_y*dt*dt) + (self.vel_y*dt))
                print(f"dx: {(0.5*accel_x*dt*dt) + (self.vel_x*dt)} dy: {(0.5*accel_y*dt*dt) + (self.vel_y*dt)}")

                self.vel_x += (accel_x*dt)
                self.vel_y += (accel_y*dt)
                print(f"Vel_x: {self.vel_x}, Vel_y: {self.vel_y}")

        except zmq.Again as e:
            pass

        # Publish new localization data
        if (time.time() - self.prev_publish_time) > (1/UPDATE_RATE):
            heading = 360+self.heading if self.heading < 0 else self.heading  # Convert heading to 0 -> 359 range
            # Since imu has a coordinate system of y pointing up and navigation has y pointing down, we need to negate y
            self.pose_pub.send_string(f"localization {self.x + Localization.X_OFFSET},{-self.y + Localization.Y_OFFSET},{heading}")
            self.prev_publish_time = time.time()
        
        self.prev_imu_update_time = time.time()


if __name__ == "__main__":
    zmq_context = zmq.Context()
    localizer = Localization(zmq_context)
    while True:
        localizer.update_pose()
        time.sleep(1 / 1000)
