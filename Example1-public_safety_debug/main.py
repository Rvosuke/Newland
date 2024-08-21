import sys
import time

import serial
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
import signal
from UI.home import Ui_Home
from Utils.AiThreads import HiKangThread, ShowCameraThread




class HomePage(QWidget, Ui_Home):
    """
    应用界面
    """

    def __init__(self):
        super(HomePage, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.showImage = None
        self.light_state = False
        self.buzzer_state = False
        self.ser = serial.Serial('/dev/ttyS0', 9600, timeout=0.2)
        self.device_reset()
        self.light_btn.clicked.connect(self.control_light)
        self.buzzer_btn.clicked.connect(self.control_buzzer)
        self.show_thread = ShowCameraThread(self)
        self.show_thread.cameraUpdatedImage.connect(self.show_camera)
        self.show_thread.start()

    def show_camera(self):
        """
        显示摄像头
        :return:
        """
        if self.showImage:
            self.labelshow_camera.setPixmap(self.showImage)

    def turn_on_red(self):
        """
        开启红灯
        :return:
        """
        command = '01 05 00 10 FF 00 8D FF'
        self.exec_cmd(command)

    def turn_off_red(self):
        """
        关闭红灯
        :return:
        """
        command = '01 05 00 10 00 00 CC 0F'
        self.exec_cmd(command)

    def turn_on_buzzer(self):
        """
        打开蜂鸣器
        :return:
        """
        command = '01 05 00 14 FF 00 CC 3E'
        self.exec_cmd(command)

    def turn_off_buzzer(self):
        """
        关闭蜂鸣器
        :return:
        """
        command = '01 05 00 14 00 00 8D CE'
        self.exec_cmd(command)

    def control_light(self):
        if not self.light_state:
            self.light_btn.setText('关闭警示灯')
            self.light_state = True
            self.turn_on_red()
        else:
            self.light_btn.setText('打开警示灯')
            self.light_state = False
            self.turn_off_red()

    def control_buzzer(self):
        if not self.buzzer_state:
            self.buzzer_btn.setText('关闭蜂鸣器')
            self.buzzer_state = True
            self.turn_on_buzzer()
        else:
            self.buzzer_btn.setText('打开蜂鸣器')
            self.buzzer_state = False
            self.turn_off_buzzer()

    def exec_cmd(self, command):
        """
        执行led控制
        :param command: 16进制值
        :return:
        """
        try:
            cmd = bytes.fromhex(command)
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.write(cmd)
        except Exception as e:
            print('4150_data error: ' + str(e))

    def device_reset(self):
        self.turn_off_buzzer()
        time.sleep(0.5)
        self.turn_off_red()
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        # rtsp摄像头线程
        hikang_thread = HiKangThread()
        hikang_thread.start()
        app = QApplication(sys.argv)
        app.setOverrideCursor(QtGui.QCursor(Qt.BlankCursor))
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        home_page = HomePage()
        home_page.show()
        sys.exit(app.exec_())

    except Exception as e:
        print(e)
