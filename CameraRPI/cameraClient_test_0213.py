# -*- coding:utf-8 -*-
import sys
import os
import struct
import time
from socket import *
from threading import Thread
from picamera import PiCamera

tcpClientA = None
BUFF_SIZE = 1024


class ClientThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        host = '172.30.1.23'
        port = 9899
        BUFFER_SIZE = 1024
        global tcpClientA
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
    if msg == 'pause':
        print("광고 중단 메시지를 받았습니당")
        newThread.setStop()
        # 쓰레드 자체를 실제로 종료시킴! 강제 종료도 아님!
        # CameraWork 객체의 onOff 가 False 니까 반복문이 멈추고 run() 이 끝나기 때문
    if msg == 'exit':
        print("빠이욤")
        break
tcpClientA.close()


class CameraWork(Thread):
    def __init__(self, tcpClientA):
        Thread.__init__(self)
        self.clientSocket = tcpClientA
        self.FILE_NAME = ('image.jpg')
        self.onOff = True


self.camera = PiCamera()


def setStop(self):
    self.onOff = False


def run(self):
    while True:


# 찍고 보내고 삭제하는데 걸리는 시간을 적절히 조절해야함
# 서버에서 이미지 도착 안했는데 분석 돌릴 가능성 있음
# FILE_NAME = ('image.jpg' % i) 얘는 주석안풀어줄거임.

print("찍습니다")
self.captureImage(self.FILE_NAME)
time.sleep(2)
print("보내기 전이요")
self.sendImage(self.FILE_NAME)
print("send이미지 끝")
time.sleep(1)
print("삭제 전이요")
os.remove(r'image.jpg')

if not self.onOff:
    break


def captureImage(self, FILE_NAME):
    time.sleep(5)
    self.camera.capture('/home/pi/sang/' + FILE_NAME)


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
        server_msg = self.clientSocket.recv(BUFF_SIZE)
        print('server : ' + server_msg.decode())

    except Exception as e:
        sys.exit()


if __name__ == '__main__':
    clientThread = ClientThread()
    clientThread.start()

