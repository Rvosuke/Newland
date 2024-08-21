import copy

import numpy as np
import os
from ctypes import *

import time

import cv2
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, QMutex
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication
from concurrent.futures import ThreadPoolExecutor

from Algorithm.rtspCamera import NLRtspApi
import faulthandler

faulthandler.enable()
executor = ThreadPoolExecutor()

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('Aithread', BASE_PATH)

# --------------物体类别中英文定义 ------------------
toy_style = {
    'aeroplane': '飞机',
    'apple': '苹果',
    'banana': '香蕉',
    'bicycle': '自行车',
    'car': '汽车',
    'cat': '猫',
    'cow': '牛',
    'dog': '狗',
    'horse': '马',
    'motorcycle': '摩托车',
    'mouse': '鼠标',
    'person': '人',
    'sheep': '山羊'
}
rtsp_img = None
rtsp_img_2 = None
rtsp_img_3 = None
login_user_info = None


class HiKangThread(QThread):
    """
    枪型摄像头
    """

    def __init__(self):
        QThread.__init__(self)
        self.working = True
        self.CapIsbasy = False
        self.thread_state = False
        self.s_u8nMediaIndex = (c_uint * 16)()

    def __del__(self):
        self.wait()

    def rtsp_config(self):
        lib_path = '/usr/lib/newland/libmedia.so'
        self.nl_rtsp_api = NLRtspApi(libNamePath=lib_path)
        # self.nl_rtsp_api.nl_media_stop()
        try:
            config_path = bytes(BASE_PATH, 'utf-8') + b'/Config/rtsp_config.ini'
            self.nl_rtsp_api.read_ini(config_path)
            num = self.nl_rtsp_api.get_url_num_from_ini()  # 获取url数量
            urls = []
            for i in range(num):
                rtsp_url = self.nl_rtsp_api.get_url_from_ini(i)  # 获取每一个url，放到列表里面
                urls.append(rtsp_url)
                self.s_u8nMediaIndex[i] = c_uint(i)
            rtsp_dict = {
                'url_num': num,
                'urls': urls
            }
            ret = self.nl_rtsp_api.nl_media_init()  # 初始化
            if ret != 0:
                self.nl_rtsp_api.nl_media_stop()
                return
            ret2 = self.nl_rtsp_api.nl_media_resource_config(self.s_u8nMediaIndex, num,
                                                             rtsp_dict)  # 配置，0表示h264，1表示h265
            if ret2 != 0:
                self.nl_rtsp_api.nl_media_stop()
                return
            ret3 = self.nl_rtsp_api.nl_media_start(self.s_u8nMediaIndex, num)  # 启动
            if ret3 != 0:
                self.nl_rtsp_api.nl_media_stop()
                return
            while self.working:
                if not self.thread_state:
                    self.thread_state = True
                    self.hikang_thread1 = HiKangThread1(self.nl_rtsp_api)
                    self.hikang_thread1.start()
                    # self.hikang_thread2 = HiKangThread2(self.nl_rtsp_api)
                    # self.hikang_thread2.start()
                time.sleep(1)
        except KeyboardInterrupt as e:
            self.nl_rtsp_api.nl_media_stop()
        except Exception as e:
            print('rtsp系统错误，' + str(e))
            self.nl_rtsp_api.nl_media_stop()

    def run(self):
        self.rtsp_config()

    def stop(self):
        if self.working:
            self.working = False
            self.hikang_thread1.stop()
            self.hikang_thread2.stop()
            self.nl_rtsp_api.nl_media_stop()
            print('The CameraThread is quit!')


class HiKangThread1(QThread):
    """
    枪型摄像头
    """

    def __init__(self, nl_rtsp_api):
        QThread.__init__(self)
        self.working = True
        self.CapIsbasy = False
        self.nl_rtsp_api = nl_rtsp_api

    def __del__(self):
        self.wait()

    def run(self):
        global rtsp_img, rtsp_img_1
        while self.working:
            try:
                # 采集图像的过程中
                ret4 = self.nl_rtsp_api.nl_media_read(0)  # 读取
                if ret4 == -1:
                    time.sleep(0.01)
                    continue
                else:
                    image_1280_960 = self.nl_rtsp_api.img_data_0.tnBgrScaleData[0].u64VirAddr
                    width_1280 = self.nl_rtsp_api.img_data_0.tnBgrScaleData[0].u32Width
                    height_960 = self.nl_rtsp_api.img_data_0.tnBgrScaleData[0].u32Height
                    srcString_1280 = string_at(image_1280_960, height_960 * width_1280 * 3)
                    imageMatIr_1280 = np.frombuffer(srcString_1280, np.uint8)
                    imageMatIr_1280 = imageMatIr_1280.reshape(height_960, width_1280, 3)
                    rtsp_img_1 = copy.deepcopy(imageMatIr_1280)

                    image_p = self.nl_rtsp_api.img_data_0.tnBgrScaleData[1].u64VirAddr
                    width = self.nl_rtsp_api.img_data_0.tnBgrScaleData[1].u32Width
                    height = self.nl_rtsp_api.img_data_0.tnBgrScaleData[1].u32Height
                    srcString = string_at(image_p, height * width * 3)
                    imageMatIr = np.frombuffer(srcString, np.uint8)
                    imageMatIr = imageMatIr.reshape(height, width, 3)
                    rtsp_img = copy.deepcopy(imageMatIr)

                    for i in range(self.nl_rtsp_api.img_data_0.ucScaleNum):
                        ret5 = self.nl_rtsp_api.nl_media_data_release(self.nl_rtsp_api.img_data_0.tnBgrScaleData[i])
            except KeyboardInterrupt as e:
                self.nl_rtsp_api.nl_media_stop()
            except Exception as e:
                print('rtsp2系统错误，' + str(e))
                self.nl_rtsp_api.nl_media_stop()

    def stop(self):
        if self.working:
            self.working = False
            print('The CameraThread is quit!')


class ShowCameraThread(QThread):
    """
    摄像头展示
    """
    cameraUpdatedImage = QtCore.pyqtSignal(int)

    def __init__(self, fr):
        self.fr = fr
        self.working = True
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        while self.working:

            try:
                limg = rtsp_img
                height, width, bytesPerComponent = limg.shape
                bytesPerLine = bytesPerComponent * width
                rgb = cv2.cvtColor(limg, cv2.COLOR_BGR2RGB)
                showImage = QImage(rgb.data, width, height, bytesPerLine, QImage.Format_RGB888)
                self.fr.showImage = QPixmap.fromImage(showImage)
                self.cameraUpdatedImage.emit(0)
            except Exception as e:
                print('FaceRegisterThread: ' + str(e))
                time.sleep(1)
                pass

    def stop(self):
        if self.working:
            self.working = False
            self.enable_smart(0)
            print('FaceRegisterThread is quit!')


