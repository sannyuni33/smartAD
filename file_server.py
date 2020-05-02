from socket import*
import struct
import clova3
from DB_interface_test import DB_interface

HOST ="172.30.1.27"
PORT = 9999

ADDR = (HOST, PORT)
BUFF_SIZE = 1024
FILE_NAME = 'client454545.jpg'
FILE_LEN = 0

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(ADDR)
serverSocket.listen(5)
db = DB_interface()

clientSocket, addr = serverSocket.accept()
print('연결되었습니다')
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
# server_msg = bytes(server_msg, encoding='utf-8')
# clientSocket.send(server_msg)
clientSocket.send(server_msg.encode())
result = clova3.recog_test(FILE_NAME)
AD = db.decide_AD(result[0], result[1])
print(AD)
clientSocket.close()