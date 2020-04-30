import sys, time
from PyQt5.QtWidgets import QScrollBar, QSplitter, QTableWidgetItem, QTableWidget, QComboBox, QVBoxLayout, QGridLayout, \
    QDialog, QWidget, QPushButton, QApplication, QMainWindow, QAction, QMessageBox, QLabel, QTextEdit, QProgressBar, \
    QLineEdit
import socket
from threading import Thread
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5 import uic

tcpClientA = None
MainUI = 'label5.ui'


class Window(QDialog, ):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(MainUI, self)
        self.label.setStyleSheet('image:url(ggg.jpg)')

    def aaa(self, ID):
        if ID == 'f10':
            self.label.setStyleSheet('image:url(f10.jpg)')
        if ID == 'f20':
            self.label.setStyleSheet('image:url(f20.jpg)')
        if ID == 'f30':
            self.label.setStyleSheet('image:url(f30.jpg)')
        if ID == 'f40':
            self.label.setStyleSheet('image:url(f40.jpg)')
        if ID == 'f50':
            self.label.setStyleSheet('image:url(f50.jpg)')
        if ID == 'f60':
            self.label.setStyleSheet('image:url(f60.jpg)')
        if ID == 'm10':
            self.label.setStyleSheet('image:url(m10.jpg)')
        if ID == 'm20':
            self.label.setStyleSheet('image:url(m20.jpg)')
        if ID == 'm30':
            self.label.setStyleSheet('image:url(m30.jpg)')
        if ID == 'm40':
            self.label.setStyleSheet('image:url(m40.jpg)')
        if ID == 'm50':
            self.label.setStyleSheet('image:url(m50.jpg)')
        if ID == 'm60':
            self.label.setStyleSheet('image:url(m60.jpg)')


class ClientThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        host = '172.30.98.130'
        port = 9966
        BUFFER_SIZE = 2048
        global tcpClientA
        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpClientA.connect((host, port))

        while True:
            data = tcpClientA.recv(BUFFER_SIZE)
            ID = data.decode('utf-8')
            window.aaa(ID)

        tcpClientA.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    clientThread = ClientThread(window)  # 쓰레드 객체 생성
    clientThread.start()  # 쓰레드 시작
    window.exec()
    sys.exit(app.exec_())
