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
    K = 2

    while True:
        output_pwm = 0
        topic, adc_msg = adc_sub.recv_string().split(' ', 1)
        topic, push_msg = push_sub.recv_string().split(' ', 1)

        right_button, left_button = push_msg.split(',', 1)
        right_button = 0 if (int(right_button) == 1) else 1
        left_button = 0 if (int(left_button) == 1) else 1

        try :
            adc_msg: dict = json.loads(adc_msg)
        except ValueError:
            pass

        serial_msg = "0000000"
        if push_msg != '0,0':
            #  Calculate PWM for each motor and send to ARDUINO
            chan0, chan1, chan2, chan3 = float(adc_msg["channel0"]), float(adc_msg["channel1"]), float(adc_msg["channel2"]), float(adc_msg["channel3"])

            left_dir = 1 if abs(chan2) < THRESHOLD else -1
            right_dir = 1 if abs(chan3) < THRESHOLD else -1

            left = left_button*left_dir
            right = right_button*right_dir

            directions = 0
            if left < 0 and right > 0:
                directions = 1
            elif left > 0 and right < 0:
                directions = 2
            elif left < 0 and right < 0:
                directions = 3

            left_pwm = int(min(PWM_MAX, abs(K*PWM_MAX*left)))  # Get PWM, clip at PWM_MAX
            right_pwm = int(min(PWM_MAX, abs(K*PWM_MAX*right)))  # Get PWM, clip at PWM_MAX

            match directions:
                case 0:
                    print(f"Pushing - Left: {left_pwm}, Right: {right_pwm}")
                case 1:
                    print(f"Pushing - Left: {left_pwm}, Right: -{right_pwm}")
                case 2:
                    print(f"Pushing - Left: -{left_pwm}, Right: {right_pwm}")
                case 3:
                    print(f"Pushing - Left: -{left_pwm}, Right: -{right_pwm}")

            serial_msg = f"{left_pwm:03}{right_pwm:03}{directions}" # msd lllrrrd lsd (e.g. 1801802)

        print(serial_msg)
        # uart.write(f'{serial_msg}\n'.encode())


if __name__ == '__main__':
    print("Starting serial to arduino process...")
    zmq_ctx = zmq.Context()
    zmq_to_serial(zmq_ctx, "/dev/ttyS0")