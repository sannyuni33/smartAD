import sys, datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSplitter, QVBoxLayout, \
    QDialog, QPushButton, QApplication, QTextEdit, \
    QLineEdit
from socket import *
from threading import Thread
import struct
import cv2
import requests
import json
import queue
from PyQt5 import uic
from DB_interface_test import DB_interface

# 클라이언트 연결
conn = None
camConn = None
disConn = None
BUFF_SIZE = 2048

# 얼굴분석 워커 쓰레드가 리턴하는 값을 메인 쓰레드가 받아보기 위해 큐 사용
que = queue.Queue()

# 서버 GUI 구성 ui 파일
MainUI = 'serverfinal.ui'

# NAVER API 연결
client_id = "38hNSdXWRhGUHxMpaRoV"
client_secret = "5YF8TJC9YQ"
url = "https://openapi.naver.com/v1/vision/face"
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}

recog_result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
genderAge = None
ADname = None


def faceAnalyse(FILE_NAME):
    # 카메라 클라이언트가 전송한 이미지에 대해 얼굴분석 수행
    files = {'image': open(FILE_NAME, 'rb')}
    # 요 부분에 히스토그램이 들어와야겠네
    response = requests.post(url, files=files, headers=headers)
    rescode = response.status_code

    if rescode == 200:
        pass
        # print(response.text)
    else:
        print("Error Code:" + rescode)

    json_data = json.loads(response.text)
    img = cv2.imread(FILE_NAME, cv2.IMREAD_COLOR)

    for i in json_data['faces']:
        x, y, w, h = i['roi'].values()
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
        gender = i['gender']['value']
        age = i['age']['value']
        age1, age2 = age.split('~')
        final_age = (int(age1) + int(age2)) / 2

        result = """
                    성별: %s
                    나이: %s
                    """ % (
            gender,
            age
        )
        print(result)
        cv2.putText(img, result, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        if gender == 'male':
            if 10 <= final_age < 20:
                recog_result[0] += 1
            elif 20 <= final_age < 30:
                recog_result[1] += 1
            elif 30 <= final_age < 40:
                recog_result[2] += 1
            elif 40 <= final_age < 50:
                recog_result[3] += 1
            elif 50 <= final_age < 60:
                recog_result[4] += 1
            else:
                recog_result[5] += 1
        else:
            if 10 <= final_age < 20:
                recog_result[6] += 1
            elif 20 <= final_age < 30:
                recog_result[7] += 1
            elif 30 <= final_age < 40:
                recog_result[8] += 1
            elif 40 <= final_age < 50:
                recog_result[9] += 1
            elif 50 <= final_age < 60:
                recog_result[10] += 1
            else:
                recog_result[11] += 1

    if max(recog_result) == 0:
        print("인식실패띠 ㅜ")
        return -1, -1
    else:
        max_index = recog_result.index(max(recog_result))

    if max_index == 0:
        genderAge = ('male', 10)
    elif max_index == 1:
        genderAge = ('male', 20)
    elif max_index == 2:
        genderAge = ('male', 30)
    elif max_index == 3:
        genderAge = ('male', 40)
    elif max_index == 4:
        genderAge = ('male', 50)
    elif max_index == 5:
        genderAge = ('male', 60)
    elif max_index == 6:
        genderAge = ('female', 10)
    elif max_index == 7:
        genderAge = ('female', 20)
    elif max_index == 8:
        genderAge = ('female', 30)
    elif max_index == 9:
        genderAge = ('female', 40)
    elif max_index == 10:
        genderAge = ('female', 50)
    elif max_index == 11:
        genderAge = ('female', 60)

    print("최종 결과: ")
    print(genderAge)

    return genderAge


class Window(QDialog):
    # 서버 관리자용 GUI
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(MainUI, self)
        self.setWindowTitle("서버 GUI")
        self.label.setStyleSheet('image:url(sexysang.jpg)')
        self.label_2.setStyleSheet('image:url(hijoo.jpg)')

        self.pushButton.clicked.connect(self.startAD)
        self.pushButton_2.clicked.connect(self.pauseAD)
        self.pushButton_3.clicked.connect(self.showStat)
        self.pushButton_4.clicked.connect(self.changeAD)
        self.pushButton_5.clicked.connect(self.changeAD) # 여기에서 정상적으로 종료시키려면 어떻게 해야할까요

    def startAD(self):
        print("시작")
        self.send("start")
        self.textBrowser.append("시작")

    def pauseAD(self):
        print("일시정지")
        self.send("pause")
        self.textBrowser.append("일시정지")

    def showStat(self):
        print("통계조회")
        self.textBrowser.append("통계조회")

    def closeAD(self):
        print("종료")
        self.send("exit")
        self.textBrowser.append("종료")

    def changeAD(self):
        print("광고 변경")
        self.textBrowser.append("광고 변경")

    def send(self, msg):
        text = msg
        # font = self.chat.font()
        # font.setPointSize(13)
        # self.chat.setFont(font)
        # textFormatted = '{:>80}'.format(text)
        # self.chat.append(textFormatted)
        # 여기서 카메라로 보낼 메시지 광고판으로 보낼 메시지
        # 구분 잘해야 함
        global camConn
        global disConn
        camConn.send(text.encode("utf-8"))
        disConn.send(text.encode("utf-8"))
        # self.chatTextField.setText("")


class ServerThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        TCP_IP = '192.168.100.38'
        TCP_PORT = 9988
        # BUFFER_SIZE = 2048
        tcpServer = socket(AF_INET, SOCK_STREAM)
        tcpServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        tcpServer.bind((TCP_IP, TCP_PORT))
        tcpServer.listen(2)
        threads = []

        while True:
            print("Multi Threaded Python server : Waiting for connections from TCP clients...")
            global conn
            global camConn
            global disConn
            conn, (ip, port) = tcpServer.accept()
            print(conn, ip, port)

            if ip == '192.168.100.38':
                camConn = conn
                camthread = CameraThread(ip, port, window)
                camthread.start()
                threads.append(camthread)
            if ip == '192.168.141.100':
                disConn = conn
                disthread = DisplayThread(ip, port, window)
                disthread.start()
                threads.append(disthread)

        for t in threads:
            t.join()



class CameraThread(Thread):
    def __init__(self, ip, port, window):
        Thread.__init__(self)
        self.window = window
        self.ip = ip
        self.port = port
        print("[+] 카메라 클라이언트와 연결되었습니다! " + ip + ':' + str(port))

    def run(self):
        while True:
            global camConn
            data = camConn.recv(BUFF_SIZE)
            window.textBrowser.append(data.decode('utf-8'))
            print(data.decode('utf-8'))
            # FILE_NAME = ('image.jpg')  # 나중엔 파일 이름 다 다른걸로 저장
            # self.recvImage(FILE_NAME)
            faceThread = Thread(target=lambda q, arg1: q.put(faceAnalyse(arg1)), args=(que, '1-2.jpg'))  # 나중엔 self.FILE_NAME
            faceThread.setDaemon(True)
            faceThread.start()
            faceThread.join()
            today = datetime.datetime.today()
            global genderAge
            genderAge = que.get()
            print("서버가 받은 결과는: ", genderAge)
            global ADname

            if genderAge == (-1, -1):
                majority = DB.findMajority(today.hour)
                ADname = DB.decideID(majority[0], majority[1])
            else:
                ADname = DB.decideID(genderAge[0], genderAge[1])
                self.insert_result(genderAge, today.year+"."+today.month+"."+today.day,
                                   today.hour, ADname)

            print("광고가 멀로 정해졌냐면: ", ADname)

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

    def insert_result(self, genderAge, date, time, ADname):
        # db.인식성공(성별, 연령대, 날짜, 시간, 광고 ID 이렇게 집어넣음 됨.)
        # 인식성공하고 광고 결정되면 통계에 집어 넣어주는 메소드를 서버에 만들어야 될 듯.
        DB.insertRecogResult(genderAge[0], genderAge[1], date, time, ADname)


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
            data = disConn.recv(BUFF_SIZE)
            window.textBrowser.append(data.decode('utf-8'))
            print(data.decode('utf-8'))

    def sendID(self, ADname):
        print("이거 열심히 만들어보......는걸 프로토타입 발표 후에 하면 되겠네", ADname)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    serverThread = ServerThread(window)
    serverThread.start()
    DB = DB_interface()
    window.exec()
    sys.exit(app.exec_())