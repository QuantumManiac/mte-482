import serial
import zmq
import json
from time import sleep
import math

def zmq_to_serial(context: zmq.Context, uart_port: str):
    adc_sub: zmq.Socket = context.socket(zmq.SUB)
    adc_sub.setsockopt(zmq.CONFLATE, 1)
    adc_sub.connect("tcp://172.20.10.4:5555")
    adc_sub.setsockopt(zmq.SUBSCRIBE, b"adc")

    push_sub: zmq.Socket = context.socket(zmq.SUB)
    push_sub.setsockopt(zmq.CONFLATE, 1)
    push_sub.connect("tcp://172.20.10.4:5555")
    push_sub.setsockopt(zmq.SUBSCRIBE, b"push_assist")

    uart = serial.Serial(uart_port, 115200)
    uart.flush()
    num = 0

    THRESHOLD = 0.5  # Volts
    MAX_VOLTAGE = 5  # Volts
    PWM_LIMIT = 0.81  # 0.81 is motor driver PWM limit
    PWM_MAX = math.floor(255 * PWM_LIMIT)  
    K = 1

    while True:
        output_pwm = 0
        topic, adc_msg = adc_sub.recv_string().split(' ', 1)
        topic, push_msg = push_sub.recv_string().split(' ', 1)
        # print("sending")

        try :
            adc_msg: dict = json.loads(adc_msg)
        except ValueError:
            pass
        
        if push_msg != 0:
            #  Calculate PWM for each motor and send to ARDUINO
            left = adc_msg["channel0"] - adc_msg["channel1"]
            right = adc_msg["channel2"] - adc_msg["channel3"]

            left = 0 if abs(left) < THRESHOLD else left
            right = 0 if abs(right) < THRESHOLD else right

            directions = 0
            if left > 0 and right < 0:
                directions = 1
            elif left < 0 and right > 0:
                directions = 2
            elif left < 0 and right < 0:
                directions - 3

            left_pwm = min(PWM_MAX, (abs(left) * K / MAX_VOLTAGE) * PWM_MAX)  # Get PWM, clip at PWM_MAX
            right_pwm = min(PWM_MAX, (abs(right) * K / MAX_VOLTAGE) * PWM_MAX)  # Get PWM, clip at PWM_MAX

            print(f"Pushing - Left: {left_pwm}, Right: {right_pwm}")

            serial_msg = directions + 10*right_pwm + left_pwm*10000  # msd lllrrrd lsd (e.g. 1801802)

        uart.write(f'{serial_msg}\n'.encode())
        # uart.write(json.dumps(msg).encode('utf-8') + b'\n')
        # uart.write(f'{num}\n'.encode())
        # print(num)
        # num = (num + 1) % 3
        # sleep(2)

if __name__ == '__main__':
    print("Starting serial to arduino process...")
    zmq_ctx = zmq.Context()
    zmq_to_serial(zmq_ctx, "/dev/ttyS0")