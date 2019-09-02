# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'haha.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QApplication, QLCDNumber
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(879, 547)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(350, 20, 201, 51))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(290, 150, 291, 121))
        self.lcdNumber.setObjectName("lcdNumber")

        self.lcdNumber.setWindowIconText("1023")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 879, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "BARAM_부릉이 차량호출기"))


class Clock(QLCDNumber):
    def __init__(self):
        super().__init__()

        title = "Digital Clock"
        top = 400
        left = 400
        width = 450
        height = 300

        icon = "clock.png"

        self.setWindowTitle(title)
        self.setGeometry(top,left,width,height)
        self.setWindowIcon(QIcon(icon))

        self.setSegmentStyle(QLCDNumber.Filled)
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.showTime()


    def showTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        if(time.second() %2)==0:
            text=text[:2] + ' ' + text[3:]

        self.display(text)
'''
app = QApplication(sys.argv)
clock = Clock()
clock.show()
app.exec()
'''



if __name__ == "__main__":
    import sys


    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()


    clock = Clock()
    print('a')
    clock.show()
    sys.exit(app.exec_())

    app = QApplication(sys.argv)

    app.exec()


