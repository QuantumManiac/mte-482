import zmq
import sys
import time

def listen(sub: zmq.Socket):
    print("Listening...")
    while True:
        message = sub.recv_string()
        print("Received: %s" % message)

def send(pub: zmq.Socket):
    message = input("Message: ")
    pub.send_string(message)

def main():
    context = zmq.Context()
    pub = context.socket(zmq.PUB)
    sub = context.socket(zmq.SUB)
    pub.connect("tcp://127.0.0.1:5556")
    sub.connect("tcp://127.0.0.1:5555")
    sub.subscribe('')
    while True:
        command = input("Command [l]isten, [s]end, or [q]uit: ")

        if command == 'l':
            listen(sub)
        if command == 's':
            send(pub)
        if command == 'q':
            break

if __name__ == '__main__':
    main()
