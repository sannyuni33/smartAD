#-*- coding:utf-8 -*-
import sys
import os
import struct
import time
from socket import *
from threading import Thread
import datetime
from picamera import PiCamera
chTime = 5
tcpClientA = None
BUFF_SIZE=1024
camera=PiCamera()

class ClientThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        host = '172.30.1.54'
        port = 9899
        BUFFER_SIZE = 1024
        global tcpClientA
        global chTime
        tcpClientA = socket(AF_INET, SOCK_STREAM)
        tcpClientA.connect((host, port))
        print("서버랑 연결되었습니다")

        while True:
            data = tcpClientA.recv(BUFFER_SIZE)
            msg = data.decode('utf-8')
            if msg == 'start':
                print("광고 시작 메시지를 받았습니당")
                newThread = CameraWork(tcpClientA)
                newThread.setDaemon(True)
                newThread.start()
            elif msg == 'pause':
                newThread.setStop()
                # 쓰레드 자체를 실제로 종료시킴! 강제 종료도 아님!
                # CameraWork 객체의 onOff 가 False 니까 반복문이 멈추고 run() 이 끝나기 때문
            elif msg == 'exit':
                print("빠이욤")
                break
            elif int(msg) <= 100:
                chTime = int(msg)
                print(chTime)
            else:
                print("오류")
                break
        tcpClientA.close()


class CameraWork(Thread):
    def __init__(self, tcpClientA):
        Thread.__init__(self)
        self.clientSocket = tcpClientA
        self.FILE_NAME = ('image.jpg')
        self.onOff = True
        global camera
        global chTime

    def setStop(self):
        self.onOff = False

    def run(self):
        while True:
            print("찍습니다")
            self.captureImage(self.FILE_NAME,chTime)
            time.sleep(3)
            print("보내기 전이요")
            self.sendImage(self.FILE_NAME)
            print("send이미지 끝")
            time.sleep(2)
            print("삭제 전이요")
            os.remove(r'image.jpg')
            print('삭제 완료')
            if not self.onOff:
                break

    def captureImage(self, FILE_NAME, chTime):
        time.sleep(chTime/2)
        print(chTime)
        time.sleep(chTime/2)
        print(chTime/2)
        camera.capture('/home/pi/sang/'+FILE_NAME)

    def sendImage(self, FILE_NAME):
        FILE_SIZE = os.path.getsize(FILE_NAME)
        FILE_SIZE = struct.pack('L', FILE_SIZE)

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
            print('send함수 끝')

        except Exception as e:
            sys.exit()


if __name__ == '__main__':

    clientThread = ClientThread()
    clientThread.start()

