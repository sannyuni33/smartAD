from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QScrollBar, QSplitter, QTableWidgetItem, QTableWidget, QComboBox, QVBoxLayout, QGridLayout, \
    QDialog, QWidget, QPushButton, QApplication, QMainWindow, QAction, QMessageBox, QLabel, QTextEdit, QProgressBar, \
    QLineEdit
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QTabWidget
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import sys
from PyQt5 import uic

MainUI = 'serverUI.ui'
changeUI = 'chAD.ui'

#광고 변경 GUI
class ch_Dialog(QDialog):
    def __init__(self,parent):
        self.ad_ID =None
        super(ch_Dialog,self).__init__(parent)
        uic.loadUi(changeUI, self)
        self.retranslateUi()
        self.show()
        self.pushButton.clicked.connect(self.f11)
        self.pushButton_2.clicked.connect(self.f12)
        self.pushButton_3.clicked.connect(self.f21)
        self.pushButton_4.clicked.connect(self.f22)
        self.pushButton_5.clicked.connect(self.f31)
        self.pushButton_6.clicked.connect(self.f32)

        self.pushButton_7.clicked.connect(self.f41)
        self.pushButton_8.clicked.connect(self.f42)
        self.pushButton_9.clicked.connect(self.f51)
        self.pushButton_10.clicked.connect(self.f52)
        self.pushButton_11.clicked.connect(self.f61)
        self.pushButton_12.clicked.connect(self.f62)

        self.pushButton_13.clicked.connect(self.m11)
        self.pushButton_14.clicked.connect(self.m12)
        self.pushButton_15.clicked.connect(self.m21)
        self.pushButton_16.clicked.connect(self.m22)
        self.pushButton_17.clicked.connect(self.m31)
        self.pushButton_18.clicked.connect(self.m32)

        self.pushButton_19.clicked.connect(self.m41)
        self.pushButton_20.clicked.connect(self.m42)
        self.pushButton_21.clicked.connect(self.m51)
        self.pushButton_22.clicked.connect(self.m52)
        self.pushButton_23.clicked.connect(self.m61)
        self.pushButton_24.clicked.connect(self.m62)
    def retranslateUi(self):
        #이함수는 탭마다 광고 이미지 넣어주는 함수
        _translate = QApplication.translate

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

        #이부분에 변경할 광고 이미지 추가해주세용
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
        self.close()

    def f11(self):
        self.ad_ID = 'f11'
        self.close()

    def f22(self):
        self.ad_ID = 'f22'
        self.close()

    def f21(self):
        self.ad_ID = 'f21'
        self.close()

    def f32(self):
        self.ad_ID = 'f32'
        self.close()

    def f31(self):
        self.ad_ID = 'f31'
        self.close()

    def f42(self):
        self.ad_ID = 'f42'
        self.close()

    def f41(self):
        self.ad_ID = 'f41'
        self.close()

    def f52(self):
        self.ad_ID = 'f52'
        self.close()

    def f51(self):
        self.ad_ID = 'f51'
        self.close()

    def f62(self):
        self.ad_ID = 'f62'
        self.close()

    def f61(self):
        self.ad_ID = 'f61'
        self.close()

    # 남자
    def m12(self):
        self.ad_ID = 'm12'
        self.close()

    def m11(self):
        self.ad_ID = 'm11'
        self.close()

    def m22(self):
        self.ad_ID = 'm22'
        self.close()

    def m21(self):
        self.ad_ID = 'm21'
        self.close()

    def m32(self):
        self.ad_ID = 'm32'
        self.close()

    def m31(self):
        self.ad_ID = 'm31'
        self.close()

    def m42(self):
        self.ad_ID = 'm42'
        self.close()

    def m41(self):
        self.ad_ID = 'm41'
        self.close()

    def m52(self):
        self.ad_ID = 'm52'
        self.close()

    def m51(self):
        self.ad_ID = 'm51'
        self.close()

    def m62(self):
        self.ad_ID = 'm62'
        self.close()

    def m61(self):
        self.ad_ID = 'm61'
        self.close()


