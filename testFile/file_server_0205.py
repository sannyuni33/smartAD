"""from socket import *
import struct
import clova3
from DB_interface_test import DB_interface

HOST = "192.168.101.125"
PORT = 9068

ADDR = (HOST, PORT)
BUFF_SIZE = 1024


def recvcamera(FILE_NAME):
    FILE_LEN = 0

    FILE_SIZE = clientSocket.recv(8)
    FILE_SIZE = struct.unpack('L', FILE_SIZE)[0]

    f = open(FILE_NAME, 'wb')

    while True:
        client_file = clientSocket.recv(BUFF_SIZE)
        # print(client_file)

        if not client_file:
            break

        f.write(client_file)
        FILE_LEN += len(client_file)

        if FILE_LEN == int(FILE_SIZE):
            break


    f.close()

    print('client : ' + FILE_NAME + ' file transfer')
    server_msg = FILE_NAME + ' received complete'
    clientSocket.send(server_msg.encode())

    #result = clova3.recog_test(FILE_NAME)
    #AD = db.decide_AD(result[0], result[1])
    #print(AD)


# server_msg = bytes(server_msg, encoding='utf-8')
# clientSocket.send(server_msg)

if __name__ == "__main__":

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(ADDR)
    serverSocket.listen(5)
    #db = DB_interface()

    clientSocket, addr = serverSocket.accept()
    print('연결되었습니다')

    for i in range(2):
        FILE_NAME = ('client%s.jpg' % i)
        recvcamera(FILE_NAME)


clientSocket.close()

from socket import*
import struct
import clova3
from DB_interface_test import DB_interface

HOST ="192.168.143.239"
PORT = 9025

ADDR = (HOST, PORT)
BUFF_SIZE = 1024
FILE_NAME = 'client.jpg'
FILE_LEN = 0

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(ADDR)
serverSocket.listen(5)
db = DB_interface()

clientSocket, addr = serverSocket.accept()
print('연결되었습니다')

FILE_SIZE = clientSocket.recv(8)
FILE_SIZE = struct.unpack('L', FILE_SIZE)[0]

f = open(FILE_NAME+'i'%i, 'wb')

while True:
    client_file = clientSocket.recv(BUFF_SIZE)
    # print(client_file)

    if not client_file:
        break

    f.write(client_file)
    FILE_LEN += len(client_file)

    if FILE_LEN == int(FILE_SIZE):
        break

f.close()
print('client : ' + FILE_NAME + ' file transfer')

server_msg = FILE_NAME + ' received complete'
# server_msg = bytes(server_msg, encoding='utf-8')
# clientSocket.send(server_msg)
clientSocket.send(server_msg.encode())
result = clova3.recog_test(FILE_NAME)
AD = db.decide_AD(result[0], result[1])
print(AD)
clientSocket.close()"""
from socket import *
import struct
import clova3
from DB_interface_test import DB_interface

HOST = "172.30.1.27"
PORT = 9988

ADDR = (HOST, PORT)
BUFF_SIZE = 1024
FILE_LEN=0

def recvcamera(FILE_NAME):
    FILE_LEN = 0
    FILE_SIZE = clientSocket.recv(8)
    FILE_SIZE = struct.unpack('L', FILE_SIZE)[0]

    f = open(FILE_NAME, 'wb')

    while True:

        client_file = clientSocket.recv(BUFF_SIZE)
        # print(client_file)

        if not client_file:
            break

        f.write(client_file)
        FILE_LEN += len(client_file)

        if FILE_LEN == int(FILE_SIZE):
            break

    f.close()  # 여기까지는 이미지 파일을 수신인데, 카메라 핸들러가 해주는게 맞고.

    print('client : ' + FILE_NAME + ' file transfer')
    server_msg = FILE_NAME + ' received complete'
    clientSocket.send(server_msg.encode())

    result = clova3.recog_test(FILE_NAME)  # 여기서 하나의 메소드로 끝내버리는게 맞는건지.
    AD = db.decide_AD(result[0], result[1])
    print(AD)


# server_msg = bytes(server_msg, encoding='utf-8')
# clientSocket.send(server_msg)

if __name__ == "__main__":

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(ADDR)
    serverSocket.listen(5)
    db = DB_interface()

    clientSocket, addr = serverSocket.accept()
    print('연결되었습니다')

    for i in range(2):
        FILE_NAME = ('client%s.jpg' % i)
        recvcamera(FILE_NAME)

    clientSocket.close()



