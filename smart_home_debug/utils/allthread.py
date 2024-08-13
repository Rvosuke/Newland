# -*- coding:utf-8 -*-
# @author: 502
import re
import subprocess
import time
import serial
from PyQt5 import QtCore

from PyQt5.QtCore import QThread, QMutex


BASE_PATH = '/usr/local'  # 语音目录


class SpeechSolve(object):

    def __init__(self):
        self.voice_broadcast = BASE_PATH + '/speech/broadcast/bin/'
        self.voice_recognition = BASE_PATH + '/speech/recognition/bin/'

    def get_device_id(self):
        """
        获取音频设备id
        :return: 返回设备id号
        """
        try:
            pattern = re.compile(r'.*card (.*?): .*, device (.*?): USB Audio.*')
            dev_cmd = "aplay -l"
            res_content = subprocess.getstatusoutput(dev_cmd)
            if res_content[0] == 0 and res_content[1] != '':
                result = pattern.findall(res_content[1])
                if result:
                    return result[0]
                else:
                    return ''
            else:
                return ''
        except Exception as e:
            print('系统错误，获取设备id失败：' + str(e))
            return ''

    def broadcast(self, text):
        """
        语音合成
        :param text: 文本内容
        :return: 返回状态值，与信息
        """
        try:
            print('语音合成开始')
            broadcast_cmd = 'cd ' + self.voice_broadcast + " && ./tts_offline_sample {}".format(text)
            res_content = subprocess.getstatusoutput(broadcast_cmd)
            if res_content[0] == 0 and '合并成功' in res_content[1]:
                return 1, '语音合并成功'
            else:
                return 0, '语音合并失败'
        except Exception as e:
            print('系统错误，语音合成失败：' + str(e))
            return 0, '系统错误，语音合成播报失败：' + str(e)

    def play_sound(self, dev_id):
        """
        语音播报
        :param dev_id: 设备id号
        :return: 返回布尔值
        """
        try:
            play_cmd = 'cd ' + self.voice_broadcast + " && aplay -Dplughw:{},{} tts_sample.wav".format(dev_id[0], dev_id[1])
            res_content = subprocess.getstatusoutput(play_cmd)
            if res_content[0] == 0 and "Playing WAVE 'tts_sample.wav'" in res_content[1]:
                return True
            else:
                return False
        except Exception as e:
            print('系统错误，播报失败：' + str(e))
            return False

    def recognition(self):
        """
        语音识别
        :return: 返回识别结果，或者None
        """
        try:
            pattern = re.compile(r'<rawtext>(.*?)</rawtext>')
            recognition_cmd = 'cd ' + self.voice_recognition + ' && ./asr_offline_record_sample'
            print('正在监听。。。')
            res_content = subprocess.getstatusoutput(recognition_cmd)
            if res_content[0] == 0 and 'Result' in res_content[1]:
                result = pattern.findall(res_content[1])
                print(result)
                if result:
                    return result[0]
                else:
                    return None
            else:
                return None
        except Exception as e:
            print('系统错误，识别失败：' + str(e))
            return None


