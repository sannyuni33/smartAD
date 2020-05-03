# 동영상, VR 브라우저, 3D 모델 동영상 띄우기 수정 완료
# ID 받아서 사진 띄우기, 이전 광고 출력 수정 필요

import sys, time
from PyQt5.QtWidgets import QScrollBar, QSplitter, QTableWidgetItem, QTableWidget, QComboBox, QVBoxLayout, QGridLayout, \
    QDialog, QWidget, QPushButton, QApplication, QMainWindow, QAction, QMessageBox, QLabel, QTextEdit, QProgressBar, \
    QLineEdit
import socket
from threading import Thread, Timer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5 import uic

from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # 전체화면 사용을 위해 Options 모듈 추가
import time
from time import sleep

from omxplayer import OMXPlayer # 이거는 라즈베리파이에서만 돌아감

tcpClientA = None
MainUI = 'label5.ui'


# IDflag = None # idflag boolean 처리

class Window(QDialog, ):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(MainUI, self)
        self.setWindowTitle("영상윤주 디스플레이 GUI")
        self.label.setStyleSheet('image:url(ready.png)')
        self.pushButton.clicked.connect(self.vid)
        self.pushButton_2.clicked.connect(self.vr)
        self.pushButton_3.clicked.connect(self.ThreeD)
        self.pushButton_3.clicked.connect(self.preAd)

    def aaa(self, ID):

        if ID == 'f10':
            self.label.setStyleSheet('image:url(m10.jpg)')

        else:
            self.label.setStyleSheet('image:url(m20.jpg)')

    def vid(self):

        # 라즈베리파이에서 사용되는 코드
        player = OMXPlayer('/home/pi/flatfish.mp4')

        player.play()
        sleep(10)  # 동영상 재생 시간 만큼 할당해야됨
        # player.pause()
        player.quit()

    def vr(self):  # (self,ID):

        options = Options()
        options.add_argument('--kiosk')  # chrome에서 F11을 눌러 전체화면으로 넓히는 옵션
        chrome_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=options)
        # chrome_driver = webdriver.Chrome(chrome_options=options)
        chrome_driver.get("https://viewer.youvr.io/post/view/1mwWGkzGqpAqXxjz")
        time.sleep(30)  # 터치가 끝날 때 까지로 바꿀 수는 없을까? (마지막 터치 인식 후 5초 뒤 종료라던지..)
        chrome_driver.quit()

    def ThreeD(self):

        # 라즈베리파이에서는 이 코드
        player = OMXPlayer('/home/pi/apt.mp4')

        player.play()
        sleep(10)  # 동영상 재생 시간 만큼 할당해야됨
        #      player.pause()

        player.quit()

    def preAd(self):
        print('이전광고')


class getID:
    def __init__(self, window):
        self.window = window

        ID = input()
        window.aaa(ID)


"""
class ClientThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        host = '172.20.10.4'
        port = 9966
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
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    # clientThread = ClientThread(window) #쓰레드 객체 생성
    # clientThread.start() # 쓰레드 시작
    window.exec()
    sys.exit(app.exec_())
