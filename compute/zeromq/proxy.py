import zmq

context = zmq.Context()
frontend = context.socket(zmq.XSUB)  # Frontend for publishers
backend = context.socket(zmq.XPUB)   # Backend for subscribers

frontend.bind("tcp://*:5556")  # Publisher connects here
backend.bind("tcp://*:5555")   # Subscriber connects here

# Start the proxy
zmq.proxy(frontend, backend)
