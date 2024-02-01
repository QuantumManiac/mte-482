import zmq
import socketio
import threading
import time
import eventlet

# Thread for proxying messages between publisher and subscriber
def proxy(context: zmq.Context):

    frontend = context.socket(zmq.XSUB)  # Frontend for publishers
    backend = context.socket(zmq.XPUB)   # Backend for subscribers

    frontend.bind("tcp://*:5556")  # Publisher connects here
    backend.bind("tcp://*:5555")   # Subscriber connects here

    # Start the proxy
    zmq.proxy(frontend, backend)

# Thread for relaying messages from zeromq to socketio
def sio(sio: socketio.Server):
    app = socketio.WSGIApp(sio)

    @sio.on('zmq_message')
    def zmq_message(event, data):
        sio.emit(data['topic'], data['msg'])
    
    eventlet.wsgi.server(eventlet.listen(('', 5557)), app)

def relay(context: zmq.Context):
    sub: zmq.Socket = context.socket(zmq.SUB)
    pub: zmq.Socket = context.socket(zmq.PUB)
    sub.connect("tcp://127.0.0.1:5555")
    pub.connect("tcp://127.0.0.1:5556")

    sub.setsockopt(zmq.SUBSCRIBE, b"")

    sio = socketio.SimpleClient()
    time.sleep(1)
    sio.connect('http://localhost:5557', wait_timeout=5, transports=['websocket'])
    with sio:
        while True:
            topic, msg = sub.recv_string().split(' ', 1)
            sio.emit('zmq_message', {'topic': topic, 'msg': msg})

if __name__ == '__main__':
    zmq_context = zmq.Context()
    sio_server = socketio.Server(cors_allowed_origins='*')

    sio_thread = threading.Thread(target=sio, args=(sio_server,))
    zmq_thread = threading.Thread(target=proxy, args=(zmq_context,))
    relay_thread = threading.Thread(target=relay, args=(zmq_context,))
    zmq_thread.start()
    sio_thread.start()
    relay_thread.start()

    sio_thread.join()
    zmq_thread.join()
    relay_thread.join()
