# -*- coding: utf-8 -*-
import os
import struct
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from socket import *
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from time import sleep
from omxplayer.player import OMXPlayer

MainUI = '/home/pi/displayUIsang2.ui'

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
        self.pushButton_4.clicked.connect(self.postPrevAD)
        self.pushButton_4.setIcon(QIcon("/home/pi/sss.jpg"))
        self.pushButton_4.setIconSize(QSize(70, 40))
        self.show()

    def showMessageBox(self, dt):
        msgbox = QtWidgets.QMessageBox(self)
        msgbox.critical(self, 'MessageBox title', dt+'을 제공하지 않는 광고입니다.\n')

    def setAD(self, ID):
        if not self.usingDT:
            self.prevAD = self.currAD
            self.currAD = ID
        else:
            self.nextAD = ID

    def postAD(self):
        self.qPixmapFileVar2 = QPixmap()
        self.qPixmapFileVar2.load("/home/pi/proto/Twin/Image/" + self.currAD + ".jpg")
        self.qPixmapFileVar2 = self.qPixmapFileVar2.scaled(780, 370)
        self.label_2.setPixmap(self.qPixmapFileVar2)
        if self.nextAD:
            self.currAD = self.nextAD
            self.nextAD = None
            self.postAD()

    def postPrevAD(self):
        self.prevAD, self.currAD = self.currAD, self.prevAD
        self.postAD()
        global tcpClientA
        tcpClientA.send(self.currAD.encode('utf-8'))

    def vid(self):
        print("video clicked, ID: " + self.currAD)
        if os.path.isfile('/home/pi/proto/Twin/vid/' + self.currAD + '.mp4'):
            player = OMXPlayer('/home/pi/proto/Twin/vid/' + self.currAD + '.mp4')
            sleep(31)
            player.quit()
        else:
            self.showMessageBox('동영상')

    def vr(self):
        print("VR clicked, ID: " + self.currAD)
        if os.path.isfile('/home/pi/proto/Twin/vr/' + self.currAD + '.txt'):
            f = open('/home/pi/proto/Twin/vr/' + self.currAD + '.txt', 'r')
            self.vrLink = f.readline()
            f.close()
            options = Options()
            options.add_argument('--kiosk')
            chrome_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=options)
            chrome_driver.get(self.vrLink)
            time.sleep(30)
            chrome_driver.quit()
        else:
            self.showMessageBox('VR')

    def threeD(self):
        print("3D clicked, ID: " + self.currAD)
        if os.path.isfile('/home/pi/proto/Twin/3D/' + self.currAD + '.mp4'):
            player = OMXPlayer('/home/pi/proto/Twin/3D/' + self.currAD + '.mp4')
            sleep(31)
            player.quit()
        else:
            self.showMessageBox('3D모델')


class ClientThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        host = '192.168.102.29'
        port = 9899
        BUFFER_SIZE = 1024
        global tcpClientA
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
