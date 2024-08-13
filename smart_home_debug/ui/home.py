# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Home(object):
    def setupUi(self, Home):
        Home.setObjectName("Home")
        Home.resize(1920, 1080)
        self.voice_btn = QtWidgets.QPushButton(Home)
        self.voice_btn.setGeometry(QtCore.QRect(1000, 770, 321, 121))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(20)
        self.voice_btn.setFont(font)
        self.voice_btn.setStyleSheet("QPushButton#voice_btn:focus{border-radius:10px;background-color: rgb(255, 255, 255);border: 1px solid #E8E8E8;color: rgb(45, 60, 99)}\n"
"QPushButton#voice_btn{border-radius:10px;background-color: rgb(255, 255, 255);border: 1px solid #E8E8E8;color: rgb(45, 60, 99)}")
        self.voice_btn.setObjectName("voice_btn")
        self.groupBox_2 = QtWidgets.QGroupBox(Home)
        self.groupBox_2.setGeometry(QtCore.QRect(80, 70, 1761, 691))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.light_textBrowser = QtWidgets.QTextBrowser(self.groupBox_2)
        self.light_textBrowser.setGeometry(QtCore.QRect(30, 30, 1701, 651))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.light_textBrowser.setFont(font)
        self.light_textBrowser.setObjectName("light_textBrowser")
        self.label_info = QtWidgets.QLabel(Home)
        self.label_info.setGeometry(QtCore.QRect(300, 910, 1331, 131))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_info.setFont(font)
        self.label_info.setText("")
        self.label_info.setAlignment(QtCore.Qt.AlignCenter)
        self.label_info.setObjectName("label_info")
        self.light_btn = QtWidgets.QPushButton(Home)
        self.light_btn.setGeometry(QtCore.QRect(600, 770, 321, 121))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.light_btn.setFont(font)
        self.light_btn.setStyleSheet("QPushButton#light_btn:focus{border-radius:10px;background-color: rgb(255, 255, 255);border: 1px solid #E8E8E8;color: rgb(45, 60, 99)}\n"
"QPushButton#light_btn{border-radius:10px;background-color: rgb(255, 255, 255);border: 1px solid #E8E8E8;color: rgb(45, 60, 99)}")
        self.light_btn.setObjectName("light_btn")

        self.retranslateUi(Home)
        QtCore.QMetaObject.connectSlotsByName(Home)

    def retranslateUi(self, Home):
        _translate = QtCore.QCoreApplication.translate
        Home.setWindowTitle(_translate("Home", "Form"))
        self.voice_btn.setText(_translate("Home", "开始语音识别"))
        self.groupBox_2.setTitle(_translate("Home", "光照传感器"))
        self.light_textBrowser.setHtml(_translate("Home", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.light_btn.setText(_translate("Home", "获取光照度"))

