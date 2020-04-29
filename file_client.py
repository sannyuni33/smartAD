# 카메라와 연결되있는 라즈베리파이에 심어지는 실행파일
from time import sleep
from socket import *
import os
import sys
import struct
import datetime
#from picamera import PiCamera

HOST = "192.168.101.125"
PORT = 9069
ADDR = (HOST, PORT)
BUFF_SIZE = 1024


"""def picam2():
    camera = PiCamera()
    camera.start_preview()
    sleep(5)
    camera.capture('/home/pi/sang/'+FILE_NAME)
    camera.stop_preview()
"""

def sendImage(FILE_NAME):
    FILE_SIZE = os.path.getsize(FILE_NAME)
    FILE_SIZE = struct.pack('L', FILE_SIZE)
    while True:
        try:
            n = 0
            f = open('/home/pi/sang/' + FILE_NAME, 'rb')
            i = f.read(BUFF_SIZE)
            clientSocket.send(FILE_SIZE)
            n += 1
            while i:
                clientSocket.send(i)
                i = f.read(BUFF_SIZE)
            f.close()

            print('(check) ' + FILE_NAME + ' transfer complete')
            server_msg = clientSocket.recv(BUFF_SIZE)
            print('server : ' + server_msg.decode())

        except Exception as e:
            sys.exit()



if __name__ == "__main__":
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(ADDR)

    for i in range(5):
        FILE_NAME = ('image%s.jpg'%i)
        #picam2(FILE_NAME)

        sendImage(FILE_NAME)
        #os.remove(r'image.jpg')

    clientSocket.close()
    sys.exit()
    print('file transfer complete')
