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
        self.layoutWidget = QtWidgets.QWidget(Home)
        self.layoutWidget.setGeometry(QtCore.QRect(15, 15, 1891, 891))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.labelshow_camera = QtWidgets.QLabel(self.layoutWidget)
        self.labelshow_camera.setMinimumSize(QtCore.QSize(1024, 768))
        self.labelshow_camera.setMaximumSize(QtCore.QSize(1024, 768))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.labelshow_camera.setFont(font)
        self.labelshow_camera.setText("")
        self.labelshow_camera.setAlignment(QtCore.Qt.AlignCenter)
        self.labelshow_camera.setObjectName("labelshow_camera")
        self.horizontalLayout_2.addWidget(self.labelshow_camera)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.layoutWidget1 = QtWidgets.QWidget(Home)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 911, 1901, 191))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.light_btn = QtWidgets.QPushButton(self.layoutWidget1)
        self.light_btn.setMinimumSize(QtCore.QSize(300, 100))
        self.light_btn.setMaximumSize(QtCore.QSize(300, 100))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.light_btn.setFont(font)
        self.light_btn.setStyleSheet("QPushButton#select_btn:focus{border-radius:10px;background-color: rgb(255, 255, 255);border: 1px solid #E8E8E8;color: rgb(45, 60, 99);}\n"
"QPushButton#select_btn{border-radius:10px;background-color: rgb(255, 255, 255);border: 1px solid #E8E8E8;color: rgb(45, 60, 99);}")
        self.light_btn.setObjectName("light_btn")
        self.horizontalLayout.addWidget(self.light_btn)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.buzzer_btn = QtWidgets.QPushButton(self.layoutWidget1)
        self.buzzer_btn.setMinimumSize(QtCore.QSize(300, 100))
        self.buzzer_btn.setMaximumSize(QtCore.QSize(300, 100))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.buzzer_btn.setFont(font)
        self.buzzer_btn.setStyleSheet("QPushButton#select_btn:focus{border-radius:10px;background-color: rgb(255, 255, 255);border: 1px solid #E8E8E8;color: rgb(45, 60, 99)}\n"
"QPushButton#select_btn{border-radius:10px;background-color: rgb(255, 255, 255);border: 1px solid #E8E8E8;color: rgb(45, 60, 99)}")
        self.buzzer_btn.setObjectName("buzzer_btn")
        self.horizontalLayout.addWidget(self.buzzer_btn)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)

        self.retranslateUi(Home)
        QtCore.QMetaObject.connectSlotsByName(Home)

    def retranslateUi(self, Home):
        _translate = QtCore.QCoreApplication.translate
        Home.setWindowTitle(_translate("Home", "Form"))
        self.light_btn.setText(_translate("Home", "打开警示灯"))
        self.buzzer_btn.setText(_translate("Home", "打开蜂鸣器"))

