import time
import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

def main():
    i2c = busio.I2C(board.SCL, board.SDA)
    adc = ADS.ADS1115(i2c)

    chan = AnalogIn(adc, ADS.P0)

    while True:
        print(f"voltage: {chan.voltage}, value: {chan.value}")
        time.sleep(0.1)

if __name__ == "__main__":
    main()
