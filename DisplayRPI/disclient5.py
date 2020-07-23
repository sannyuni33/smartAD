# -*- coding: utf-8 -*-
import os
import struct

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import sys
from socket import *
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from time import sleep
from omxplayer.player import OMXPlayer

MainUI = '/home/pi/displayUI2.ui'

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
        self.chAD = None
        self.prevAD = None
        self.currAD = None
        self.nextAD = None
        self.usingDT = False
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
        if not self.usingDT:
            self.prevAD = self.currAD
            self.currAD = ID
            if self.chAD:
                self.currAD = chAD
                self.chAD = None
        else:
            self.nextAD = ID
            if chAD:
                self.nextAD = chAD
                self.chAD = None

    def postAD(self):
        self.qPixmapFileVar2 = QPixmap()
        self.qPixmapFileVar2.load("/home/pi/proto/Twin/Image/" + self.currAD + ".jpg")
        self.qPixmapFileVar2 = self.qPixmapFileVar2.scaled(780, 370)
        self.label_2.setPixmap(self.qPixmapFileVar2)
        self.prevAD, self.currAD = self.currAD, self.prevAD
        if self.nextAD:
            self.currAD = self.nextAD
            self.nextAD = None

    def postPrevAD(self):
        self.prevAD, self.currAD = self.currAD, self.prevAD
        self.postAD()

    def setChAD(self, chAD):
        self.chAD = chAD

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
        if os.path.isfile('/home/pi/proto/Twin/vr/' + self.ID + '.txt'):
            f = open('/home/pi/proto/Twin/vr/' + self.ID + '.txt', 'r')
            self.vrLink = f.readline()
            f.close()
            options = Options()
            options.add_argument('--kiosk')
            chrome_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=options)
            chrome_driver.get(self.vrLink)
            time.sleep(30)  # 터치가 끝날 때 까지로 바꿀 수는 없을까? (마지막 터치 인식 후 5초 뒤 종료라던지..)
            chrome_driver.quit()
        else:
            print("VR을 제공하지 않는 광고입니다.")

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
        global tcpClientA, chAD
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
                f = msg[3:]
                recvFile('/home/pi/proto/Twin/Image/' + f + '.jpg')
            elif msg[:3] == 'vid':
                f = msg[3:]
                recvFile('/home/pi/proto/Twin/vid/' + f + '.mp4')
            elif msg[:2] == 'vr':
                f = msg[2:]
                recvFile('/home/pi/proto/Twin/vr/' + f + '.txt')
            elif msg[:2] == '3d':
                f = msg[2:]
                recvFile('/home/pi/proto/Twin/3D/' + f + '.mp4')
            elif msg[:3] == 'del':
                f = msg[3:]
                if os.path.isfile('/home/pi/proto/Twin/Image/' + f + '.jpg'):
                    os.remove('/home/pi/proto/Twin/Image/' + f + '.jpg')
                if os.path.isfile('/home/pi/proto/Twin/vid/' + f + '.mp4'):
                    os.remove('/home/pi/proto/Twin/vid/' + f + '.mp4')
                if os.path.isfile('/home/pi/proto/Twin/vr/' + f + '.txt'):
                    os.remove('/home/pi/proto/Twin/vr/' + f + '.txt')
                if os.path.isfile('/home/pi/proto/Twin/3D/' + f + '.mp4'):
                    os.remove('/home/pi/proto/Twin/3D/' + f + '.mp4')
            elif msg[:2] == 'ch':
                f = msg[2:]
                window.setChAD(f)
                window.postAD()
            else:
                print(msg)
                window.setAD(msg)
                window.postAD()
        tcpClientA.close()


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    clientThread = ClientThread(window)
    clientThread.start()
    sys.exit(App.exec())
