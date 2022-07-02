from multiprocessing import Process,Queue
from queue import Empty
import threading
import os
import time
import random
from core import actions
from core.act_queue import q as queueA
from core.cloud import cli
from core import status
from extent import weather
from extent import gesture
# from core.cloud import connected as WEB_CONNECTED
# from core.cloud import chosen as WEB_CHOSEN




def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def Qadd(qI):
    queueA.put(qI)
    print("queue size####################################################",queueA.qsize())

def start_getweather():
    myweather = threading.Thread(target=weather.get_weather)
    myweather.daemon=True
    myweather.start()

def start_getsture():
    mygetsture = threading.Thread(target=gesture.detect)
    mygetsture.daemon=True
    mygetsture.start()
    
def start_facedetect():
    myfacedetect = threading.Thread(target=face.start_facedetect)
    myfacedetect.daemon=True
    myfacedetect.start()

def start_processes():
    start_getweather()
    # start_facedetect()

    pass
    
def randomAct():
    Qadd(actions.walk(direction=1))
    t=random.randint(0, 8)
    # # t=0
    if(status.selected):
        # Qadd(actions.snail())
        Qadd(actions.stand())

        # Qadd(actions.board(text=str(status.weather)))

        # if(t>4):
        #     Qadd(actions.walk(direction=0))
        # else:
        #     Qadd(actions.walk(direction=1))


        # # if t>1:
        # # Qadd(actions.walkl())
        # if t==1:
        #     # print("StTTTTands")
        #     Qadd(actions.stand())
        # if t==2:
        #     Qadd(actions.boring())
        # if t==3:
        #     Qadd(actions.lie())
        # if t==4 or t==5:
        #     Qadd(actions.pull())
        # if t==6:
        #     Qadd(actions.sing())
        # if t==7:
        #     Qadd(actions.board())
        # if t==8:
        #     Qadd(actions.walk(direction=0))
        # if t==9:
        #     Qadd(actions.walk(direction=1))
        # if t>=10:
        #     Qadd(actions.hide())   
        print("randomAct")
    else:
        Qadd(actions.hide())




    # currentMovie = random.choice(self.allActions)
def nothingToDo(father):
    randomAct()
    # q.put(actions.walk(father))
    print("nothingToDo")
    # currentMovie = random.choice(self.allActions)

    # time.sleep(6)
    # print(q.get())    # prints "[42, None, 'hello']"
    
#     try:
#         print(q.get(block=False))    # prints "[42, None, 'hello']"
#     except Empty:
#          print("clean")
#     # p.join()
# a()