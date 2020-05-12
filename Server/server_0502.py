import sys
import datetime

import matplotlib
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
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTabWidget
from PyQt5.QtWidgets import *
from DB_interface_test import DB_interface
from matplotlib import pyplot as plt
from matplotlib import font_manager, rc
import numpy as np
from time import *

# 클라이언트 연결
conn = None
camConn = None
disConn = None
BUFF_SIZE = 1024

# 얼굴분석 워커 쓰레드가 리턴하는 값을 메인 쓰레드가 받아보기 위해 큐 사용
que = queue.Queue()

# 서버 GUI 구성 ui 파일
MainUI = 'serverUi.ui'
# 광고변경 ui 파일
changeUI = 'chAD.ui'

# NAVER API 연결
client_id = "38hNSdXWRhGUHxMpaRoV"
client_secret = "5YF8TJC9YQ"
url = "https://openapi.naver.com/v1/vision/face"
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}

# matplotlib 한글 출력 설정
font_name = font_manager.FontProperties(fname="C:/Windows/Fonts/08seoulnamsanl.ttf").get_name()
rc('font', family=font_name)

genderAge = None
ADtarget = None


def faceAnalyse(FILE_NAME):
    # 카메라 클라이언트가 전송한 이미지에 대해 얼굴분석 수행
    recog_result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # 히스토그램 평활화
    # src = cv2.imread(FILE_NAME)
    #
    # # hsv 컬러 형태로 변형합니다.
    # hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    # # h, s, v로 컬러 영상을 분리 합니다.
    # h, s, v = cv2.split(hsv)
    # # v값을 히스토그램 평활화를 합니다.
    # equalizedV = cv2.equalizeHist(v)
    # # h,s,equalizedV를 합쳐서 새로운 hsv 이미지를 만듭니다.
    # hsv2 = cv2.merge([h, s, equalizedV])
    #
    # # 마지막으로 hsv2를 다시 BGR 형태로 변경합니다.
    # hsv3 = cv2.cvtColor(hsv2, cv2.COLOR_HSV2BGR)
    # cv2.imwrite(FILE_NAME, hsv3)
    files = {'image': open(FILE_NAME, 'rb')}

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
    cv2.imwrite(FILE_NAME, img)
    window.label.setStyleSheet('image:url(' + FILE_NAME + ')')

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


