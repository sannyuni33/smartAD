import os
import sys
import datetime
import matplotlib
from socket import *
import socket as sc
from threading import Thread
import struct
import cv2
import requests
import json
import queue
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
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

# 메인쓰레드와 워커쓰레드 모두 접근 가능한 전역변수. (얼굴 분석 결과)
genderAge = None
ADtarget = None
histoFlag = False


# 얼굴분석 워커 쓰레드가 리턴하는 값을 메인 쓰레드가 받아보기 위해 큐 사용
que = queue.Queue()

# 서버 GUI 구성 ui 파일
MainUI = '../UI/serverUI0701.ui'
showAdUI = '../UI/showAdUI.ui'
addUI = '../UI/addUI.ui'
deleteUI = '../UI/deleteUI.ui'
changeTwinUI = '../UI/changeTwinUI.ui'
changeUI = '../UI/chAD.ui'

# NAVER API 연결
client_id = "38hNSdXWRhGUHxMpaRoV"
client_secret = "5YF8TJC9YQ"
url = "https://openapi.naver.com/v1/vision/face"
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}

# matplotlib 한글 출력 설정
font_name = font_manager.FontProperties(fname="C:/Windows/Fonts/08seoulnamsanl.ttf").get_name()
rc('font', family=font_name)


# 카메라 클라이언트가 전송한 이미지에 대해 얼굴분석 수행
def faceAnalyse(FILE_NAME):
    recog_result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    global histoFlag
    # 히스토그램 평활화
    if histoFlag:
        src = cv2.imread(FILE_NAME)
        hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        equalizedV = cv2.equalizeHist(v)
        hsv2 = cv2.merge([h, s, equalizedV])
        hsv3 = cv2.cvtColor(hsv2, cv2.COLOR_HSV2BGR)
        cv2.imwrite(FILE_NAME, hsv3)

    files = {'image': open(FILE_NAME, 'rb')}

    response = requests.post(url, files=files, headers=headers)
    rescode = response.status_code

    if rescode != 200:
        print("Error Code:" + rescode)

    json_data = json.loads(response.text)
    img = cv2.imread(FILE_NAME, cv2.IMREAD_COLOR)

    for i in json_data['faces']:
        x, y, w, h = i['roi'].values()
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
        gender = i['gender']['value']
        age = i['age']['value']
        confi = i['age']['confidence']
        age1, age2 = age.split('~')
        final_age = (int(age1) + int(age2)) / 2

        result = """%s, %s, %s""" % (gender, str(age), str(confi))
        if gender:
            DB.insertRecogResult(gender, final_age, time)
        print(result)
        # putText 할 때 이미지? 얼굴? 크기에 따라 폰트 크기를 다르게 한다면 좋을 것 같다!
        cv2.putText(img, result, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (255, 255, 255), 1, cv2.LINE_AA)

        recog_index = 0
        if gender == 'female':
            recog_index += 6
        recog_index += int((final_age//10)) + 1
        recog_result[recog_index] += 1


    cv2.imwrite(FILE_NAME, img)
    window.qPixmapFileVar.load(FILE_NAME)
    window.qPixmapFileVar = window.qPixmapFileVar.scaled(650, 720)
    window.label.setPixmap(window.qPixmapFileVar)

    if max(recog_result) == 0:
        return 0
    else:
        index_list = [i for i, j in enumerate(recog_result) if j == max(recog_result)]

    result_list = []
    for i in index_list:
        if i < 6:
            temp_gender = 'male'
            temp_age = (i+1)*10
        else:
            temp_gender = 'female'
            temp_age = (i-5)*10
        result_list.append([temp_gender, temp_age])
    print("result_list: ", result_list)
    return result_list


def sendCam(msg):
    text = msg
    global camConn
    camConn.send(text.encode("utf-8"))


def sendDis(msg):
    text = msg
    global disConn
    disConn.send(text.encode("utf-8"))


# 서버 관리자용 GUI
class Window(QMainWindow, ):
    def __init__(self):
        super().__init__()
        global histoFlag
        # 초기화면 세팅
        uic.loadUi(MainUI, self)
        self.showFullScreen()
        self.setWindowTitle("서버 GUI")
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load("../imgFile/ready.png")
        self.qPixmapFileVar = self.qPixmapFileVar.scaled(650, 720)
        self.label.setPixmap(self.qPixmapFileVar)
        self.label_2.setPixmap(self.qPixmapFileVar)
        self.pushButton.clicked.connect(self.showAdInfo)
        self.pushButton_2.clicked.connect(self.addAdInfo)
        self.pushButton_3.clicked.connect(self.changeTwinInfo)
        self.pushButton_4.clicked.connect(self.deleteAdInfo)
        self.pushButton_5.clicked.connect(self.showAdStat)
        self.pushButton_6.clicked.connect(self.showTimeStat)
        self.pushButton_7.clicked.connect(self.startAD)
        self.pushButton_8.clicked.connect(self.pauseAD)
        self.pushButton_9.clicked.connect(self.chCamTime)
        self.pushButton_10.clicked.connect(self.changeAD)
        self.pushButton_11.clicked.connect(self.closeAd)
        self.checkBox.stateChanged.connect(self.histogramOn)

    def showAdInfo(self):
        print("광고정보조회")
        cd5 = showAd_Dialog(self)
        cd5.exec

    def addAdInfo(self):
        print("광고정보를 추가합니다. ")
        cd2 = add_Dialog(self)
        cd2.exec()

    def changeTwinInfo(self):
        print("광고정보를 변경합니다. ")
        cd4 = change_Dialog(self)
        cd4.exec()

    def deleteAdInfo(self):
        print("광고정보를 삭제합니다.")
        cd3 = delete_Dialog(self)
        cd3.exec()

    def showTimeStat(self):
        print("시간대별 인식통계를 조회합니다.")
        res = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        res_cnt = DB.lookUpTimeStat(datetime.datetime.today().hour)
        for row in res_cnt:
            index = 0
            if row[0] == 'female':
                index += 6
            index += (int(row[1])//10)-1
        label = ['male\n10', 'male\n20', 'male\n30', 'male\n40',
                 'male\n50', 'male\n60', 'female\n10', 'female\n20',
                 'female\n30', 'female\n40', 'female\n50', 'female\n60']

        bar_width = 0.35
        opacity = 0.5
        font = {'size': 9.5}
        matplotlib.rc('font', **font)
        plt.bar(label, res, bar_width, bottom=2,
                tick_label=label, align='center', label='A',
                alpha=opacity, color='b', edgecolor='black', linewidth=1.2)

        plt.title(str(datetime.datetime.today().hour) + "시 인식결과통계")
        plt.xlim(-0.5, 12)
        plt.ylabel('인식 횟수')

        plt.show()

    def showAdStat(self):
        print("광고별 관심지수통계를 조회합니다.")
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

    def startAD(self):
        sendCam("start")
        sendDis("start")
        print("광고를 시작합니다!")

    def pauseAD(self):
        sendCam("pause")
        sendDis("pause")
        print("광고를 일시 중단합니다!")

    def chCamTime(self):
        self.chmsg = self.lineEdit.text()
        sendCam(self.chmsg)
        print(self.chmsg + "초로 카메라 주기 변경")

    def changeAD(self):
        cd = ch_Dialog(self)
        cd.exec()
        id = cd.ad_ID
        self.qPixmapFileVar2 = QPixmap()
        self.qPixmapFileVar2.load("../imgFile/" + id + ".jpg")
        self.qPixmapFileVar2 = self.qPixmapFileVar2.scaled(650, 720)
        self.label_2.setPixmap(self.qPixmapFileVar2)
        print(id + "광고로 변경됐슴다")

    def closeAd(self):
        sendCam("exit")
        sendDis("exit")
        print("시스템을 종료합니다.")
        time.sleep(3)

    def histogramOn(self, state):
        global histoFlag
        if state == Qt.Checked:
            print("히스토 온")
            histoFlag = True
        else:
            print("히스토 오프")
            histoFlag = False


def sendFile(FILE_NAME):
    global disConn
    FILE_SIZE = os.path.getsize(FILE_NAME)
    FILE_SIZE = struct.pack('L', FILE_SIZE)

    try:
        n = 0
        f = open(FILE_NAME, 'rb')
        i = f.read(BUFF_SIZE)

        disConn.send(FILE_SIZE)
        n += 1
        while i:
            disConn.send(i)
            i = f.read(BUFF_SIZE)
        f.close()

        print('(check) ' + FILE_NAME + ' transfer complete')

    except Exception as e:
        sys.exit()


# 광고조회
class showAd_Dialog(QDialog):
    def __init__(self, parent):
        super(showAd_Dialog, self).__init__(parent)
        uic.loadUi(showAdUI, self)
        self.pushButton.clicked.connect(self.changeOk)
        self.show()
        self.dbInfo = DB.showAD()
        self.tableWidget.setRowCount(len(self.dbInfo))
        self.showAdInfo2(self.dbInfo)

    def showAdInfo2(self, dbInfo):  # ui컬럼에 db정보 추가 함수
        for idx, (hname, price_str, price, vol, ayou) in enumerate(dbInfo):
            print(idx)
            self.tableWidget.setItem(idx, 0, QTableWidgetItem(hname))
            self.tableWidget.setItem(idx, 1, QTableWidgetItem(price_str))
            self.tableWidget.setItem(idx, 2, QTableWidgetItem(price))
            self.tableWidget.setItem(idx, 3, QTableWidgetItem(str(vol)))
            self.tableWidget.setItem(idx, 4, QTableWidgetItem(str(ayou)))

    def changeOk(self):
        self.close()


# 광고정보 추가 GUI
class add_Dialog(QDialog):
    def __init__(self, parent):
        super(add_Dialog, self).__init__(parent)
        uic.loadUi(addUI, self)
        self.AD_ID = self.lineEdit.text()
        self.target = self.lineEdit_2.text()
        # 성별
        self.comboBox.activated[str].connect(self.ComboBoxEvent)
        # 연령대
        self.comboBox_2.activated[str].connect(self.ComboBoxEvent2)
        self.pushButton.clicked.connect(self.addImage)
        self.pushButton_5.clicked.connect(self.addOk)
        self.pushButton_6.clicked.connect(self.addClose)
        self.label_6.setStyleSheet('background:white')
        self.gender = "male"
        self.age = "10"

        self.show()

    def ComboBoxEvent(self):  # 성별
        self.gender = self.comboBox.currentText()

    def ComboBoxEvent2(self):  # 연령대
        self.age = self.comboBox_2.currentText()

    def addImage(self):
        self.fname = QFileDialog.getOpenFileName(self)
        self.label_6.setText(self.fname[0])

    def addOk(self):
        DB.insertAD(self.lineEdit.text(), self.lineEdit_2.text(), self.gender, self.age)
        sendDis('img' + self.lineEdit_2.text())
        sendFile(self.fname[0])
        self.close()

    def addClose(self):
        self.close()


# 광고정보 삭제 GUI
class delete_Dialog(QDialog):
    def __init__(self, parent):
        super(delete_Dialog, self).__init__(parent)
        uic.loadUi(deleteUI, self)
        self.pushButton.clicked.connect(self.deleteOk)
        self.pushButton_2.clicked.connect(self.deleteClose)
        self.show()

    def deleteOk(self):
        DB.deleteAD(self.lineEdit.text())
        sendDis('del' + self.lineEdit.text())
        self.close()

    def deleteClose(self):
        self.close()


# 디지털트윈 광고 추가 GUI
class change_Dialog(QDialog):
    def __init__(self, parent):
        super(change_Dialog, self).__init__(parent)
        uic.loadUi(changeTwinUI, self)

        self.comboBox.activated[str].connect(self.ComboBoxEvent)
        self.pushButton.clicked.connect(self.changeTwin)
        self.pushButton_2.clicked.connect(self.changeOk)
        self.pushButton_3.clicked.connect(self.changeClose)
        self.show()

        self.twin = "vid"

    def ComboBoxEvent(self):
        self.twin = self.comboBox.currentText()

    def changeTwin(self):
        self.twinName = QFileDialog.getOpenFileName(self)

    def changeOk(self):
        global disConn
        sendDis(self.twin+self.self.lineEdit.text())
        sendFile(self.twinName[0])
        self.close()

    def changeClose(self):
        self.close()


# 광고변경 GUI
class ch_Dialog(QDialog):
    def __init__(self, parent):
        self.ad_ID = None
        super(ch_Dialog, self).__init__(parent)
        uic.loadUi(changeUI, self)
        self.retranslateUi()
        self.show()
        self.pushButton.clicked.connect(self.f12)
        self.pushButton_2.clicked.connect(self.f11)
        self.pushButton_3.clicked.connect(self.f22)
        self.pushButton_4.clicked.connect(self.f21)
        self.pushButton_5.clicked.connect(self.f32)
        self.pushButton_6.clicked.connect(self.f31)

        self.pushButton_7.clicked.connect(self.f42)
        self.pushButton_8.clicked.connect(self.f41)
        self.pushButton_9.clicked.connect(self.f52)
        self.pushButton_10.clicked.connect(self.f51)
        self.pushButton_11.clicked.connect(self.f62)
        self.pushButton_12.clicked.connect(self.f61)

        self.pushButton_13.clicked.connect(self.m12)
        self.pushButton_14.clicked.connect(self.m11)
        self.pushButton_15.clicked.connect(self.m22)
        self.pushButton_16.clicked.connect(self.m21)
        self.pushButton_17.clicked.connect(self.m32)
        self.pushButton_18.clicked.connect(self.m31)

        self.pushButton_19.clicked.connect(self.m42)
        self.pushButton_20.clicked.connect(self.m41)
        self.pushButton_21.clicked.connect(self.m52)
        self.pushButton_22.clicked.connect(self.m51)
        self.pushButton_23.clicked.connect(self.m62)
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
        self.pushButton.setStyleSheet('image:url(../imgFile/f12.jpg.);border:0px;')
        self.pushButton_2.setStyleSheet('image:url(../imgFile/f11.jpg.);border:0px;')
        self.pushButton_3.setStyleSheet('image:url(../imgFile/f22.jpg.);border:0px;')
        self.pushButton_4.setStyleSheet('image:url(../imgFile/f21.jpg.);border:0px;')
        self.pushButton_5.setStyleSheet('image:url(../imgFile/f32.jpg.);border:0px;')
        self.pushButton_6.setStyleSheet('image:url(../imgFile/f31.jpg.);border:0px;')
        self.pushButton_7.setStyleSheet('image:url(../imgFile/f42.jpg.);border:0px;')
        self.pushButton_8.setStyleSheet('image:url(../imgFile/f41.jpg.);border:0px;')
        self.pushButton_9.setStyleSheet('image:url(../imgFile/f52.jpg.);border:0px;')
        self.pushButton_10.setStyleSheet('image:url(../imgFile/f51.jpg.);border:0px;')
        self.pushButton_11.setStyleSheet('image:url(../imgFile/f62.jpg.);border:0px;')
        self.pushButton_12.setStyleSheet('image:url(../imgFile/f61.jpg.);border:0px;')

        self.pushButton_13.setStyleSheet('image:url(../imgFile/m12.jpg.);border:0px;')
        self.pushButton_14.setStyleSheet('image:url(../imgFile/m11.jpg.);border:0px;')
        self.pushButton_15.setStyleSheet('image:url(../imgFile/m22.jpg.);border:0px;')
        self.pushButton_16.setStyleSheet('image:url(../imgFile/m21.jpg.);border:0px;')
        self.pushButton_17.setStyleSheet('image:url(../imgFile/m32.jpg.);border:0px;')
        self.pushButton_18.setStyleSheet('image:url(../imgFile/m31.jpg.);border:0px;')
        self.pushButton_19.setStyleSheet('image:url(../imgFile/m42.jpg.);border:0px;')
        self.pushButton_20.setStyleSheet('image:url(../imgFile/m41.jpg.);border:0px;')
        self.pushButton_21.setStyleSheet('image:url(../imgFile/m52.jpg.);border:0px;')
        self.pushButton_22.setStyleSheet('image:url(../imgFile/m51.jpg.);border:0px;')
        self.pushButton_23.setStyleSheet('image:url(../imgFile/m62.jpg.);border:0px;')
        self.pushButton_24.setStyleSheet('image:url(../imgFile/m61.jpg.);border:0px;')

    # 여자
    def f12(self):
        self.ad_ID = 'f12'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def f11(self):
        self.ad_ID = 'f11'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def f22(self):
        self.ad_ID = 'f22'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def f21(self):
        self.ad_ID = 'f21'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def f32(self):
        self.ad_ID = 'f32'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def f31(self):
        self.ad_ID = 'f31'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def f42(self):
        self.ad_ID = 'f42'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def f41(self):
        self.ad_ID = 'f41'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def f52(self):
        self.ad_ID = 'f52'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def f51(self):
        self.ad_ID = 'f51'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def f62(self):
        self.ad_ID = 'f62'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def f61(self):
        self.ad_ID = 'f61'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    # 남자
    def m12(self):
        self.ad_ID = 'm12'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def m11(self):
        self.ad_ID = 'm11'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def m22(self):
        self.ad_ID = 'm22'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def m21(self):
        self.ad_ID = 'm21'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def m32(self):
        self.ad_ID = 'm32'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def m31(self):
        self.ad_ID = 'm31'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def m42(self):
        self.ad_ID = 'm42'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def m41(self):
        self.ad_ID = 'm41'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def m52(self):
        self.ad_ID = 'm52'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def m51(self):
        self.ad_ID = 'm51'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def m62(self):
        self.ad_ID = 'm62'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()

    def m61(self):
        self.ad_ID = 'm61'
        global disConn
        disConn.send(self.ad_ID.encode('utf-8'))
        self.close()


class ServerThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        TCP_IP = sc.gethostbyname_ex(sc.gethostname())
        TCP_PORT = 9899
        tcpServer = socket(AF_INET, SOCK_STREAM)
        tcpServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        tcpServer.bind((TCP_IP[2][-1], TCP_PORT))
        tcpServer.listen(4)
        threads = []

        while True:
            print("Multi Threaded Python server : Waiting for connections from TCP clients...")
            print("클라이언트 접속 대기중...")
            global conn
            global camConn
            global disConn
            conn, (ip, port) = tcpServer.accept()

            if ip == '192.168.142.29':
                camConn = conn
                camthread = CameraThread(ip, port, window)
                camthread.start()
                threads.append(camthread)
            if ip == '192.168.103.67':
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
        count = 0
        while True:
            global camConn
            FILE_NAME = ('../imgFile/' + str(count) + '.jpg')

            self.recvImage(FILE_NAME)
            print(FILE_NAME + " 이미지 수신 완료")
            faceThread = Thread(target=lambda q, arg1: q.put(faceAnalyse(arg1)), args=(que, FILE_NAME))
            faceThread.setDaemon(True)
            faceThread.start()
            faceThread.join()
            today = datetime.datetime.today()
            global genderAge
            genderAge = que.get()
            print("서버가 받은 결과는: ", genderAge)
            global ADtarget

            if not genderAge:
                print("얼굴이 인식되지 않습니다. 통계기반의 광고를 출력합니다.")
                majority = DB.findMajority(today.hour)
                ADtarget = DB.decideID(majority[0], majority[1])
            else:
                if len(genderAge) == 1:
                    ADtarget = DB.decideID(genderAge[0][0], genderAge[0][1])
                else:
                    countList = []
                    for i in genderAge:
                        countList.append(DB.recogCount(i[0], i[1], today.hour))
                    print("countList: ", countList)
                    maxIndex = countList.index(max(countList))
                    ADtarget = DB.decideID(genderAge[maxIndex][0], genderAge[maxIndex][1])

            print("광고가 멀로 정해졌냐면:", ADtarget)
            print("광고 ID: " + ADtarget)
            window.qPixmapFileVar.load(('../imgFile/' + ADtarget + '.jpg'))
            window.qPixmapFileVar = window.qPixmapFileVar.scaled(650, 720)
            window.label_2.setPixmap(window.qPixmapFileVar)
            global disConn
            disConn.send(ADtarget.encode('utf-8'))
            print(ADtarget+"전송완료")

            count += 1

    def recvImage(self, FILE_NAME):
        global camConn
        FILE_LEN = 0
        FILE_SIZE = camConn.recv(4)
        FILE_SIZE = struct.unpack('L', FILE_SIZE)[0]

        f = open(FILE_NAME, 'wb')
        while True:
            client_file = camConn.recv(BUFF_SIZE)

            if not client_file:
                break

            f.write(client_file)
            FILE_LEN += len(client_file)

            if FILE_LEN == int(FILE_SIZE):
                break

        f.close()


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
            print(data.decode('utf-8'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    serverThread = ServerThread(window)
    serverThread.start()
    DB = DB_interface()
    window.show()
    sys.exit(app.exec_())

