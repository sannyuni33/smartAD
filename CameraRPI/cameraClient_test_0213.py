import sys
import os
import struct
import time
import socket
from threading import Thread
import datetime
#from picamera import PiCamera

tcpClientA = None


class ClientThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        host = '172.30.1.27'
        port = 9988
        BUFFER_SIZE = 2048
        global tcpClientA
        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpClientA.connect((host, port))

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
        self.FILE_NAME = 'image.jpg'
        self.onOff = True

    def setStop(self):
        self.onOff = False

    def run(self):
        while True:
            # time.sleep(1)
            # print('찍고')
            # time.sleep(1)
            # print('보내고')
            # msg = '이미지파일 수신'
            # self.clientSocket.send(msg.encode('utf-8'))
            # time.sleep(1)
            # print('삭제하고')

            # 찍고 보내고 삭제하는데 걸리는 시간을 적절히 조절해야함
            # 서버에서 이미지 도착 안했는데 분석 돌릴 가능성 있음
            # FILE_NAME = ('image.jpg' % i) 얘는 주석안풀어줄거임.
            self.captureImage(self.FILE_NAME)
            self.sendImage(self.FILE_NAME)
            os.remove(r'image.jpg')

            if not self.onOff:
                break

    def captureImage(self, FILE_NAME):
        camera = PiCamera()
        camera.start_preview()
        time.sleep(5)
        camera.capture('/home/pi/sang/'+FILE_NAME)
        camera.stop_preview()

    def sendImage(self, FILE_NAME):
        FILE_SIZE = os.path.getsize(FILE_NAME)
        FILE_SIZE = struct.pack('L', FILE_SIZE)
        try:
            n = 0
            f = open('/home/pi/sang/' + FILE_NAME, 'rb')
            i = f.read(self.clientSocket.BUFF_SIZE)
            self.clientSocket.send(FILE_SIZE)
            n += 1
            while i:
                self.clientSocket.send(i)
                i = f.read(self.clientSocket.BUFF_SIZE)
            f.close()

            print('(check) ' + FILE_NAME + ' transfer complete')
            server_msg = self.clientSocket.recv(self.clientSocket.BUFF_SIZE)
            print('server : ' + server_msg.decode())

        except Exception as e:
            sys.exit()


if __name__ == '__main__':
    clientThread = ClientThread()
    clientThread.start()