# 서버 메인 GUI
class Window(QMainWindow,):
    def __init__(self):
        super().__init__()
        # 초기화면 세팅
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
        # ch window를 인자로 받아서 실행시킨다.

        cd = ch_Dialog(self)
        cd.exec()
        self.textBrowser.append("광고 변경을 시작합니다")
        id = cd.ad_ID

        # 10대 여자
        if id == 'f10':
            self.label_2.setStyleSheet('image:url(../imgFile/f20.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'f11':
            self.label_2.setStyleSheet('image:url(../imgFile/f11.jpg)')
            self.textBrowser.append(id+"광고로 변경됐슴다")
        # 20대 여자
        if id == 'f20':
            self.label_2.setStyleSheet('image:url(../imgFile/f22.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'f21':
            self.label_2.setStyleSheet('image:url(../imgFile/f21.jpg)')
            self.textBrowser.append(id+"광고로 변경됐슴다")
        # 30대 여자
        if id == 'f30':
            self.label_2.setStyleSheet('image:url(../imgFile/f32.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'f31':
            self.label_2.setStyleSheet('image:url(../imgFile/f31.jpg)')
            self.textBrowser.append(id+"광고로 변경됐슴다")
        # 40대 여자
        if id == 'f40':
            self.label_2.setStyleSheet('image:url(../imgFile/f42.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'f41':
            self.label_2.setStyleSheet('image:url(../imgFile/f41.jpg)')
            self.textBrowser.append(id+"광고로 변경됐슴다")
        # 50대 여자
        if id == 'f50':
            self.label_2.setStyleSheet('image:url(../imgFile/f52.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'f51':
            self.label_2.setStyleSheet('image:url(../imgFile/f51.jpg)')
            self.textBrowser.append(id+"광고로 변경됐슴다")
        # 60대 여자
        if id == 'f60':
            self.label_2.setStyleSheet('image:url(../imgFile/f62.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        # 10대 남자
        if id == 'm10':
            self.label_2.setStyleSheet('image:url(../imgFile/m12.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'm11':
            self.label_2.setStyleSheet('image:url(../imgFile/m11.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        #20대 남자
        if id == 'm20':
            self.label_2.setStyleSheet('image:url(../imgFile/m22.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'm21':
            self.label_2.setStyleSheet('image:url(../imgFile/m21.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        # 30대 남자
        if id == 'm30':
            self.label_2.setStyleSheet('image:url(../imgFile/m32.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'm31':
            self.label_2.setStyleSheet('image:url(../imgFile/m31.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")

        # 40대 남자
        if id == 'm40':
            self.label_2.setStyleSheet('image:url(../imgFile/m42.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'm41':
            self.label_2.setStyleSheet('image:url(../imgFile/m41.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        # 50대 남자
        if id == 'm50':
            self.label_2.setStyleSheet('image:url(../imgFile/m52.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'm51':
            self.label_2.setStyleSheet('image:url(../imgFile/m51.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        # 60대 남자
        if id == 'm60':
            self.label_2.setStyleSheet('image:url(../imgFile/m62.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")
        if id == 'm61':
            self.label_2.setStyleSheet('image:url(../imgFile/m61.jpg)')
            self.textBrowser.append(id + "광고로 변경됐슴다")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

"""
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(688, 541)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(30, 30, 631, 461))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton_23 = QtWidgets.QPushButton(self.tab)
        self.pushButton_23.setGeometry(QtCore.QRect(40, 60, 261, 281))
        self.pushButton_23.setObjectName("pushButton_23")
        self.pushButton_24 = QtWidgets.QPushButton(self.tab)
        self.pushButton_24.setGeometry(QtCore.QRect(330, 60, 261, 281))
        self.pushButton_24.setObjectName("pushButton_24")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 70, 261, 281))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_4.setGeometry(QtCore.QRect(330, 70, 261, 281))
        self.pushButton_4.setObjectName("pushButton_4")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_5.setGeometry(QtCore.QRect(40, 60, 261, 281))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_6.setGeometry(QtCore.QRect(330, 60, 261, 281))
        self.pushButton_6.setObjectName("pushButton_6")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_7.setGeometry(QtCore.QRect(30, 60, 261, 281))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_8.setGeometry(QtCore.QRect(320, 60, 261, 281))
        self.pushButton_8.setObjectName("pushButton_8")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.pushButton_9 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_9.setGeometry(QtCore.QRect(40, 60, 261, 281))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_10.setGeometry(QtCore.QRect(330, 60, 261, 281))
        self.pushButton_10.setObjectName("pushButton_10")
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.pushButton_11 = QtWidgets.QPushButton(self.tab_6)
        self.pushButton_11.setGeometry(QtCore.QRect(30, 50, 261, 281))
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_12 = QtWidgets.QPushButton(self.tab_6)
        self.pushButton_12.setGeometry(QtCore.QRect(320, 50, 261, 281))
        self.pushButton_12.setObjectName("pushButton_12")
        self.tabWidget.addTab(self.tab_6, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.pushButton_13 = QtWidgets.QPushButton(self.tab_7)
        self.pushButton_13.setGeometry(QtCore.QRect(40, 60, 261, 281))
        self.pushButton_13.setObjectName("pushButton_13")
        self.pushButton_14 = QtWidgets.QPushButton(self.tab_7)
        self.pushButton_14.setGeometry(QtCore.QRect(330, 60, 261, 281))
        self.pushButton_14.setObjectName("pushButton_14")
        self.tabWidget.addTab(self.tab_7, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.pushButton_15 = QtWidgets.QPushButton(self.tab_8)
        self.pushButton_15.setGeometry(QtCore.QRect(50, 70, 261, 281))
        self.pushButton_15.setObjectName("pushButton_15")
        self.pushButton_16 = QtWidgets.QPushButton(self.tab_8)
        self.pushButton_16.setGeometry(QtCore.QRect(340, 70, 261, 281))
        self.pushButton_16.setObjectName("pushButton_16")
        self.tabWidget.addTab(self.tab_8, "")
        self.tab_9 = QtWidgets.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.pushButton_17 = QtWidgets.QPushButton(self.tab_9)
        self.pushButton_17.setGeometry(QtCore.QRect(30, 60, 261, 281))
        self.pushButton_17.setObjectName("pushButton_17")
        self.pushButton_18 = QtWidgets.QPushButton(self.tab_9)
        self.pushButton_18.setGeometry(QtCore.QRect(320, 60, 261, 281))
        self.pushButton_18.setObjectName("pushButton_18")
        self.tabWidget.addTab(self.tab_9, "")
        self.tab_10 = QtWidgets.QWidget()
        self.tab_10.setObjectName("tab_10")
        self.pushButton_19 = QtWidgets.QPushButton(self.tab_10)
        self.pushButton_19.setGeometry(QtCore.QRect(30, 70, 261, 281))
        self.pushButton_19.setObjectName("pushButton_19")
        self.pushButton_20 = QtWidgets.QPushButton(self.tab_10)
        self.pushButton_20.setGeometry(QtCore.QRect(320, 70, 261, 281))
        self.pushButton_20.setObjectName("pushButton_20")
        self.tabWidget.addTab(self.tab_10, "")
        self.tab_11 = QtWidgets.QWidget()
        self.tab_11.setObjectName("tab_11")
        self.pushButton_21 = QtWidgets.QPushButton(self.tab_11)
        self.pushButton_21.setGeometry(QtCore.QRect(40, 60, 261, 281))
        self.pushButton_21.setObjectName("pushButton_21")
        self.pushButton_22 = QtWidgets.QPushButton(self.tab_11)
        self.pushButton_22.setGeometry(QtCore.QRect(330, 60, 261, 281))
        self.pushButton_22.setObjectName("pushButton_22")
        self.tabWidget.addTab(self.tab_11, "")
        self.tab_12 = QtWidgets.QWidget()
        self.tab_12.setObjectName("tab_12")
        self.pushButton = QtWidgets.QPushButton(self.tab_12)
        self.pushButton.setGeometry(QtCore.QRect(40, 70, 261, 281))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_12)
        self.pushButton_2.setGeometry(QtCore.QRect(330, 70, 261, 281))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tabWidget.addTab(self.tab_12, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_23.setText(_translate("Dialog", "PushButton"))
        self.pushButton_24.setText(_translate("Dialog", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Tab 1"))
        self.pushButton_3.setText(_translate("Dialog", "PushButton"))
        self.pushButton_4.setText(_translate("Dialog", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Tab 2"))
        self.pushButton_5.setText(_translate("Dialog", "PushButton"))
        self.pushButton_6.setText(_translate("Dialog", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "쪽"))
        self.pushButton_7.setText(_translate("Dialog", "PushButton"))
        self.pushButton_8.setText(_translate("Dialog", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog", "쪽"))
        self.pushButton_9.setText(_translate("Dialog", "PushButton"))
        self.pushButton_10.setText(_translate("Dialog", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Dialog", "쪽"))
        self.pushButton_11.setText(_translate("Dialog", "PushButton"))
        self.pushButton_12.setText(_translate("Dialog", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("Dialog", "쪽"))
        self.pushButton_13.setText(_translate("Dialog", "PushButton"))
        self.pushButton_14.setText(_translate("Dialog", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _translate("Dialog", "쪽"))
        self.pushButton_15.setText(_translate("Dialog", "PushButton"))
        self.pushButton_16.setText(_translate("Dialog", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), _translate("Dialog", "쪽"))
        self.pushButton_17.setText(_translate("Dialog", "PushButton"))
        self.pushButton_18.setText(_translate("Dialog", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_9), _translate("Dialog", "쪽"))
        self.pushButton_19.setText(_translate("Dialog", "PushButton"))
        self.pushButton_20.setText(_translate("Dialog", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_10), _translate("Dialog", "쪽"))
        self.pushButton_21.setText(_translate("Dialog", "PushButton"))
        self.pushButton_22.setText(_translate("Dialog", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_11), _translate("Dialog", "쪽"))
        self.pushButton.setText(_translate("Dialog", "PushButton"))
        self.pushButton_2.setText(_translate("Dialog", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_12), _translate("Dialog", "쪽"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
"""
