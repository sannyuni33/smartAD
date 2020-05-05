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
from PyQt5.QtGui import *
from DB_interface_test import DB_interface

# 클라이언트 연결
conn = None
camConn = None
disConn = None
BUFF_SIZE = 1024

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

    # 히스토그램 평활화
    src = cv2.imread(FILE_NAME)

    # hsv 컬러 형태로 변형합니다.
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    # h, s, v로 컬러 영상을 분리 합니다.
    h, s, v = cv2.split(hsv)
    # v값을 히스토그램 평활화를 합니다.
    equalizedV = cv2.equalizeHist(v)
    # h,s,equalizedV를 합쳐서 새로운 hsv 이미지를 만듭니다.
    hsv2 = cv2.merge([h, s, equalizedV])

    # 마지막으로 hsv2를 다시 BGR 형태로 변경합니다.
    hsv3 = cv2.cvtColor(hsv2, cv2.COLOR_HSV2BGR)
    cv2.imwrite(FILE_NAME,hsv3)
    files = {'image': open(FILE_NAME, 'rb')}

    response = requests.post(url, files=files, headers=headers)
    rescode = response.status_code

    # 요 부분에 히스토그램이 들어와야겠네


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

        result = """%s, %s""" % (gender, str(age))
        print(result)
        # putText 할 때 이미지? 얼굴? 크기에 따라 폰트 크기를 다르게 한다면 좋을 것 같다!
        cv2.putText(img, result, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (255, 255, 255), 1, cv2.LINE_AA)

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

    # cv2.imshow('image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    window.label.setStyleSheet('image:url('+FILE_NAME+')')

    # window.qPixmapVar_1.load(FILE_NAME)
    # window.label.setPixmap(window.qPixmapVar_1)

    if max(recog_result) == 0:
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

    return genderAge


def send(msg):
    text = msg  # 이거 없애고 camConn.send(msg.encode()) 해도 될듯
    # 여기서 카메라로 보낼 메시지 광고판으로 보낼 메시지
    # 구분 잘해야 함
    global camConn
    global disConn
    camConn.send(text.encode("utf-8"))
    disConn.send(text.encode("utf-8"))


class Window(QDialog):
    # 서버 관리자용 GUI
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(MainUI, self)
        self.setWindowTitle("서버 GUI")
        # self.qPixmapVar_1 = QPixmap()
        # self.qPixmapVar_2 = QPixmap()
        # self.qPixmapVar_1.load('sexysang.jpg')
        # self.qPixmapVar_2.load('hijoo.jpg')
        # self.label.setPixmap(self.qPixmapVar_1)
        # self.label_2.setPixmap(self.qPixmapVar_2)

        self.label.setStyleSheet('image:url(ready.png)')
        self.label_2.setStyleSheet('image:url(ready.png)')

        self.pushButton.clicked.connect(self.startAD)
        self.pushButton_2.clicked.connect(self.pauseAD)
        self.pushButton_3.clicked.connect(self.showStat)
        self.pushButton_4.clicked.connect(self.changeAD)
        self.pushButton_5.clicked.connect(self.closeAD)

    def startAD(self):
        send("start")
        self.textBrowser.append("시작")

    def pauseAD(self):
        send("pause")
        self.textBrowser.append("일시정지")

    def showStat(self):
        self.textBrowser.append("통계조회")

    def closeAD(self):
        send("exit")
        self.textBrowser.append("종료")

    def changeAD(self):
        self.textBrowser.append("광고 변경")


class ServerThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        TCP_IP = '172.30.98.130'
        TCP_PORT = 9988
        tcpServer = socket(AF_INET, SOCK_STREAM)
        tcpServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        tcpServer.bind((TCP_IP, TCP_PORT))
        tcpServer.listen(2)
        threads = []

        while True:
            print("Multi Threaded Python server : Waiting for connections from TCP clients...")
            window.textBrowser.append("클라이언트 접속 대기중...")
            global conn
            global camConn
            global disConn
            conn, (ip, port) = tcpServer.accept()

            if ip == '172.30.98.130':
                camConn = conn
                camthread = CameraThread(ip, port, window)
                camthread.start()
                threads.append(camthread)
            if ip == '172.30.1.27':
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
        window.textBrowser.append("[+] 카메라 클라이언트와 연결되었습니다! " + ip + ':' + str(port))

    def run(self):
        while True:
            global camConn
            # data = camConn.recv(BUFF_SIZE)
            # window.textBrowser.append(data.decode('utf-8'))
            # print(data.decode('utf-8'))
            img_path = '../imgFile/'
            count = 0

            FILE_NAME = (img_path + str(count) + '.jpg')

            self.recvImage(FILE_NAME)
            window.textBrowser.append(FILE_NAME+" 이미지 수신 완료")
            faceThread = Thread(target=lambda q, arg1: q.put(faceAnalyse(arg1)), args=(que, FILE_NAME))
            faceThread.setDaemon(True)
            faceThread.start()
            faceThread.join()
            today = datetime.datetime.today()
            global genderAge
            genderAge = que.get()
            print("서버가 받은 결과는: ", genderAge)
            guimsg = "성별, 연령대: "+genderAge[0]+str(genderAge[1])
            window.textBrowser.append(guimsg)
            window.label_2.setStyleSheet('image:url(f20.jpg)')

            global ADname

            if genderAge == (-1, -1):
                window.textBrowser.append("얼굴이 인식되지 않습니다. 통계기반의 광고를 출력합니다.")
                majority = DB.findMajority(today.hour)
                ADname = DB.decideID(majority[0], majority[1])
            else:
                ADname = DB.decideID(genderAge[0], genderAge[1])
                self.insert_result(genderAge, str(today.year) + "." + str(today.month) + "." + str(today.day),
                                   str(today.hour), ADname)

            print("광고가 멀로 정해졌냐면: ", ADname)
            window.textBrowser.append("광고 ID: " + ADname)
            window.label_2.setStyleSheet('image:url(m20.jpg)')
            # window.qPixmapVar_2.load('f20.jpg')
            # window.label_2.setPixmap(window.qPixmapVar_2)

            count += 1

    def recvImage(self, FILE_NAME):
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
        window.textBrowser.append("[+] 광고판 클라이언트와 연결되었습니다! " + ip + ':' + str(port))

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