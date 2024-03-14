# Power states are based on voltage of battery:
# Normal: > 13.5V - Normal operation
# Low: 12.8V - 13.5V - Display warning message
# Critical: < 12.8V - Execute shutdown command
from time import sleep
import os
import zmq

ZMQ_PUB = "tcp://172.20.10.4:5556"
ZMQ_SUB = "tcp://172.20.10.4:5555"
TICK_RATE = 3  # Hz

def handle_critical():
    print("Critical state! Shutting down...")
    # shutdown command
    os.system("shutdown now")

def handle_low(zmq_pub: zmq.Socket):
    print("Battery voltage low! Displaying warning message...")
    zmq_pub.send_string("power low")

def main():
    print("Starting power management process...")
    context = zmq.Context()
    voltage_sub: zmq.Socket = context.socket(zmq.SUB)
    voltage_sub.setsockopt(zmq.CONFLATE, 1)
    voltage_sub.connect(ZMQ_SUB)
    voltage_sub.setsockopt(zmq.SUBSCRIBE, b"battery_voltage")

    shutdown_sub: zmq.Socket = context.socket(zmq.SUB)
    shutdown_sub.setsockopt(zmq.CONFLATE, 1)
    shutdown_sub.connect(ZMQ_SUB)
    shutdown_sub.setsockopt(zmq.SUBSCRIBE, b"ui_shutdown")

    pub: zmq.Socket = context.socket(zmq.PUB)
    pub.connect(ZMQ_PUB)

    voltage_query_attempts = 0

    while True:
        try:
            _, _ = shutdown_sub.recv_string(flags=zmq.NOBLOCK).split(' ', 1)
            print("Received shutdown command")
            handle_critical()
        except zmq.error.Again:
            pass

        try:
            _, msg = voltage_sub.recv_string(flags=zmq.NOBLOCK).split(' ', 1)
            voltage = float(msg)
            voltage_query_attempts = 0
        except zmq.error.Again:
            # No new voltage reading
            voltage_query_attempts += 1
            if voltage_query_attempts > 10:
                print("Failing to get voltage readings, assuming critical voltage")
                handle_critical()
            continue

        if voltage == 0:
            # Invalid voltage reading
            continue
        elif voltage > 13.5:
            continue
        elif voltage > 12.8:
            handle_low(pub)
        else:
            print("Voltage critical")
            handle_critical()

        sleep(1 / TICK_RATE)

if __name__ == "__main__":
    main()
