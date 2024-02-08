import zmq
import gpiozero
import board
import busio
import threading
from time import sleep

ZMQ_PUB = "tcp://127.0.0.1:5556"

def adc(zmq: zmq.Context, i2c: busio.I2C):
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
    adc = ADS.ADS1115(i2c)

    chan0 = AnalogIn(adc, ADS.P0)
    chan1 = AnalogIn(adc, ADS.P1)
    chan2 = AnalogIn(adc, ADS.P2)
    chan3 = AnalogIn(adc, ADS.P2)
    

    while True:
        print(f"[ADC] chan0 voltage: {chan0.voltage}, chan1 voltage: {chan1.voltage}, chan2 voltage: {chan2.voltage}, chan3 voltage: {chan3.voltage}")
        sleep(0.1)
    # pub = setup_zmq_pub(zmq)

def rfid(zmq: zmq.Context, i2c: busio.I2C):
    from adafruit_pn532.i2c import PN532_I2C
    
    pn532 = PN532_I2C(i2c, debug=False)
    pn532.SAM_configuration()
    pn532.listen_for_passive_target(timeout=0.1)
    # Check if a card is available to read
    while True:
        uid = pn532.get_passive_target()
        if uid is not None:
            print("[RFID] Found card with UID:", [hex(i) for i in uid])
        else:
            print("[RFID] No RFID")
        sleep(0.1)
        pn532.listen_for_passive_target(timeout=0.1)

    # pub = setup_zmq_pub(zmq)

def pushbutton(zmq: zmq.Context):
    pin = gpiozero.InputDevice(17, pull_up=True)
    # pub = setup_zmq_pub(zmq)

    while True:
        print(f'[BUTTON] {pin.value}')
        sleep(0.1)


def imu(zmq: zmq.Context, i2c: busio.I2C):
    from adafruit_bno08x import BNO_REPORT_ACCELEROMETER
    from adafruit_bno08x.i2c import BNO08X_I2C
    # pub = setup_zmq_pub(zmq)
    bno = BNO08X_I2C(i2c)
    bno.enable_feature(BNO_REPORT_ACCELEROMETER)

    while True:
        accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
        print("[IMU] X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))
        sleep(0.1)

def setup_zmq_pub(context: zmq.Context):
    pub = context.socket(zmq.PUB)
    pub.connect(ZMQ_PUB)
    return pub


def main():
    ctx = zmq.Context()
    i2c = busio.I2C(board.SCL, board.SDA)

    adc_thread = threading.Thread(target=adc, args=(ctx, i2c))
    rfid_thread = threading.Thread(target=rfid, args=(ctx, i2c))
    pushbutton_thread = threading.Thread(target=pushbutton, args=(ctx,))
    imu_thread = threading.Thread(target=imu, args=(ctx, i2c))

    adc_thread.start()
    rfid_thread.start()
    pushbutton_thread.start()
    imu_thread.start()



if __name__ == '__main__':
    main()