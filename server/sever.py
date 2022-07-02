import eventlet
eventlet.monkey_patch()
import datetime
import socketio
import time
import threading
import random
import sys
import select




sio = socketio.Server(async_mode='eventlet')  # 指明在evenlet模式下

#TODO:deal with the delete
ClientOnlineSid=[]
curClientSid=""


def findCli(sid):
    for index,i in enumerate(ClientOnlineSid):
        if(sid==i):
            return index
    return -1

def GlobalEmit():
    global curClientSid
    for i in ClientOnlineSid:
        if(i==curClientSid):
            print("select----------------",curClientSid)
            sio.emit('response', {'data': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),'selected':'1'},room=i)
        else:
            sio.emit('response', {'data': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),'selected':'0'},room=i)


def nextOne():
    print("-------------new one")
    global curClientSid
    if(len(ClientOnlineSid)==0):
        print("NO BODY HERE")
        return

    print("-------------old",curClientSid)

    if(curClientSid==""):
        curClientSid=ClientOnlineSid[0]
    else:
        Num=findCli(curClientSid)
        print(Num)
        print((Num+1)% len(ClientOnlineSid))
        curClientSid=ClientOnlineSid[(Num+1)% len(ClientOnlineSid)]
    print("-------------new",curClientSid)

    GlobalEmit()



sio = socketio.Server()
app = socketio.Middleware(sio)
# app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('server', {'data': 'connert success'})
    sio.enter_room(sid, 'chat_users')
    ClientOnlineSid.append(sid)
    #是第一个
    if(len(ClientOnlineSid)==1):
        nextOne()


@sio.on('out')
def on_message(sid, data):
    print('Walk to another screen')
    nextOne()

@sio.on('words')
def on_message(sid, data):
    tt=data["data"]
    for i in ClientOnlineSid:
        sio.emit('words', {'data': tt})
    # print('Walk to another screen')

@sio.on('summon')
def on_message(sid, data):
    curClientSid=sid
    GlobalEmit()

    # print('Walk to another screen')


@sio.on('client')
def on_message(sid, data):
    print('I received a message!', data)
    # sio.emit('response', {'data': 'Recieved'})
    


@sio.event
def disconnect(sid):
    global curClientSid
    #选中者失连，选新
    if(sid==curClientSid):
        nextOne()

    ClientOnlineSid.remove(sid)
    sio.leave_room(sid, 'chat_users')
    if(len(ClientOnlineSid)==0):
        curClientSid=""
    print('disconnect ', sid)


def serve_app( _sio, _app):
    app = socketio.Middleware(_sio, _app)
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)


def getinput():
    while True:
        input = select.select([sys.stdin], [], [], 1)[0]
        if input:
            value = sys.stdin.readline().rstrip()
            sio.emit('response', {'data': str(value)})
        time.sleep(1)
    
        # if (value == "q"):
        #     print ("Exiting")
        #     sys.exit(0)
    #     else:
    #         print ("You entered: %s" % value)
    # else:
    #     processSomething()
    # while True:
    #     a=input()
    #     sio.emit('response', {'data': str(a)})
    #     time.sleep(1)


if __name__ == '__main__':
    wst = threading.Thread(target=serve_app, args=(sio,app))
    wst.daemon =  False
    wst.start()

    thr2=threading.Thread(target=getinput)
    thr2.daemon=  False
    thr2.start()
    while True:
        # if(len(ClientOnlineSid)==0):
        #     print("NO BODY HERE")
        #     time.sleep(1)
        # else:
        #     curPRO=(curPRO+1)% len(ClientOnlineSid)
        #     for i in ClientOnlineSid:
        #         if(i==ClientOnlineSid[curPRO]):
        #             sio.emit('response', {'data': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),'selected':'1'},room=i)
        #         else:
        #             sio.emit('response', {'data': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),'selected':'0'},room=i)
        
        # #显示连接的client的sid
        print("---------")
        for i in ClientOnlineSid:
            print(i)
        GlobalEmit()

        # sio.emit('server', {'data': 'haha'})
        time.sleep(5)
    



