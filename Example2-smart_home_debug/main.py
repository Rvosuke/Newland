# -*- coding:utf-8 -*-
# @author: 502
import random
import signal
import subprocess
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget
from ui.home import Ui_Home
from utils.allthread import BeamThread, VoiceRecThread, VoiceSpeakThread, SpeechSolve, QuerySerial


class HomePage(QWidget, Ui_Home):
    """
    应用界面
    """

    def __init__(self):
        super(HomePage, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.fan_state = False
        self.isVoice = False
        self.voice_thread_state = False
        self.light_btn.clicked.connect(self.get_light_data)
        self.voice_btn.clicked.connect(self.open_voice_rec)
        self.speak = SpeechSolve()  # 语音模块
        self.qs = QuerySerial()
        self.qs.reset()
        self.words = ['打开风扇', '关闭风扇']
        self.fan_open_words = ['风扇已经开了呢', '别玩了，风已经够大了', '没听到风扇在呼呼的响吗？']
        self.fan_close_words = ['风扇已经关了', '风扇没有在转', '别逗了，早就没风了']

    def get_light_data(self):
        self.beam_thread = BeamThread(self)
        self.beam_thread.beamUpdate.connect(self.print_light_log)
        self.beam_thread.start()
        self.light_btn.setEnabled(False)

    def open_voice_rec(self):
        self.voice_btn.setEnabled(False)
        self.vr_thread = VoiceRecThread(self)
        self.vr_thread.updateInfo.connect(self.voice_rec)
        self.vr_thread.start()
        self.label_info.setText('请说出打开风扇或者关闭风扇')

    def voice_rec(self):
        try:
            if self.result:
                if self.result in self.words:
                    if self.result == '打开风扇':
                        if not self.fan_state:
                            self.fan_control()
                            if not self.voice_thread_state:
                                self.speak_text('风扇已打开')
                                self.label_info.setText('风扇已打开')
                        else:
                            if not self.voice_thread_state:
                                word = random.choice(self.fan_open_words)
                                self.speak_text(word)
                                self.label_info.setText(word)
                    elif self.result == '关闭风扇':
                        if self.fan_state:
                            self.fan_control()
                            if not self.voice_thread_state:
                                self.speak_text('风扇已关闭')
                                self.label_info.setText('风扇已关闭')
                        else:
                            if not self.voice_thread_state:
                                word = random.choice(self.fan_close_words)
                                self.speak_text(word)
                                self.label_info.setText(word)
                else:
                    self.speak_text('无法识别， 请重试')
                    self.label_info.setText('无法识别， 请重试')
            else:
                self.speak_text('无法识别， 请重试')
                self.label_info.setText('无法识别， 请重试')
        except Exception as e:
            pass

    def speak_text(self, text):
        try:
            dev_id = self.speak.get_device_id()
            if dev_id:
                self.voice_thread_state = True
                self.vs_thread = VoiceSpeakThread(self, text, dev_id)
                self.vs_thread.start()
            else:
                print('没有相关音频设备，无法使用语音播报')
                self.label_info.setText('没有相关音频设备，无法使用语音播报')
        except Exception as e:
            print('系统错误，语音播报无法使用：' + str(e))

    def fan_control(self):
        """
        风扇控制
        """
        try:
            if self.fan_state:
                self.qs.fan_power_off()
                self.fan_state = False

            else:
                self.qs.fan_power_on()
                self.qs.open_fan()
                self.fan_state = True
        except Exception as e:
            pass

    def print_light_log(self, text):
        self.light_textBrowser.append('当前光照度为: {}'.format(text))
        self.cursor = self.light_textBrowser.textCursor()
        self.light_textBrowser.moveCursor(self.cursor.End)
        if int(text) < 100:
            self.qs.turn_on_yellow()
            self.light_textBrowser.append('光照度太低，已为您打开灯'.format(text))
            self.cursor = self.light_textBrowser.textCursor()
            self.light_textBrowser.moveCursor(self.cursor.End)
        elif int(text) > 200:
            self.qs.turn_off_yellow()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOverrideCursor(QtGui.QCursor(Qt.BlankCursor))
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    home_page = HomePage()
    home_page.show()
    sys.exit(app.exec_())
