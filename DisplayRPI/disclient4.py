# -*- coding: utf-8 -*-
import os
import struct

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
import sys, time
from socket import *
from threading import Thread, Timer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # 전체화면 사용을 위해 Options 모듈 추가
import time
from time import sleep
from omxplayer import OMXPlayer

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
        self.setWindowTitle("Display")
        self.setGeometry(-10, 0, 810, 600)

        # creating a label widget
        self.label = QLabel(self)

        self.label.setStyleSheet('image:url(/home/pi/proto/Twin/Image/ready.png)')
        self.label.setGeometry(40, 30, 700, 300)
        self.button_1 = QPushButton("Video", self)
        self.button_1.setGeometry(100, 350, 160, 70)
        self.button_1.clicked.connect(self.vid)

        self.button_2 = QPushButton("VR", self)
        self.button_2.resize(160, 70)
        self.button_2.move(310, 350)
        self.button_2.clicked.connect(self.vr)

        self.button_3 = QPushButton("3D", self)
        self.button_3.setGeometry(520, 350, 160, 70)
        self.button_3.clicked.connect(self.threeD)

        # show all the widgets
        self.show()

    def setAD(self, ID):
        self.ID = ID
        self.label.setStyleSheet('image:url(/home/pi/proto/Twin/Image/' + ID + '.jpg)')

    def vid(self):
        print("video clicked, ID: " + self.ID)
        player = OMXPlayer('/home/pi/proto/Twin/vid/' + self.ID + '.mp4')
        player.play()
        sleep(31)
        player.quit()

    def vr(self):
        print("VR clicked, ID: " + self.ID)
        options = Options()
        options.add_argument('--kiosk')  # chrome에서 F11을 눌러 전체화면으로 넓히는 옵션
        chrome_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=options)
        # chrome_driver = webdriver.Chrome(chrome_options=options)
        # 이부분만 수정해주면 됨
        if self.ID == 'm50':  # 골프장 vr
            chrome_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=options)
            # chrome_driver = webdriver.Chrome(chrome_options=options)
            chrome_driver.get("https://viewer.youvr.io/post/view/OpDnGyKzp9RMKVg9")

        elif self.ID == 'f20':
            chrome_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=options)
            # chrome_driver = webdriver.Chrome(chrome_options=options)
            chrome_driver.get("https://viewer.youvr.io/post/view/1nmeOk1YJ2kZWgBG")
        time.sleep(30)  # 터치가 끝날 때 까지로 바꿀 수는 없을까? (마지막 터치 인식 후 5초 뒤 종료라던지..)
        chrome_driver.quit()

    def threeD(self):
        print("3D clicked, ID: " + self.ID)
        if self.ID == 'm20':  # 아이폰
            player = OMXPlayer('/home/pi/proto/Twin/3D/m20.mp4')
            player.play()
            sleep(21)  # 20초길이 동영상
            player.quit()
        elif self.ID == 'm30':  # 텐트
            player = OMXPlayer('/home/pi/proto/Twin/3D/m30.mp4')
            player.play()
            sleep(26)  # 25초길이 동영상
            player.quit()
        elif self.ID == 'm51':  # BMW
            player = OMXPlayer('/home/pi/proto/Twin/3D/m51.mp4')
            player.play()
            sleep(26)  # 25초길이 동영상
            player.quit()
        elif self.ID == 'f31':  # 유모차
            player = OMXPlayer('/home/pi/proto/Twin/3D/f31.mp4')
            player.play()
            sleep(31)  # 30초길이 동영상
            player.quit()
        elif self.ID == 'f42':  # 핸드백
            player = OMXPlayer('/home/pi/proto/Twin/3D/f42.mp4')
            player.play()
            sleep(26)  # 30초길이 동영상
            player.quit()
        elif self.ID == 'f50':  # 아파트 내부구조
            player = OMXPlayer('/home/pi/proto/Twin/3D/f50.mp4')
            player.play()
            sleep(31)  # 30초길이 동영상
            player.quit()


class ClientThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        host = '172.30.1.16'
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
