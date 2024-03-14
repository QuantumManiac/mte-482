import zmq
import socketio
import threading
import time
import eventlet
import json
import argparse

# Thread for proxying messages between publisher and subscriber
def zmq_server(context: zmq.Context):

    frontend = context.socket(zmq.XSUB)  # Frontend for publishers
    backend = context.socket(zmq.XPUB)   # Backend for subscribers

    frontend.bind("tcp://*:5556")  # Publisher connects here
    backend.bind("tcp://*:5555")   # Subscriber connects here

    # Start the proxy
    zmq.proxy(frontend, backend)

# Thread for relaying messages from zeromq to socketio and back
def sio_server(sio: socketio.Server, context: zmq.Context, print_messages=False):
    app = socketio.WSGIApp(sio)
    pub: zmq.Socket = context.socket(zmq.PUB)
    pub.connect("tcp://127.0.0.1:5556")

    @sio.on('zmq_message')
    def zmq_message(event, data):
        if print_messages:
            print(f'[from ZMQ] zmq_{data["topic"]}: {data["msg"]}')
        sio.emit(f'zmq_{data["topic"]}', data['msg'])

    @sio.on('ui_message')
    def ui_message(event, data):
        if print_messages:
            print(f'[from UI] ui_{data["topic"]}: {data["msg"]}')
        pub.send_string(f'ui_{data["topic"]} {data["msg"]}')

    eventlet.wsgi.server(eventlet.listen(('', 5557)), app, log_output=False)

def zmq_to_sio(context: zmq.Context):
    sub: zmq.Socket = context.socket(zmq.SUB)
    sub.setsockopt(zmq.CONFLATE, 1)
    sub.connect("tcp://127.0.0.1:5555")
    sub.setsockopt(zmq.SUBSCRIBE, b"")

    sio = socketio.SimpleClient()
    time.sleep(1)
    # sio.connect('http://192.168.137.10:5557', wait_timeout=5, transports=['websocket'])
    sio.connect('http://172.20.10.4:5557', wait_timeout=5, transports=['websocket'])
    with sio:
        while True:
            topic, msg = sub.recv_string().split(' ', 1)

            try :
                msg: dict = json.loads(msg)
            except ValueError:
                pass

            sio.emit('zmq_message', {'topic': topic, 'msg': msg})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--print-messages', action='store_true', help='Print messages to console')
    args = parser.parse_args()
    print_messages = args.print_messages

    zmq_ctx = zmq.Context()
    sio_srv = socketio.Server(cors_allowed_origins='*')

    sio_thread = threading.Thread(target=sio_server, args=(sio_srv, zmq_ctx, print_messages))
    zmq_thread = threading.Thread(target=zmq_server, args=(zmq_ctx,))
    relay_thread = threading.Thread(target=zmq_to_sio, args=(zmq_ctx,))

    zmq_thread.start()
    sio_thread.start()
    relay_thread.start()

    print('Server started')

    sio_thread.join()
    zmq_thread.join()
    relay_thread.join()
