import zmq
import socketio
import threading

# Thread for proxying messages between publisher and subscriber
def proxy(context: zmq.Context):

    frontend = context.socket(zmq.XSUB)  # Frontend for publishers
    backend = context.socket(zmq.XPUB)   # Backend for subscribers

    frontend.bind("tcp://*:5556")  # Publisher connects here
    backend.bind("tcp://*:5555")   # Subscriber connects here

    # Start the proxy
    zmq.proxy(frontend, backend)

# Thread for relaying messages from zeromq to socketio
def relay(context: zmq.Context):

    sub = context.socket(zmq.SUB)
    pub = context.socket(zmq.PUB)
    sub.connect("tcp://*:5555")
    pub.connect("tcp://*:5556")

    sub.setsockopt(zmq.SUBSCRIBE, b"")





if __name__ == '__main__':
    context = zmq.Context()
    proxy_thread = threading.Thread(target=proxy, args=(context,))
    proxy_thread.start()
    # relay_thread = threading.Thread(target=relay, args=(context,))
    # relay_thread.start()

    proxy_thread.join()
    # relay_thread.join()
