import sys, time
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSplitter, QVBoxLayout, \
    QDialog, QPushButton, QApplication, QTextEdit, \
    QLineEdit
import socket
from threading import Thread
#from clova3 import FaceRecog
import struct
from PyQt5 import uic

conn = None
camConn = None
disConn = None
BUFF_SIZE = 2048
MainUI = 'serverfinal.ui'


class Window(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(MainUI, self)
        self.setWindowTitle("서버 GUI")
        self.label.setStyleSheet('image:url(ready.png)')
        self.label_2.setStyleSheet('image:url(ready2.png)')

        self.pushButton.clicked.connect(self.startAD)
        self.pushButton_3.clicked.connect(self.pauseAD)
        self.pushButton_2.clicked.connect(self.closeAD)
        self.pushButton_4.clicked.connect(self.changeAD)

    def startAD(self):
        print("시작")
        self.textBrowser.append("시작")
    def pauseAD(self):
        print("일시정지")
        self.textBrowser.append("일시정지")
    def closeAD(self):
        print("종료")
        self.textBrowser.append("종료")
    def changeAD(self):
        print("광고 변경")
        self.textBrowser.append("광고 변경")


    """def send(self):
        text = self.chatTextField.text()
        font = self.chat.font()
        font.setPointSize(13)
        self.chat.setFont(font)
        textFormatted = '{:>80}'.format(text)
        self.chat.append(textFormatted)
        # 여기서 카메라로 보낼 메시지 광고판으로 보낼 메시지
        # 구분 잘해야 함
        global camConn
        global disConn
        camConn.send(text.encode("utf-8"))
        disConn.send(text.encode("utf-8"))
        self.chatTextField.setText("")

    """
class ServerThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        TCP_IP = '172.30.98.72'
        TCP_PORT = 9966
        BUFFER_SIZE = 2048
        tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpServer.bind((TCP_IP, TCP_PORT))
        threads = []

        tcpServer.listen(4)
        while True:
            print("Multi Threaded Python server : Waiting for connections from TCP clients...")
            global conn
            global camConn
            global disConn
            conn, (ip, port) = tcpServer.accept()
            if ip == '172.30.98.71':
                camConn = conn
                camthread = CameraThread(ip, port, window)
                print("스레드 생성전")
                camthread.start()
                threads.append(camthread)
            if ip == '172.30.98.72':
                disConn = conn
                disthread = DisplayThread(ip, port, window)
                print("디스레드 생성 전 ")
                disthread.start()
                threads.append(disthread)

        for t in threads:
            t.join()

    def insert_result(self):
        # db.인식성공(성별, 연령대, 날짜, 시간, 광고 ID 이렇게 집어넣음 됨.)
        # 인식성공하고 광고 결정되면 통계에 집어 넣어주는 메소드를 서버에 만들어야 될 듯.
        return


class CameraThread(Thread):
    def __init__(self, ip, port, window):
        Thread.__init__(self)
        self.window = window
        self.ip = ip
        self.port = port
        print("[+] 카메라 클라이언트와 연결되었습니다! " + ip + ':' + str(port))

    def run(self):
        while True:
            # (conn, (self.ip,self.port)) = serverThread.tcpServer.accept()
            global camConn
            data = camConn.recv(2048)
            window.chat.append(data.decode('utf-8'))
            print(data.decode('utf-8'))
            # FILE_NAME = ('image.jpg')  # 나중엔 파일 이름 다 다른걸로 저장
            # self.recvImage(FILE_NAME)
            facethread = FaceRecog('girl3.jpg')  # 나중엔 self.FILE_NAME
            facethread.setDaemon(True)
            facethread.start()
            print(facethread.genderAge)

    def recvImage(FILE_NAME):
        global camConn
        FILE_LEN = 0
        FILE_SIZE = camConn.recv(8)
        FILE_SIZE = struct.unpack('L', FILE_SIZE)[0]

        f = open(FILE_NAME, 'wb')

        while True:
            client_file = camConn.recv(BUFF_SIZE)
            # print(client_file)

            if not client_file:
                break

            f.write(client_file)
            FILE_LEN += len(client_file)

            if FILE_LEN == int(FILE_SIZE):
                break

        f.close()  # 여기까지 이미지 파일 수신인데, 카메라 핸들러가 해주는게 맞고.

        print('client : ' + FILE_NAME + ' file transfer')
        server_msg = FILE_NAME + ' received complete'
        camConn.send(server_msg.encode('utf-8'))


class DisplayThread(Thread):
    def __init__(self, ip, port, window):
        Thread.__init__(self)
        self.window = window
        self.ip = ip
        self.port = port
        print("[+] 광고판 클라이언트와 연결되었습니다! " + ip + ':' + str(port))

    def run(self):
        while True:
            global disConn
            data = disConn.recv(2048)
            window.chat.append(data.decode('utf-8'))
            print(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    serverThread = ServerThread(window)
    serverThread.start()
    window.exec()

    sys.exit(app.exec_())