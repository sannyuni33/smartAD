import sys, time
from PyQt5.QtWidgets import QScrollBar, QSplitter, QTableWidgetItem, QTableWidget, QComboBox, QVBoxLayout, QGridLayout, \
    QDialog, QPushButton, QApplication, QMainWindow, QAction, QMessageBox, QLabel, QTextEdit, QProgressBar, \
    QLineEdit, QTabWidget,QWidget
import socket
from threading import Thread,Timer
from PyQt5 import uic
from PyQt5.QtCore import QUrl, QRect,QCoreApplication
from PyQt5.QtWebEngineWidgets import QWebEnginePage


MainUI = 'UI/label5.ui'

class Ui_MainWindow(object):
    def __init__(self):
        #super().__init__()
        super(Ui_MainWindow,self).__init__()
        self.setupUi()
        #self.show()

    def setupUi(self):

        self.resize(799, 596)
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.pushButton_2 = QPushButton(self.tab)
        self.pushButton_2.setGeometry(QRect(10, 80, 241, 341))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QPushButton(self.tab)
        self.pushButton_3.setGeometry(QRect(270, 80, 241, 341))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QPushButton(self.tab)
        self.pushButton_4.setGeometry(QRect(530, 80, 241, 341))
        self.pushButton_4.setObjectName("pushButton_4")
        self.tabWidget.addTab(self.tab, "")

        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.pushButton_5 = QPushButton(self.tab_2)
        self.pushButton_5.setGeometry(QRect(270, 80, 241, 341))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QPushButton(self.tab_2)
        self.pushButton_6.setGeometry(QRect(10, 80, 241, 341))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QPushButton(self.tab_2)
        self.pushButton_7.setGeometry(QRect(530, 80, 241, 341))
        self.pushButton_7.setObjectName("pushButton_7")
        self.tabWidget.addTab(self.tab_2, "")



        self.verticalLayout.addWidget(self.tabWidget)
        self.setCentralWidget(self.centralwidget)


        self.retranslateUi()
        self.tabWidget.setCurrentIndex(5)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setStyleSheet('image:url(joojoo.jpg.);border:0px;')
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "10대여자"))
        self.pushButton_2.clicked.connect(self.Stop)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "20대여자"))

    def Stop(self):
        print("광고 변경")
        #여기다가 메시지 주고 종료
        sys.exit()

class Window(QDialog, ):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(MainUI, self)
        self.setWindowTitle("영상윤주 디스플레이 GUI")
        #self.label.setStyleSheet('image:url(video.mp4)')
        #self.webEngineView.load(QUrl("https://www.google.com"))
        self.pushButton.clicked.connect(self.urlGo)
        self.pushButton_2.clicked.connect(self.Stop)
        self.pushButton_3.clicked.connect(self.modelclick)

    def aaa(self, ID):

        if ID == 'f10':
            self.label.setStyleSheet('image:url(m12.jpg)')

        else:
            self.label.setStyleSheet('image:url(m20.png)')

    def urlGo(self):
        print("")






    def Stop(self):
        print('PyQt5 stop')

    def modelclick(self):
        print('PyQt5 stop')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())



