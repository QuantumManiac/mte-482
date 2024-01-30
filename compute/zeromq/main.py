import zmq

def listen(sub: zmq.Socket):
    topic = input("Topic (leave empty for all): ")
    print("Listening...")
    sub.subscribe(topic)
    while True:
        recieved = sub.recv_string()
        topic, message = recieved.split(' ', 1)
        print(f"Received from topic {topic}: {message}")

def send(pub: zmq.Socket):
    topic = input("Topic: ")
    message = input("Message: ")
    
    if topic == '':
        send = message
    else:
        send = topic + ' ' + message

    pub.send_string(send)

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
