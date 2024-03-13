import zmq
import json
import threading


ZMQ_PUB = "tcp://192.168.137.10:5556"
ZMQ_SUB = "tcp://192.168.137.10:5555"

class Localization:
    def __init__(self, context) -> None:
        # State variables
        self.x = 0
        self.y = 0
        self.heading = 0

        # Interprocess communication objects
        camera_sub: zmq.Socket = context.socket(zmq.SUB)
        camera_sub.setsockopt(zmq.CONFLATE, 1)
        camera_sub.connect(ZMQ_SUB)
        camera_sub.setsockopt(zmq.SUBSCRIBE, b"qr")

        imu_sub: zmq.Socket = context.socket(zmq.SUB)
        imu_sub.setsockopt(zmq.CONFLATE, 1)
        imu_sub.connect(ZMQ_SUB)
        imu_sub.setsockopt(zmq.SUBSCRIBE, b"imu")

        pose_pub: zmq.Socket = context.socket(zmq.PUB)
        pose_pub.connect(ZMQ_PUB)

    def update_pose():
        ...

if __name__ == "__main__":
    zmq_context = zmq.Context()
    localizer = Localization(zmq_context)

    while True:
        localizer.update_pose()
