# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewClock.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import QTime
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLCDNumber
from PyQt5 import QtCore, QtGui, QtWidgets


from gui_CarNumber import *

print("gui_clock 불리는중 ")
system_time = 0
flag = 0


class Clock(QLCDNumber):

    def __init__(self):
        super().__init__()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()

    def showTime(self):
        global system_time
        global flag
        if flag  == 0:
            time = QTime.currentTime()
            text = time.toString('hh:mm:ss')
            system_time = text
            print(system_time)
            if (time.second() % 2) == 0:
                text = text[:2] + ' ' + text[3:]
            self.display(text)
            flag = 1

        elif flag == 1:
            time = QTime.currentTime()
            text = time.toString('hh:mm:ss')
            system_time = text
            print(system_time)
            if (time.second() % 2) == 0:
                text = text[:2] + ' ' + text[3:]
            self.display(text)
            ui = Ui_MainWindow()
            ui.setupUi(MainWindow)
            MainWindow.show()

        elif flag == 2:                   # 화면전환을 위한 flag
            time = QTime.currentTime()
            text = time.toString('hh:mm:ss')
            system_time = text
            if (time.second() % 2) == 0:
                text = text[:2] + ' ' + text[3:]
            self.display(text)
            ui = Ui_MainWindow1()
            ui.setup(MainWindow)

class Ui_MainWindow(object):

    def carIn(self):
        global flag
        ui = Ui_MainWindow1_in()
        ui.setup(MainWindow)
        MainWindow.show()
        flag = 2  # 화면전환을 위한 flag


    def ok(self):
        global flag
        #global MainWindow
        ui = Ui_MainWindow1()
        ui.setup(MainWindow)
        MainWindow.show()
        flag = 2                   # 화면전환을 위한 flag



    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(879, 647)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 30, 351, 101))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setFamily("NanumGothic")
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(170, 140, 541, 191))
        self.lcdNumber.setDigitCount(8)    # 8칸 맞추기
        self.lcdNumber.setObjectName("lcdNumber")
        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(190, 400, 221, 71))

        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(470, 400, 221, 71))

        font = QtGui.QFont()
        font.setPointSize(20)
        font.setFamily("NanumGothic")
        self.pushButton1.setFont(font)
        self.pushButton1.setObjectName("pushButton")

        self.pushButton2.setFont(font)
        self.pushButton2.setObjectName("pushButton")

        #############################################
        self.pushButton1.clicked.connect(Ui_MainWindow.ok)  # 버튼 클릭시 ok함수 실행
        self.pushButton2.clicked.connect(Ui_MainWindow.carIn)  # 버튼 클릭시 ok함수 실행

        #############################################
        self.lcdNumber.display(system_time)  # LCD에 숫자 띄우기

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
        self.pushButton1.setText(_translate("MainWindow", "내 차 부르기"))
        self.pushButton2.setText(_translate("MainWindow", "내 차 주차하기"))



import sys

app = QtWidgets.QApplication(sys.argv)
clock = Clock()  # Clock 객체 만들면 생성자 바로 호출된다.
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()



app.exec()       # 루프
sys.exit()       # 종료 버튼 누르면 끄기

