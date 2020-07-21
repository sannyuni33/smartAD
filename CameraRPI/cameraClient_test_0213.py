# -*- coding:utf-8 -*-
import sys
import os
import struct
import time
from socket import *
from threading import Thread
from picamera import PiCamera
chTime = 5
tcpClientA = None
BUFF_SIZE = 1024
camera = PiCamera()


class ClientThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        host ='192.168.103.37'
        port = 9899
        BUFFER_SIZE = 1024
        global tcpClientA
        global chTime
        tcpClientA = socket(AF_INET, SOCK_STREAM)
        tcpClientA.connect((host, port))
        print("서버와 연결되었습니다")

        while True:
            data = tcpClientA.recv(BUFFER_SIZE)
            msg = data.decode('utf-8')
            if msg == 'start':
                print("광고시작 메시지를 받았습니당")
                newThread = CameraWork(tcpClientA)
                newThread.setDaemon(True)
                newThread.start()
            elif msg == 'pause':
                newThread.setStop()
                print("광고중단 메시지를 받았습니당")
            elif msg == 'exit':
                print("빠이욤")
                break
            elif int(msg) <= 100:
                chTime = int(msg)
                print("카메라 촬영 주기 변경: "+str(chTime)+"초")
        tcpClientA.close()


class CameraWork(Thread):
    def __init__(self, tcpClientA):
        Thread.__init__(self)
        self.clientSocket = tcpClientA
        self.FILE_NAME = 'image.jpg'
        self.onOff = True
        global camera
        global chTime

    def setStop(self):
        self.onOff = False

    def run(self):
        while True:
            self.captureImage(self.FILE_NAME, chTime)
            self.sendImage(self.FILE_NAME)
            os.remove(r'image.jpg')
            if not self.onOff:
                break

    def captureImage(self, FILE_NAME, chTime):
        print("찍습니다")
        time.sleep(chTime)
        camera.capture('/home/pi/sang/'+FILE_NAME)

    def sendImage(self, FILE_NAME):
        FILE_SIZE = os.path.getsize(FILE_NAME)
        FILE_SIZE = struct.pack('L', FILE_SIZE)
        print("FILE_SIZE: ", str(FILE_SIZE))

        try:
            n = 0
            f = open('/home/pi/sang/' + FILE_NAME, 'rb')
            i = f.read(BUFF_SIZE)
            self.clientSocket.send(FILE_SIZE)
            n += 1
            while i:
                self.clientSocket.send(i)
                i = f.read(BUFF_SIZE)
            f.close()
            print('(check) ' + FILE_NAME + ' transfer complete')
        except Exception as e:
            sys.exit()


if __name__ == '__main__':
    clientThread = ClientThread()
    clientThread.start()

