# -*- coding: utf-8 -*-
import os
import struct

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
import sys, time
from socket import *
from threading import Thread, Timer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # 전체화면 사용을 위해 Options 모듈 추가
import time
from time import sleep
from omxplayer.player import OMXPlayer

MainUI = '/home/pi/displayUI2.ui'

# ID = None
# chID = None
currAD = None
tempAD = None
prevAD = None
tcpClientA = None
BUFF_SIZE = 1024

def recvFile(FILE_NAME):
    global tcpClientA
    FILE_LEN = 0
    FILE_SIZE = tcpClientA.recv(4)
    FILE_SIZE = struct.unpack('L', FILE_SIZE)[0]

    f = open(FILE_NAME, 'wb')
    while True:
        client_file = tcpClientA.recv(BUFF_SIZE)
        if not client_file:
            break

        f.write(client_file)
        FILE_LEN += len(client_file)

        if FILE_LEN == int(FILE_SIZE):
            break

    f.close()
    print('client : ' + FILE_NAME + ' file transfer')


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # global ID
        # global chID
        uic.loadUi(MainUI, self)
        self.showFullScreen()
        self.setWindowTitle("Display")
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load("/home/pi/proto/Twin/Image/ready.png")
        self.qPixmapFileVar = self.qPixmapFileVar.scaled(780, 370)
        self.label_2.setPixmap(self.qPixmapFileVar)
        self.pushButton.clicked.connect(self.vid)
        self.pushButton_2.clicked.connect(self.vr)
        self.pushButton_3.clicked.connect(self.threeD)
        self.show()

    def setAD(self, ID):
        self.ID = ID
        self.qPixmapFileVar2 = QPixmap()
        self.qPixmapFileVar2.load("/home/pi/proto/Twin/Image/"+ID+".jpg")
        self.qPixmapFileVar2 = self.qPixmapFileVar2.scaled(780, 370)
        self.label_2.setPixmap(self.qPixmapFileVar2)

    def vid(self):
        print("video clicked, ID: " + self.ID)
        if os.path.isfile('/home/pi/proto/Twin/vid/' + self.ID + '.mp4'):
            player = OMXPlayer('/home/pi/proto/Twin/vid/' + self.ID + '.mp4')
            sleep(31)
            player.quit()
        else:
            print("동영상을 제공하지 않는 광고입니다.")

    def vr(self):
        print("VR clicked, ID: " + self.ID)
        options = Options()
        options.add_argument('--kiosk')  # chrome에서 F11을 눌러 전체화면으로 넓히는 옵션
        chrome_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=options)
        # chrome_driver = webdriver.Chrome(chrome_options=options)
        # 이부분만 수정해주면 됨
        if self.ID == 'm50':  # 골프장 vr
            # chrome_driver = webdriver.Chrome(chrome_options=options)
            chrome_driver.get("https://viewer.youvr.io/post/view/OpDnGyKzp9RMKVg9")

        elif self.ID == 'f20':
            # chrome_driver = webdriver.Chrome(chrome_options=options)
            chrome_driver.get("https://viewer.youvr.io/post/view/1nmeOk1YJ2kZWgBG")
        time.sleep(30)  # 터치가 끝날 때 까지로 바꿀 수는 없을까? (마지막 터치 인식 후 5초 뒤 종료라던지..)
        chrome_driver.quit()

    def threeD(self):
        print("3D clicked, ID: " + self.ID)
        if os.path.isfile('/home/pi/proto/Twin/3D/' + self.ID + '.mp4'):
            player = OMXPlayer('/home/pi/proto/Twin/3D/' + self.ID + '.mp4')
            sleep(31)
            player.quit()
        else:
            print("3D 모델을 제공하지 않는 광고입니다.")


class ClientThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        host = '192.168.103.67'
        port = 9899
        BUFFER_SIZE = 1024
        global tcpClientA
        global currAD
        global prevAD
        global ID
        #global IDflag
        tcpClientA = socket(AF_INET, SOCK_STREAM)
        tcpClientA.connect((host, port))
        print("서버와 연결되었습니다")

        while True:
            data = tcpClientA.recv(BUFFER_SIZE)
            msg = data.decode()
            if msg == 'start':
                print('광고시작 메시지를 받았습니당')
            elif msg == 'pause':
                print("광고중단 메시지를 받았습니당")
            elif msg == 'exit':
                print("빠이욤")
                break
            elif msg[:3] == 'img':
                print("img 추가 메시지 받음요")
                f = msg[3:]
                recvFile('/home/pi/proto/Twin/Image/' + f + '.jpg')
            elif msg[:3] == 'vid':
                f = msg[3:]
                recvFile('/home/pi/proto/Twin/vid/' + f + '.mp4')
            elif msg[:2] == 'vr':
                f = msg[2:]
            elif msg[:2] == '3d':
                f = msg[2:]
                recvFile('/home/pi/proto/Twin/3D/' + f + '.mp4')
            elif msg[:3] == 'del':
                f = msg[3:]
                if os.path.isfile('/home/pi/proto/Twin/Image/' + f + '.jpg'):
                    os.remove('/home/pi/proto/Twin/Image/' + f + '.jpg')
                if os.path.isfile('/home/pi/proto/Twin/vid/' + f + '.mp4'):
                    os.remove('/home/pi/proto/Twin/vid/' + f + '.mp4')
                if os.path.isfile('/home/pi/proto/Twin/3D/' + f + '.mp4'):
                    os.remove('/home/pi/proto/Twin/3D/' + f + '.mp4')
            else:
                print(msg)
                # currAD = ID
                window.setAD(msg)
                # IDflag= True
        tcpClientA.close()


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    clientThread = ClientThread(window)  # 쓰레드 객체 생성
    clientThread.start()  # 쓰레드 시작
    sys.exit(App.exec())
