
import socketio
import time
from core.act_queue import q as queueA
from core import actions
from core import status

sio = socketio.Client()


def mydisconnected():
    if(status.connected):
        status.connected=False 
        status.selected=True
        

def myconnected():
    if(not status.connected):
        status.connected=True
        print("connected")
        # queueA.put(actions.hide())

def myselected():
    print("selected")
    status.flag=True
    status.selected=True

def myreleased():
    print("release")
    # if(not status.selected):
        # queueA.put(actions.hide())
    status.flag=True
    status.selected=False



class client():

    @sio.event
    def connect():
        sio.emit('client', {'data': 'connection established'})
        myconnected()

    @sio.on('server')
    def on_message(data):
        print('I get :',data['data'])


    @sio.on('response')
    def on_message(data):
        print('Client get response:',data)
        if(data['selected']=='1'):
            myselected()
        elif (data['selected']=='0'):
            myreleased()
            
    @sio.on('words')
    def on_message(data):
        print('Client get words:',data)
        status.boardText=data["data"]


    @sio.event
    def message(data):
        print('message received with ', data)
        sio.emit('client', {'response': 'my response'})
        


    @sio.event
    def disconnect():
        mydisconnected()

  
    def start(self):
        if(not sio.connected):
            try:
                sio.connect('http://124.223.84.162:5000')
            except BaseException as e:
                mydisconnected()   

    def get_out(self):
        if(sio.connected):
            sio.emit('out', {'data': ""})        

    def summon(self):
        print("SUMMON")
        if(sio.connected):
            sio.emit('summon', {'data': "summon"})    
            
    def update_words(self):
        if(sio.connected):
            sio.emit('words', {'data': status.boardText})    
        # while True:
        #     try:
        #         sio.connect('http://localhost:5000')
        #         while sio.connected:
        #             a=input()
        #             sio.emit('client', {'data': str(a)})
        #     except BaseException as e:
        #         mydisconnected()
        #     time.sleep(5)



cli=client()
if __name__ == '__main__':
    cli.start()