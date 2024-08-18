# -*- coding: utf-8 -*-
from ctypes import *
import os
import cv2
import numpy as np


# ================结构体定义=========================
class Struct_POSE_Handle(Structure):  # NLDJ_ACTION_Handle
    _fields_ = [("pvModel", c_void_p)]


class Struct_ACT_VarIn(Structure):  # NLDJ_ACTION_VarIn
    _fields_ = [("pubyIm", c_char_p), ("dwWidth", c_int), ("dwHeight", c_int), ("dwChannel", c_int)]


class Struct_POS(Structure):  # NL_Pose_POS
    _fields_ = [("x", c_float), ("y", c_float), ("p_score", c_float)]


class Struct_ACT_Info(Structure):  # NLDJ_ACPRED_Infor
    _fields_ = [("dwPoseNum", c_int), ("fPosePos", Struct_POS * 100), ("pdwBowHead", c_int),
                ("pdwHandUp", c_int), ("pdwStandUp", c_int), ("pdwBendOverDesk", c_int), ("pdwPlayPhone", c_int),
                ("pdwStudy", c_int)]


class Struct_UP_Pos(Structure):  # NL_upbodyPos
    _fields_ = [("x", c_int), ("y", c_int), ("height", c_int), ("width", c_int)]


class Struct_ACT_VarOut(Structure):  # NLDJ_ACTION_VarOut
    _fields_ = [("dwPersonNum", c_int), ("pdjActionInfors", Struct_ACT_Info * 64), ("pdjUpBodyPos", Struct_UP_Pos * 64),
                ("bUpBodyPosTrue", c_bool * 64)]


# POSE_PAIRS
gPosePairs = [1, 2, 1, 5, 2, 3, 3, 4, 5, 6, 6, 7, 1, 8, 8, 9, 9, 10, 1,
              11, 11, 12, 12, 13, 1, 0, 0, 14, 14, 16, 0, 15, 15, 17]

# POSE_COLORS
gColors = [255, 0, 85, 255, 0, 0, 255, 85, 0, 255, 170, 0, 255, 255, 0, 170, 255, 0,
           85, 255, 0, 0, 255, 0, 0, 255, 85, 0, 255, 170, 0, 255, 255, 0, 170, 255, 0,
           85, 255, 0, 0, 255, 255, 0, 170, 170, 0, 255, 255, 0, 255, 85, 0, 255]


class NLPose(object):
    """骨骼描点"""

    def __init__(self, libNamePath):
        """
        初始化
        :param libNamePath: 算法so库名称
        """
        if not os.path.exists(libNamePath):
            print("library file not exit!", libNamePath)
            quit()
            return -1001
        else:
            self.PACT = cdll.LoadLibrary(libNamePath)  # linux版本

        # 指定函数参数类型
        self.PACT.NL_ACTION_Command.argtypes = (POINTER(Struct_POSE_Handle), c_char_p)
        self.PACT.NL_ACTION_Command.restype = c_int
        self.PACT.NL_ACTION_Process.argtypes = (POINTER(Struct_POSE_Handle),
                                                POINTER(Struct_ACT_VarIn),
                                                POINTER(Struct_ACT_VarOut))
        self.PACT.NL_ACTION_Process.restype = c_int
        self.PACT.NL_ACTION_UnloadModel.argtypes = (POINTER(Struct_POSE_Handle),)
        self.PACT.NL_ACTION_UnloadModel.restype = c_int

        # 初始化：结构体变量和函数
        self.djACTHandle = Struct_POSE_Handle()  # 结构体变量定义
        self.djACTVarIn = Struct_ACT_VarIn()  # 结构体变量定义
        self.djACTVarOut = Struct_ACT_VarOut()  # 结构体变量定义

    def NL_Pose_ComInit(self, configPath):
        """
        骨骼描点初始化配置，以及加载模型
        :param configPath: 指定的配置文件路径, 以及模型路径
        :return: 返回0， 非0负数表示异常
        """
        if not os.path.exists(configPath):
            print("Config or model file not exit!")
            return -2501
        ret = self.PACT.NL_ACTION_Command(self.djACTHandle, configPath)
        if ret != 0:
            print("Command error code:", ret)
            return ret
        return ret

    def NL_Pose_InitVarIn(self, imgInput):
        """
        骨骼描点输入源参数设置
        :param imgInput: 一帧图片，或者一张图片
        :return: 返回0，非0负数表示异常
        """
        imgResize = cv2.resize(imgInput, (1280, 960), interpolation=cv2.INTER_CUBIC)
        img_len = len(imgResize.shape)
        if img_len == 3:
            srcBGR = imgResize
        else:
            srcBGR = cv2.cvtColor(imgResize, cv2.COLOR_GRAY2BGR)
        h, w, c = srcBGR.shape
        self.djACTVarIn.dwChannel = c
        self.djACTVarIn.dwWidth = w
        self.djACTVarIn.dwHeight = h
        self.djACTVarIn.pubyIm = srcBGR.astype(np.uint8).tostring()  # src_RGB.astype(np.uint8).tostring()
        if h > 1:
            return 0
        else:
            print("Init VarIn Error!")
            return -3001

    def NL_Pose_Process_C(self):
        """
        骨骼描点，主处理函数
        :return: 返回人员个数, 非0负数表示异常
        """
        try:
            ret = self.PACT.NL_ACTION_Process(self.djACTHandle, self.djACTVarIn, self.djACTVarOut)
        except Exception as e:
            print(e)
            ret = -1
        if ret != 0:
            print("Process Error code:", ret)
            return ret
        return int(self.djACTVarOut.dwPersonNum)

    def NL_Pose_Exit(self):
        """
        释放模型和内存
        :return:
        """
        ret = self.PACT.NL_ACTION_UnloadModel(self.djACTHandle)
        if ret != 0:
            print("UnloadModel Error code:", ret)
            return ret
        return ret
