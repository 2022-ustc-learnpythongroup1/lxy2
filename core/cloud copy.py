import socketio
import time
# import core.interaction as interaction
from core.act_queue import q as queueA

sio = socketio.Client()

# , engineio_logger=True logger=True)
@sio.event
def connect():
    print('connection established')
    sio.emit('client', {'data': 'connection established'})


@sio.on('server')
def on_message(data):
    print('I get :',data['data'])


@sio.on('response')
def on_message(data):
    print('Client get response:',data['data'])



@sio.event
def message(data):
    print('message received with ', data)
    sio.emit('client', {'response': 'my response'})

# @sio.event
# def connect_error():
#     print("The connection failed!")
#     sio.disconnect()

# @sio.event
# def disconnect():
#     print('disconnected from server')
#     sio.disconnect()
# sio.re

connected=False
chosen=True
def get_connected():
    pass 


while True:
    try:
        sio.connect('http://localhost:5000')
        while sio.connected:
            a=input()
            sio.emit('client', {'data': str(a)})
        # sio.wait()
    except BaseException as e:
        # print(e)
        pass
    time.sleep(5)
# while 1:
#     # sio.

# sio.wait()