class QuerySerial(object):
    """
    获取相应传感器的值
    """

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyS0', 9600, timeout=0.2)
        self.ser.flushInput()

    def exec_cmd(self, command):
        """
        执行led控制
        :param command: 16进制值
        :return:
        """
        try:
            cmd = bytes.fromhex(command)
            # self.ser.reset_input_buffer()
            # self.ser.reset_output_buffer()
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.write(cmd)
            # data = self.ser.read(8)
            # logger.debug('4150_data: ' + str(data.hex()))
        except Exception as e:
            print('4150_data error: ' + str(e))

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

    def turn_on_yellow(self):
        """
        开启黄灯
        :return:
        """
        command = '01 05 00 11 FF 00 DC 3F'
        self.exec_cmd(command)

    def turn_off_yellow(self):
        """
        关闭黄灯
        :return:
        """
        command = '01 05 00 11 00 00 9D CF'
        self.exec_cmd(command)

    def turn_on_green(self):
        """
        开启绿灯
        :return:
        """
        command = '01 05 00 12 FF 00 2C 3F'
        self.exec_cmd(command)

    def turn_off_green(self):
        """
        关闭绿灯
        :return:
        """
        command = '01 05 00 12 00 00 6D CF'
        self.exec_cmd(command)

    def turn_on_door(self):
        """
        开门
        :return:
        """
        command = '01 05 00 13 FF 00 7D FF'
        self.exec_cmd(command)

    def turn_off_door(self):
        """
        关门
        :return:
        """
        command = '01 05 00 13 00 00 3C 0F'
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

    def get_beam_data(self, command='0C 03 00 00 00 02 C5 16'):
        """
        查询光照强度
        :param command:
        :return:
        """
        try:
            cmd = bytes.fromhex(command)
            # self.ser.reset_input_buffer()
            # self.ser.reset_output_buffer()
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.write(cmd)
            data = self.ser.read(9)
            print('beam_data: ' + str(data.hex()))
            data = str(data.hex())
            if data[0:2] == '0c':
                beam_var = int('0x' + data[6:14], 16)
                # print('beam_var: ' + str(beam_var))
                return beam_var
            else:
                return None
        except Exception as e:
            # print('beam_data error: ' + str(e))
            return None

    def fan_power_on(self):
        """
        风扇上电
        :return:
        """
        command = '01 05 00 15 FF 00 9D FE'
        self.exec_cmd(command)
        time.sleep(0.5)

    def fan_power_off(self):
        """
        风扇断电
        :return:
        """
        command = '01 05 00 15 00 00 DC 0E'
        self.exec_cmd(command)

    def fan_high_level(self):
        """
        风扇高电平
        :return:
        """
        command = '01 05 00 16 FF 00 6D FE'
        self.exec_cmd(command)

    def fan_low_level(self):
        """
        风扇低电平
        :return:
        """
        command = '01 05 00 16 00 00 2C 0E'
        self.exec_cmd(command)

    def open_fan(self):
        """
        打开风扇的脉冲信号
        :return:
        """
        self.fan_high_level()
        time.sleep(0.3)
        self.fan_low_level()

    def open_ambiance_lamp(self):
        """
        打开风扇的气氛灯脉冲信号
        :return:
        """
        self.fan_high_level()
        time.sleep(0.6)
        self.fan_low_level()

    def reset(self):
        """
        复位AiOT器件
        :return:
        """
        self.turn_off_green()
        time.sleep(0.05)
        self.turn_off_buzzer()
        time.sleep(0.05)
        self.fan_power_off()
        time.sleep(0.05)
        self.turn_off_yellow()
        time.sleep(0.05)
        self.turn_off_red()
        time.sleep(0.05)
        self.turn_off_door()

    def close_serial(self):
        """
        关闭串口
        :return:
        """
        try:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            self.ser.close()
        except Exception as e:
            print(e)


class BeamThread(QThread):
    """
    获取光照值刷新线程
    """
    beamUpdate = QtCore.pyqtSignal(str)

    def __init__(self, beam):
        self.beam = beam
        self.working = True
        self.mutex = QMutex()
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        while self.working:
            self.mutex.lock()
            try:
                beam = self.beam.qs.get_beam_data()
                if beam:
                    self.beamUpdate.emit(str(beam))
                time.sleep(1)
            except Exception as e:
                print('beam thread error: ' + str(e))
            self.mutex.unlock()

    def stop(self):
        if self.working:
            self.working = False


class VoiceRecThread(QThread):
    """
    语音识别线程
    """
    updateInfo = QtCore.pyqtSignal(int)

    def __init__(self, vr):
        self.vr = vr
        self.working = True
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        try:
            self.vr.result = self.vr.speak.recognition()
            if self.vr.result:
                self.updateInfo.emit(0)
            else:
                self.updateInfo.emit(0)
        except Exception as e:
            print('VoiceRecThread error: ' + str(e))

    def stop(self):
        if self.working:
            self.working = False
            print('VoiceRecThread is quit!')


class VoiceSpeakThread(QThread):
    """
    语音播报线程
    """
    updateInfo = QtCore.pyqtSignal(int)

    def __init__(self, vs, text, dev_id=None):
        self.vs = vs
        self.text = text
        self.dev_id = dev_id
        self.working = True
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        try:
            if self.dev_id:
                state, info = self.vs.speak.broadcast(self.text)
                if state:
                    self.vs.speak.play_sound(self.dev_id)
                else:
                    print(info)
            else:
                print('无相关音频设备')
        except Exception as e:
            print('VoiceSpeakThread error: ' + str(e))
        self.vs.voice_thread_state = False
        self.vs.voice_btn.setEnabled(True)


    def stop(self):
        if self.working:
            self.working = False
            print('VoiceRecThread is quit!')