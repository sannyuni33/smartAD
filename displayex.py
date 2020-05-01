import sys, time
from PyQt5.QtWidgets import QScrollBar, QSplitter, QTableWidgetItem, QTableWidget, QComboBox, QVBoxLayout, QGridLayout, \
    QDialog, QWidget, QPushButton, QApplication, QMainWindow, QAction, QMessageBox, QLabel, QTextEdit, QProgressBar, \
    QLineEdit
import socket
from threading import Thread,Timer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5 import uic
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSlot, QTimer


tcpClientA = None
MainUI = 'label5.ui'
#IDflag = None # idflag boolean 처리

class Window(QDialog, ):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(MainUI, self)
        self.setWindowTitle("영상윤주 서버 GUI")
        self.label.setStyleSheet('image:url(video.mp4)')
        #self.webEngineView.load(QUrl("https://www.google.com"))
        self.pushButton.clicked.connect(self.urlGo)
        self.pushButton_2.clicked.connect(self.Stop)
        self.pushButton_3.clicked.connect(self.modelclick)

    def aaa(self, ID):

        if ID == 'f10':
            self.label.setStyleSheet('image:url(m10.jpg)')

        else:
            self.label.setStyleSheet('image:url(m20.jpg)')

    def urlGo(self):

        self.webEngineView.load(QUrl("https://viewer.youvr.io/post/view/1mwWGkzGqpAqXxjz"))
        self.timer = QTimer(self)
        self.timer.start(5000)
        self.timer.timeout.connect(self.urlGo)
        self.timer.stop()


    def Stop(self):#(self,ID):

        self.webEngineView.load(QUrl("https://www.naver.com"))
        #if ID =='stop':
            #self.webEngineView.stop("https://www.naver.com")


    """def videoclick(self):
        print('PyQt5 video click')
        self.QWebEngineView이름.load(QUrl("주소(문자열)"))

    def vrimgclick(self):
        print('PyQt5 video click')"""

    def modelclick(self):
        print('PyQt5 3dmodeling click')


class ClientThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        host = '192.168.100.38'
        port = 9988
        BUFFER_SIZE = 2048
        global tcpClientA
        #global IDflag
        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpClientA.connect_ex((host, port))


        while True:
            data = tcpClientA.recv(BUFFER_SIZE)
            ID = data.decode()
            window.aaa(ID)
            #IDflag= True


        tcpClientA.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    clientThread = ClientThread(window) #쓰레드 객체 생성
    clientThread.start() # 쓰레드 시작
    window.exec()
    sys.exit(app.exec_())





