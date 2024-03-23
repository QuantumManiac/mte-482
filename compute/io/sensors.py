import zmq
import gpiozero
import json
import busio
import threading
from time import sleep
from adafruit_extended_bus import ExtendedI2C as I2C

ZMQ_PUB = "tcp://172.20.10.4:5556"

def adc(zmq: zmq.Context, i2c: busio.I2C):
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
    adc = ADS.ADS1115(i2c)
    chan0 = AnalogIn(adc, ADS.P0)
    chan1 = AnalogIn(adc, ADS.P1)
    chan2 = AnalogIn(adc, ADS.P2)
    chan3 = AnalogIn(adc, ADS.P3)
    pub = setup_zmq_pub(zmq)
    
    while True:
        # print(f"[ADC] chan0 voltage: {chan0.voltage}, chan1 voltage: {chan1.voltage}, chan2 voltage: {chan2.voltage}, chan3 voltage: {chan3.voltage}")
        send_zmq_json(pub, "adc", {
            "channel0": chan0.voltage,
            "channel1": chan1.voltage,
            "channel2": chan2.voltage,
            "channel3": chan3.voltage
        })
        sleep(0.1)

def rfid(zmq: zmq.Context, i2c: busio.I2C):
    from adafruit_pn532.i2c import PN532_I2C
    
    pn532 = PN532_I2C(i2c, debug=False)
    pn532.SAM_configuration()
    pn532.listen_for_passive_target(timeout=0.1)
    pub = setup_zmq_pub(zmq)
    # Check if a card is available to read
    while True:
        uid = pn532.get_passive_target()
        if uid is not None:
            # print("[RFID] Found card with UID:", "-".join(f"{i:x}" for i in uid))
            send_zmq_msg(pub, "rfid", "-".join(f"{i:x}" for i in uid))
        else:
            send_zmq_msg(pub, "rfid", "00-00-00-00")
        sleep(0.1)
        pn532.listen_for_passive_target(timeout=0.1)

def pushbutton(zmq: zmq.Context):
    pin = gpiozero.InputDevice(18, pull_up=True)
    pub = setup_zmq_pub(zmq)

    while True:
        # print(f'[BUTTON] {pin.value}')
        send_zmq_msg(pub, "push_assist", str(pin.value))
        sleep(0.1)


def imu(zmq: zmq.Context, i2c: busio.I2C):
    from adafruit_bno08x import BNO_REPORT_ACCELEROMETER, BNO_REPORT_ROTATION_VECTOR
    from adafruit_bno08x.i2c import BNO08X_I2C
    pub = setup_zmq_pub(zmq)
    bno = BNO08X_I2C(i2c)
    bno.enable_feature(BNO_REPORT_ACCELEROMETER)
    bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)

    while True:
        accel_x, accel_y, accel_z = bno.acceleration
        quat_i, quat_j, quat_k, quat_real = bno.quaternion
        # print("[IMU] X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))
        send_zmq_json(pub, "imu", {
            "accel_x": accel_x,
            "accel_y": accel_y,
            "accel_z": accel_z,
            "quat_i": quat_i,
            "quat_j": quat_j,
            "quat_k": quat_k,
            "quat_real": quat_real
        })
        # TODO: check if sampling rate is good
        sleep(0.1)

def voltage(zmq: zmq.Context):
    VOLTAGE_MULTIPLIER = 0.95
    from ina226 import INA226
    ina = INA226(busnum=3)
    ina.configure(bus_ct=INA226.VCT_1100us_BIT)
    pub = setup_zmq_pub(zmq)
    while True:
        if ina.is_conversion_ready():
            voltage = ina.voltage()
            # print("[VOLTAGE] Bus Voltage: %0.6f" % (voltage * VOLTAGE_MULTIPLIER))
            send_zmq_msg(pub, "battery_voltage", str(voltage * VOLTAGE_MULTIPLIER))
        sleep(0.1)
    

def setup_zmq_pub(context: zmq.Context) -> zmq.Socket:
    pub = context.socket(zmq.PUB)
    pub.connect(ZMQ_PUB)
    return pub

def send_zmq_msg(pub: zmq.Socket, topic: str, msg: str):
    pub.send_string(f"{topic} {msg}")

def send_zmq_json(pub: zmq.Socket, topic: str, msg: dict):
    serialized = json.dumps(msg)
    pub.send_string(f"{topic} {serialized}")

def main():
    print("Starting sensor processes...")
    ctx = zmq.Context()
    i2c = I2C(3)

    adc_thread = threading.Thread(target=adc, args=(ctx, i2c))
    rfid_thread = threading.Thread(target=rfid, args=(ctx, i2c))
    pushbutton_thread = threading.Thread(target=pushbutton, args=(ctx,))
    imu_thread = threading.Thread(target=imu, args=(ctx, i2c))
    voltage_thread = threading.Thread(target=voltage, args=(ctx,))

    adc_thread.start()
    rfid_thread.start()
    pushbutton_thread.start()
    imu_thread.start()
    voltage_thread.start()



if __name__ == '__main__':
    main()
