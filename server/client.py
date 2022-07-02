import socketio


sio = socketio.Client()
@sio.event
def connect():
    print('connection established')
    sio.emit('client', {'foo': 'bar'})

@sio.on('serve')
def on_message(data):
    print('client received a message!',data)


@sio.on('dataBack')
def on_message(data):
    print('client received a message!',data)
# @sio.event
# def message(data):
#     print('message received with ', data)
#     sio.emit('client', {'response': 'my response'})

@sio.event
def connect_error():
    print("The connection failed!")
    sio.disconnect()

@sio.event
def disconnect():
    print('disconnected from server')
    sio.disconnect()

sio.connect('http://localhost:5000')
while 1:
    a=input()
    sio.emit('cc', {'data': str(a)})
sio.wait()

