import board
import busio
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER
import time
from statistics import mean

i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)

# Kinematic Variables
cart_x = 0
cart_y = 0
cart_accel_x = [0]*20  # avg for noise
cart_accel_y = [0]*20  # avg for noise
cart_vel_x = 0
cart_vel_y = 0

# Helper Variables
i = 0
previous_time = time.time_ns()


# Main Integration Loop
while True:
    time.sleep(0.1)
    accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
    delta_time = time.time_ns() - previous_time

    print("Accel_X: %0.6f  Accel_Y: %0.6f Accel_Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))

    cart_accel_x[i] = accel_x
    cart_accel_y[i] = accel_y

    accel_x = mean(cart_accel_x)
    accel_y = mean(cart_accel_y)

    cart_vel_x += ((accel_x * delta_time) / 1e9)
    cart_vel_y += ((accel_y * delta_time) / 1e9)

    print("Vel_X: %0.6f  Vel_Y: %0.6f m/s" % (cart_vel_x, cart_vel_y))

    cart_x += ((cart_vel_x * delta_time) / 1e9)
    cart_y += ((cart_vel_y * delta_time) / 1e9)

    print("X: %0.6f  Y: %0.6f m" % (cart_x, cart_y))

    i = (i + 1) % len(cart_accel_x)
    

