import time
import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

def main():
    i2c = busio.I2C(board.SCL, board.SDA)
    adc = ADS.ADS1115(i2c)

    chan0 = AnalogIn(adc, ADS.P0)
    chan1 = AnalogIn(adc, ADS.P1)
    chan2 = AnalogIn(adc, ADS.P2)
    chan3 = AnalogIn(adc, ADS.P2)
    

    while True:
        print(f"chan0 voltage: {chan0.voltage}, chan1 voltage: {chan1.voltage}, chan2 voltage: {chan2.voltage}, chan3 voltage: {chan3.voltage}")
        time.sleep(0.1)

if __name__ == "__main__":
    main()
