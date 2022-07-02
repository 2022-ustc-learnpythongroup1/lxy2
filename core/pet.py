import core.interaction as interaction
from core.act_queue import q as queueA
import queue
import threading
import time
import random
import core.status  as status
from core import cloud
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtWidgets import QWidget, QMenu, QApplication, QSystemTrayIcon, QAction, QMainWindow

from core import actions
from core.actions import Action
from core import settings

interaction.start_processes()
q = queue.PriorityQueue()

if __name__ == '__main__':
    while True:
        time.sleep(1)



class DesktopPet(QMainWindow):
    """桌宠核心类"""


    curAction=actions.fallingBody()
    TIME_INTERVAL=500
    draging = False

    def __init__(self, parent=None, tray=False):
        self.imgDir = settings.IMG_DIR
        super(DesktopPet, self).__init__(parent)
        self.draging = False
        self.autoFalling = False
        self.tray = tray
        #生成当前动作
        self.curAction=actions.fallingBody()
        self.curAction.init(self)
        self.initUI()
        self.WakeUp()


    def initUI(self):
        """初始化窗口"""
        self.setWindowIcon(QIcon(str(self.imgDir / settings.ICON)))
        self.desktop = QApplication.desktop()
        #输出基本环境设置
        print("桌面尺寸 x：", self.desktop.availableGeometry().bottomRight().x(),
              "y:", self.desktop.availableGeometry().bottomRight().y())
        print("屏幕宽:" + str(self.desktop.width()))
        print("屏幕高:" + str(self.desktop.height()))
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint  # 无框，置顶
            |Qt.X11BypassWindowManagerHint # 允许移动出屏幕
        )
        self.move(100, 100)

        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 背景透明
        self.setAutoFillBackground(False)
        if self.tray:
            self.trayMenu()  # 系统托盘

    def trayMenu(self):
        """显示系统托盘"""
        tray = QSystemTrayIcon(self)
        tray.setIcon(QIcon(str(self.imgDir / settings.TRAY_ICON)))
        tray.show()


    def mousePressEvent(self, event):
        """鼠标点击事件"""
        print("clicked!")
        if self.curAction.acceptClick:
            self.curAction.Clicked(event.button())
        if event.button() == Qt.LeftButton:
            self.draging = True
            self.mDragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        # 双击鼠标 启动walk, 所以释放的时候要判断是否是双击的情况

        if self.curAction.acceptRelease:
            self.curAction.Released()
        self.draging = False

    def mouseMoveEvent(self, event):
        #左键按下
        if Qt.LeftButton:
            self.moveDistance = (self.mDragPosition - event.pos()).x()   
            if self.curAction.Move_able:
                self.move(event.globalPos() - self.mDragPosition)
            if not self.curAction.acceptMove:
                pass
                # queueA.put(actions.drag())#调用中断


        """鼠标移动事件"""
        if self.curAction.acceptMove:
            self.curAction.moved()



    def mouseDoubleClickEvent(self, QMouseEvent):
        """鼠标双击事件, 进行walk"""
        if self.curAction.acceptDoubleClick:
            self.curAction.doubleClicked()
        else:
            queueA.put(actions.walk(direction=0))
            #TODO


    def closeEvent(self, QCloseEvent):
        """关闭事件"""
        pass



    def paintEvent(self, QPaintEvent):
        """绘图"""
        painter = QPainter(self)
        #在多次绘图叠加时可以设置叠加的模式
        # painter.CompositionMode(QPainter.CompositionMode_SourceOver)
        if hasattr(self, "pix"):
            painter.drawPixmap(self.rect(), self.pix)
            # t=QPixmap(str(self.imgDir / settings.MOUSE_TO_RIGHT_2))
            # painter.drawPixmap(self.rect(),t)
            painter.drawText(10,100,status.boardText)#here in place of vegitables i want to print the my filenames

            
    def setPix(self, pix):
        """设置帧"""
        if isinstance(pix, QPixmap):
            self.pix = pix
        else:
            # self.pix = QPixmap(pix)
            self.pix = QPixmap(str(settings.IMG_DIR / pix))
        self.pix=self.pix.scaledToWidth(settings.SELF_SIZE,Qt.SmoothTransformation)
        #TODO:
        self.resize(self.pix.size())
        # setMask()的作用是为调用它的控件增加一个遮罩，遮住所选区域以外的部分，使之看起来是透明的。
        # 它的参数可以为QBitmap或QRegion对象，此处调用QPixmap的mask（）函数获得图片自身的遮罩，是一个QBitmap对象，
        # 在示例中使用的是Png格式，它的透明部分实际上就是一个遮罩
        self.setMask(self.pix.mask())
        self.update()

    def ShowWelcome(self):
        """欢迎页面"""
        # queueA.put(actions.fallingBody(self.desktop.availableGeometry().bottomRight().x() - 300, 0))



    def WakeUp(self):
        """定义定时器,通过定时器完成动画功能"""
        
        #设置计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.action)
        self.timer.start(self.TIME_INTERVAL)



    #处理一下动作队列
    def dealWithTheQueue(self):
        try:
            # print(queueA.qsize(),"              ----       ")
            #避免动作序列过量积压
            while(queueA.qsize()>1000):
                print("interation queue overflow")
                queueA.get(block=False)
            while(q.qsize()>1000):
                print("action queue overflow")
                q.get()
            #获取互动
            while True: 
                t=queueA.get(block=False)
                q.put(t)
                # print("ww",t.IsInterrupt)
        # except queue.Empty:
        #     print("get All interactions")
        except BaseException as e:
            # print("end",e)
            pass
        if(status.selected==False and self.curAction.actionName!="hide" and status.flag):
            q.put(actions.hide())
            status.flag=False



    def action(self):
        """加载动作"""
        thr=threading.Thread(target=cloud.cli.start)
        thr.daemon=True
        thr.start()
        self.timer.stop()
        print("MY PLACE:",self.pos().x(),",",self.pos().y())
        self.dealWithTheQueue()
        # self.curAction.finished=True
        #取优先级最高的元素
        if(q.empty()):
            print("empty queue")
            interaction.nothingToDo(self)
            time.sleep(0.1)
        else:
            t=q.get()
            print("t.priority",t.priority)
            # print("t here",t)
            if((not status.selected) ):
                print("a")
            #     print("------------------------------------end-----------------------")
            #     while(not q.empty()):
            #         tt=q.get()
            #         print(tt.actionName,"         ",tt.priority)
            #     exit(0) 
            print("aaaaaha",q.qsize())
            if(t.IsInterrupt and self.curAction.Interupt_able):
                self.curAction.actionInterrupted()
                self.curAction=t
                self.curAction.init(self)
            else:
                q.put(t)
                self.curAction.nextAct()
                QApplication.processEvents()

            #结束上新
            if(self.curAction.finished):
                self.curAction=q.get()
                self.curAction.init(self)
        # print("TIME_INTERVAL",self.TIME_INTERVAL)
        print(self.curAction.actionName,"!!!!!!!!",status.selected)
        self.timer.start(self.TIME_INTERVAL)



