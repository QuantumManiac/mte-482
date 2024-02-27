import serial
import zmq
import json
from time import sleep

def zmq_to_serial(context: zmq.Context, uart_port: str):
    sub: zmq.Socket = context.socket(zmq.SUB)
    sub.setsockopt(zmq.CONFLATE, 1)
    sub.connect("tcp://192.168.0.114:5555")
    sub.setsockopt(zmq.SUBSCRIBE, b"adc")

    uart = serial.Serial(uart_port, 9600)
    while True:
        topic, msg = sub.recv_string().split(' ', 1)
        print("sending")

        try :
            msg: dict = json.loads(msg)
        except ValueError:
            pass
        uart.write(json.dumps(msg).encode('utf-8') + b'\n')
        # uart.write(1)
        # sleep(1)

if __name__ == '__main__':
    zmq_ctx = zmq.Context()
    zmq_to_serial(zmq_ctx, "/dev/ttyS0")