# 서버 관리자용 GUI
class Window(QMainWindow, ):
    def __init__(self):
        super().__init__()

        # 초기화면 세팅
        uic.loadUi(MainUI, self)
        self.setWindowTitle("서버 GUI")

        self.label.setStyleSheet('image:url(../imgFile/ready.png)')
        self.label_2.setStyleSheet('image:url(../imgFile/ready.png)')

        self.pushButton.clicked.connect(self.startAD)
        self.pushButton_2.clicked.connect(self.pauseAD)
        self.pushButton_3.clicked.connect(self.showTimeStat)
        self.pushButton_4.clicked.connect(self.changeAD)
        self.pushButton_5.clicked.connect(self.closeAD)
        self.pushButton_6.clicked.connect(self.showAdStat)

    def startAD(self):
        send("start")
        self.textBrowser.append("광고를 시작합니다!")

    def pauseAD(self):
        send("pause")
        self.textBrowser.append("광고를 일시 중단합니다!")

    def showTimeStat(self):
        self.textBrowser.append("시간대별 인식통계를 조회합니다.")
        res = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        res_cnt = DB.lookUpTimeStat(datetime.datetime.today().hour)
        for row in res_cnt:
            if row[0] == 'male' and row[1] == 10:
                res[0] += row[2]
            elif row[0] == 'male' and row[1] == 20:
                res[1] += row[2]
            elif row[0] == 'male' and row[1] == 30:
                res[2] += row[2]
            elif row[0] == 'male' and row[1] == 40:
                res[3] += row[2]
            elif row[0] == 'male' and row[1] == 50:
                res[4] += row[2]
            elif row[0] == 'male' and row[1] == 60:
                res[5] += row[2]
            elif row[0] == 'female' and row[1] == 10:
                res[6] += row[2]
            elif row[0] == 'female' and row[1] == 20:
                res[7] += row[2]
            elif row[0] == 'female' and row[1] == 30:
                res[8] += row[2]
            elif row[0] == 'female' and row[1] == 40:
                res[9] += row[2]
            elif row[0] == 'female' and row[1] == 50:
                res[10] += row[2]
            elif row[0] == 'female' and row[1] == 60:
                res[11] += row[2]
        label = ['male\n10', 'male\n20', 'male\n30', 'male\n40',
                 'male\n50', 'male\n60', 'female\n10', 'female\n20',
                 'female\n30', 'female\n40', 'female\n50', 'female\n60']

        bar_width = 0.35
        opacity = 0.5
        font = {'size': 12}
        matplotlib.rc('font', **font)
        plt.bar(label, res, bar_width, bottom=2,
                tick_label=label, align='center', label='A',
                alpha=opacity, color='b', edgecolor='black', linewidth=1.2)

        plt.title(str(datetime.datetime.today().hour) + "시 인식결과통계")
        plt.xlim(-0.5, 12)
        plt.ylabel('인식 횟수')

        plt.show()

    def showAdStat(self):
        self.textBrowser.append("광고별 관심지수통계를 조회합니다.")
        tmp_res = DB.lookUpADStat()
        X_label = []
        Y_label = []
        for i in tmp_res:
            X_label.insert(0, i[0])
            Y_label.insert(0, i[1])
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)

        ypos = np.arange(10)
        rects = plt.barh(ypos, Y_label, align='center', height=0.5)
        plt.yticks(ypos, X_label)

        plt.title('관심 지수 TOP 10 광고')
        plt.xlabel('관심 지수')
        plt.show()

    def closeAD(self):
        send("exit")
        self.textBrowser.append("시스템을 종료합니다.")
        time.sleep(3)

    def changeAD(self):
        # ch window를 인자로 받아서 실행시킨다.
        cd = ch_Dialog(self)
        cd.exec()
        self.textBrowser.append("광고 변경을 시작합니다")
        id = cd.ad_ID
        # 10대 여자
        if id == 'f10':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/f10.jpeg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'f11':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/f11.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        # 20대 여자
        if id == 'f20':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/f20.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'f21':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/f21.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        # 30대 여자
        if id == 'f30':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/f30.jpeg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'f31':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/f31.jpeg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        # 40대 여자
        if id == 'f40':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/f40.jpeg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'f41':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/f41.jpeg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        # 50대 여자
        if id == 'f50':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/f50.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'f51':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/f51.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        # 60대 여자
        if id == 'f60':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/f60.jpeg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'f61':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/f61.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        # 10대 남자
        if id == 'm10':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/m10.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'm11':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/m11.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        # 20대 남자
        if id == 'm20':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/m20.jpeg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'm21':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/m21.png)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        # 30대 남자
        if id == 'm30':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/m30.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'm31':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/m31.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")

        # 40대 남자
        if id == 'm40':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/m40.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'm41':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/m41.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        # 50대 남자
        if id == 'm50':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/m50.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'm51':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/m51.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        # 60대 남자
        if id == 'm60':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/m60.jpeg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'm61':
            self.label_2.setStyleSheet('image:url(../imgFile/chAD/m61.jpeg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")


# 광고변경 GUI
class ch_Dialog(QDialog):
    def __init__(self, parent):
        self.ad_ID = None
        super(ch_Dialog, self).__init__(parent)
        uic.loadUi(changeUI, self)
        self.retranslateUi()
        self.show()
        self.pushButton.clicked.connect(self.f10)
        self.pushButton_2.clicked.connect(self.f11)
        self.pushButton_3.clicked.connect(self.f20)
        self.pushButton_4.clicked.connect(self.f21)
        self.pushButton_5.clicked.connect(self.f30)
        self.pushButton_6.clicked.connect(self.f31)

        self.pushButton_7.clicked.connect(self.f40)
        self.pushButton_8.clicked.connect(self.f41)
        self.pushButton_9.clicked.connect(self.f50)
        self.pushButton_10.clicked.connect(self.f51)
        self.pushButton_11.clicked.connect(self.f60)
        self.pushButton_12.clicked.connect(self.f61)

        self.pushButton_13.clicked.connect(self.m10)
        self.pushButton_14.clicked.connect(self.m11)
        self.pushButton_15.clicked.connect(self.m20)
        self.pushButton_16.clicked.connect(self.m21)
        self.pushButton_17.clicked.connect(self.m30)
        self.pushButton_18.clicked.connect(self.m31)

        self.pushButton_19.clicked.connect(self.m40)
        self.pushButton_20.clicked.connect(self.m41)
        self.pushButton_21.clicked.connect(self.m50)
        self.pushButton_22.clicked.connect(self.m51)
        self.pushButton_23.clicked.connect(self.m60)
        self.pushButton_24.clicked.connect(self.m61)

    def retranslateUi(self):
        # 이 함수는 탭마다 광고 이미지 넣어주는 함수
        _translate = QApplication.translate
        # 먼저 tab 이름 설정 fm10 m10...
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Fm10"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Fm20"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Fm30"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Fm40"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Fm50"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("MainWindow", "Fm60"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _translate("MainWindow", "M10"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), _translate("MainWindow", "M20"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_9), _translate("MainWindow", "M30"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_10), _translate("MainWindow", "M40"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_11), _translate("MainWindow", "M50"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_12), _translate("MainWindow", "M60"))

        # 이부분에 변경할 광고 이미지 추가해주세용
        self.pushButton.setStyleSheet('image:url(../imgFile/chAD/f10.jpeg.);border:0px;')
        self.pushButton_2.setStyleSheet('image:url(../imgFile/chAD/f11.jpg.);border:0px;')
        self.pushButton_3.setStyleSheet('image:url(../imgFile/chAD/f20.jpg.);border:0px;')
        self.pushButton_4.setStyleSheet('image:url(../imgFile/chAD/f21.jpg.);border:0px;')
        self.pushButton_5.setStyleSheet('image:url(../imgFile/chAD/f30.jpeg.);border:0px;')
        self.pushButton_6.setStyleSheet('image:url(../imgFile/chAD/f31.jpeg.);border:0px;')

        self.pushButton_7.setStyleSheet('image:url(../imgFile/chAD/f40.jpeg.);border:0px;')
        self.pushButton_8.setStyleSheet('image:url(../imgFile/chAD/f41.jpeg.);border:0px;')
        self.pushButton_9.setStyleSheet('image:url(../imgFile/chAD/f50.jpg.);border:0px;')
        self.pushButton_10.setStyleSheet('image:url(../imgFile/chAD/f51.jpg.);border:0px;')
        self.pushButton_11.setStyleSheet('image:url(../imgFile/chAD/f60.jpeg.);border:0px;')
        self.pushButton_12.setStyleSheet('image:url(../imgFile/chAD/f61.jpg.);border:0px;')

        self.pushButton_13.setStyleSheet('image:url(../imgFile/chAD/m10.jpg.);border:0px;')
        self.pushButton_14.setStyleSheet('image:url(../imgFile/chAD/m11.jpg.);border:0px;')
        self.pushButton_15.setStyleSheet('image:url(../imgFile/chAD/m20.jpeg.);border:0px;')
        self.pushButton_16.setStyleSheet('image:url(../imgFile/chAD/m21.png.);border:0px;')
        self.pushButton_17.setStyleSheet('image:url(../imgFile/chAD/m30.jpg.);border:0px;')
        self.pushButton_18.setStyleSheet('image:url(../imgFile/chAD/m31.jpg.);border:0px;')
        self.pushButton_19.setStyleSheet('image:url(../imgFile/chAD/m40.jpg.);border:0px;')
        self.pushButton_20.setStyleSheet('image:url(../imgFile/chAD/m41.jpg.);border:0px;')
        self.pushButton_21.setStyleSheet('image:url(../imgFile/chAD/m50.jpg.);border:0px;')
        self.pushButton_22.setStyleSheet('image:url(../imgFile/chAD/m51.jpg.);border:0px;')
        self.pushButton_23.setStyleSheet('image:url(../imgFile/chAD/m60.jpeg.);border:0px;')
        self.pushButton_24.setStyleSheet('image:url(../imgFile/chAD/m61.jpeg.);border:0px;')

    # 여자
    def f10(self):
        self.ad_ID = 'f10'
        self.close()

    def f11(self):
        self.ad_ID = 'f11'
        self.close()

    def f20(self):
        self.ad_ID = 'f20'
        self.close()

    def f21(self):
        self.ad_ID = 'f21'
        self.close()

    def f30(self):
        self.ad_ID = 'f30'
        self.close()

    def f31(self):
        self.ad_ID = 'f31'
        self.close()

    def f40(self):
        self.ad_ID = 'f40'
        self.close()

    def f41(self):
        self.ad_ID = 'f41'
        self.close()

    def f50(self):
        self.ad_ID = 'f50'
        self.close()

    def f51(self):
        self.ad_ID = 'f51'
        self.close()

    def f60(self):
        self.ad_ID = 'f60'
        self.close()

    def f61(self):
        self.ad_ID = 'f61'
        self.close()

    # 남자
    def m10(self):
        self.ad_ID = 'm10'
        self.close()

    def m11(self):
        self.ad_ID = 'm11'
        self.close()

    def m20(self):
        self.ad_ID = 'm20'
        self.close()

    def m21(self):
        self.ad_ID = 'm21'
        self.close()

    def m30(self):
        self.ad_ID = 'm30'
        self.close()

    def m31(self):
        self.ad_ID = 'm31'
        self.close()

    def m40(self):
        self.ad_ID = 'm40'
        self.close()

    def m41(self):
        self.ad_ID = 'm41'
        self.close()

    def m50(self):
        self.ad_ID = 'm50'
        self.close()

    def m51(self):
        self.ad_ID = 'm51'
        self.close()

    def m60(self):
        self.ad_ID = 'm60'
        self.close()

    def m61(self):
        self.ad_ID = 'm61'
        self.close()


class ServerThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        TCP_IP = '172.30.1.44'
        TCP_PORT = 9899
        tcpServer = socket(AF_INET, SOCK_STREAM)
        tcpServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        tcpServer.bind((TCP_IP, TCP_PORT))
        tcpServer.listen(4)
        threads = []

        while True:
            print("Multi Threaded Python server : Waiting for connections from TCP clients...")
            window.textBrowser.append("클라이언트 접속 대기중...")
            global conn
            global camConn
            global disConn
            conn, (ip, port) = tcpServer.accept()

            if ip == '172.30.1.52':
                camConn = conn
                camthread = CameraThread(ip, port, window)
                camthread.start()
                threads.append(camthread)
            if ip == '172.30.1.44':
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
        count = 0
        while True:
            global camConn
            img_path = '../imgFile/'
            FILE_NAME = (img_path + str(count) + '.jpg')

            self.recvImage(FILE_NAME)
            window.textBrowser.append(FILE_NAME + " 이미지 수신 완료")
            faceThread = Thread(target=lambda q, arg1: q.put(faceAnalyse(arg1)), args=(que, FILE_NAME))
            faceThread.setDaemon(True)
            faceThread.start()
            faceThread.join()
            today = datetime.datetime.today()
            global genderAge
            genderAge = que.get()
            print("서버가 받은 결과는: ", genderAge)
            guimsg = "성별, 연령대: " + str(genderAge[0]) + str(genderAge[1])
            window.textBrowser.append(guimsg)

            global ADtarget

            if genderAge == (-1, -1):
                window.textBrowser.append("얼굴이 인식되지 않습니다. 통계기반의 광고를 출력합니다.")
                majority = DB.findMajority(today.hour)
                ADtarget = DB.decideID(majority[0], majority[1])
            else:
                ADtarget = DB.decideID(genderAge[0], genderAge[1])
                self.insert_result(genderAge, str(today.hour))

            print("광고가 멀로 정해졌냐면:", ADtarget)
            window.textBrowser.append("광고 ID: " + ADtarget)
            window.label_2.setStyleSheet('image:url(../imgFile/'+ADtarget+'.jpg)')
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

    def insert_result(self, genderAge, time):
        # db.인식성공(성별, 연령대, 날짜, 시간, 광고 ID 이렇게 집어넣음 됨.)
        # 인식성공하고 광고 결정되면 통계에 집어 넣어주는 메소드를 서버에 만들어야 될 듯.
        DB.insertRecogResult(genderAge[0], genderAge[1], time)


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

    def sendID(self, ADtarget):
        print("이거 열심히 만들어보......는걸 프로토타입 발표 후에 하면 되겠네", ADtarget)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    serverThread = ServerThread(window)
    serverThread.start()
    DB = DB_interface()
    window.show()
    sys.exit(app.exec_())
