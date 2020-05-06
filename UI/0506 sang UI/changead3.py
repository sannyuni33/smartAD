import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class1 = uic.loadUiType("serverfinal.ui")[0]
form_class2 = uic.loadUiType("changead.ui")[0]

class AdWindow(QMainWindow, form_class2):
    def __init__(self, parent=None):
        super(AdWindow, self).__init__(parent)
        self.setupUi(self)



class Window(QDialog, form_class1):
    def __init__(self):
        QDialog.__init__(self, None)
        super().__init__()

    def __init__(self):
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
        self.adWindow = AdWindow()
        self.adWindow.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = Window()
    mywindow.show()
    app.exec_()