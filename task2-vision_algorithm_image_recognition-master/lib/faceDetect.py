# -*- coding: utf-8 -*-
from ctypes import *
import os

import cv2
import numpy as np


# -----------人脸识别结构体定义---------------
class FaceRect(Structure):
    _fields_ = [("x1", c_float), ("y1", c_float), ("x2", c_float), ("y2", c_float), ("score", c_float)]


class FacePts(Structure):
    _fields_ = [("x", c_float * 5), ("y", c_float * 5)]


class FaceInfo(Structure):
    _fields_ = [("bbox", FaceRect), ("regression", c_float * 4), ("facePts", FacePts), ("quality", c_float),
                ("good", c_bool),
                ("track", c_bool), ("chn", c_int), ("dev", c_int), ("src", c_char_p), ("img_w", c_int),
                ("img_h", c_int)]


class NLDJ_EM_Handle(Structure):
    _fields_ = [("fdModel", c_void_p), ("faModel", c_void_p), ("fd_nnie_id", c_int), ("fe_nnie_id", c_int)]


class NLDJ_ED_VarIn(Structure):
    _fields_ = [("imgaddr", c_char_p), ("imgWidth", c_int), ("imgHeight", c_int), ("pyramid", c_char_p),
                ("pydWidth", c_int), ("pydHeight", c_int), ("chn", c_int), ("dev", c_int)]


class NLDJ_ED_VarOut(Structure):
    _fields_ = [("num", c_uint), ("chn", c_int), ("dev", c_int), ("faceInfos", FaceInfo * 255)]


class NLDJ_EA_VarIn(Structure):
    _fields_ = [("faces", FaceInfo * 255), ("num", c_uint)]


class NLDJ_EA_VarOut(Structure):
    _fields_ = [("faces", FaceInfo * 255), ("num", c_uint)]


class NLDJ_ER_VarIn(Structure):
    _fields_ = [("faces", FaceInfo * 255), ("num", c_uint)]


class NLDJ_ER_VarOut(Structure):
    _fields_ = [("faces", FaceInfo * 255), ("features", c_float * 512 * 255), ("num", c_uint)]


############################################################################


class NLFaceDetect(object):
    def __init__(self, libNamePath):
        """
        加载库，以及指定函数参数类型，初始化结构体变量
        :param libNamePath: 算法库路径
        """
        # 人脸识别目标动态库
        if not os.path.exists(libNamePath):
            print("library file not exit! " + str(libNamePath))
            return -1001
        else:
            self.FD_SO = cdll.LoadLibrary(libNamePath)

        # 人脸识别指定函数参数类型
        self.FD_SO.NL_EA_Init.argtypes = (POINTER(NLDJ_EM_Handle),)
        self.FD_SO.NL_EA_Init.restype = c_int
        self.FD_SO.NL_EA_Process.argtypes = (POINTER(NLDJ_EM_Handle), POINTER(NLDJ_EA_VarIn), POINTER(NLDJ_EA_VarOut))
        self.FD_SO.NL_EA_Process.restype = c_int

        self.FD_SO.NL_EM_Command.argtypes = (POINTER(NLDJ_EM_Handle), c_char_p)
        self.FD_SO.NL_EM_Command.restype = c_int
        self.FD_SO.NL_EM_Exit.argtypes = (POINTER(NLDJ_EM_Handle),)
        self.FD_SO.NL_EM_Exit.restype = c_int
        self.FD_SO.NL_EM_UnloadModel.argtypes = (POINTER(NLDJ_EM_Handle),)
        self.FD_SO.NL_EM_UnloadModel.restype = c_int

        self.FD_SO.NL_ED_Init.argtypes = (POINTER(NLDJ_EM_Handle),)
        self.FD_SO.NL_ED_Init.restype = c_int
        self.FD_SO.NL_ED_Process.argtypes = (POINTER(NLDJ_EM_Handle), POINTER(NLDJ_ED_VarIn), POINTER(NLDJ_ED_VarOut))
        self.FD_SO.NL_ED_Process.restype = c_int

        self.FD_SO.NL_ER_Init.argtypes = (POINTER(NLDJ_EM_Handle),)
        self.FD_SO.NL_ER_Init.restype = c_int
        self.FD_SO.NL_ER_Process.argtypes = (POINTER(NLDJ_EM_Handle), POINTER(NLDJ_ER_VarIn), POINTER(NLDJ_ER_VarOut))
        self.FD_SO.NL_ER_Process.restype = c_int

        self.FD_SO.NL_EC_Process.argtypes = ((c_float * 512), (c_float * 512), POINTER(c_float))
        self.FD_SO.NL_EC_Process.restype = c_int

        # 人脸识别初始化：结构体变量和函数
        ret = 0  # 返回值
        self.djEMHandle = NLDJ_EM_Handle()  # 结构体变量定义
        self.djEAVarIn = NLDJ_EA_VarIn()  # 结构体变量定义
        self.djEAVarOut = NLDJ_EA_VarOut()  # 结构体变量定义
        self.djEDVarIn = NLDJ_ED_VarIn()  # 结构体变量定义
        self.djEDVarOut = NLDJ_ED_VarOut()  # 结构体变量定义
        self.djERVarIn = NLDJ_ER_VarIn()  # 结构体变量定义
        self.djERVarOut = NLDJ_ER_VarOut()  # 结构体变量定义

    def NL_FD_ComInit(self, configPath):
        """
        加载人脸模型，以及人脸检测初始化内存，人脸对齐初始化，人脸特征提取初始化
        :param configPath: 指定的人脸模型和配置的路径
        :return: 返回非零值，则表示初始化失败
        """
        if not os.path.exists(configPath):
            print("Config file not exit! " + str(configPath))
            return -2501
        ret = self.FD_SO.NL_EM_Command(self.djEMHandle, configPath)  # 加载人脸模型
        if ret != 0:
            print("Command Error Code: " + str(ret))
            self.FD_SO.NL_EM_Exit(self.djEMHandle)
            self.FD_SO.NL_EM_UnloadModel(self.djEMHandle)
            return ret

        ret = self.FD_SO.NL_ED_Init(self.djEMHandle)  # 人脸检测初始化
        if ret != 0:
            print("ED Init Error Code: " + str(ret))
            self.FD_SO.NL_EM_Exit(self.djEMHandle)
            self.FD_SO.NL_EM_UnloadModel(self.djEMHandle)
            return ret

        ret = self.FD_SO.NL_EA_Init(self.djEMHandle)  # 人脸对齐初始化
        if ret != 0:
            print("EA Init Error Code: " + str(ret))
            self.FD_SO.NL_EM_Exit(self.djEMHandle)
            self.FD_SO.NL_EM_UnloadModel(self.djEMHandle)
            return ret

        ret = self.FD_SO.NL_ER_Init(self.djEMHandle)  # 人脸特征提取初始化
        if ret != 0:
            print("ER Init Error Code: " + str(ret))
            self.FD_SO.NL_EM_Exit(self.djEMHandle)
            self.FD_SO.NL_EM_UnloadModel(self.djEMHandle)
            return ret

    def NL_FD_InputImg(self, inputImg):
        """
        读取图片
        :param inputImg: 图片路径或图片源
        :return:
        """
        if not os.path.exists(inputImg):
            print("Image file not exit! ")
            return -3001
        else:
            img = cv2.imread(inputImg)
            img_len = len(img.shape)
            if img_len == 3:
                src_RGB = img
            else:
                src_RGB = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            return src_RGB

    def NL_FD_InitVarIn(self, srcBGR):
        """
        输入参数的设置
        :param src_RGB: 一帧图片，或者一张图片
        :return: 返回0，非0负数表示异常
        """
        h, w, c = srcBGR.shape
        self.djEDVarIn.imgaddr = srcBGR.astype(np.uint8).tostring()
        self.djEDVarIn.imgWidth = w
        self.djEDVarIn.imgHeight = h
        self.djEDVarIn.pyramid = None
        self.djEDVarIn.chn = 9
        self.djEDVarIn.dev = 1
        if h > 1:
            return 0
        else:
            print("NL_FD_InitVarIn Error!")
            return -1001

    def NL_FD_Process_C(self):
        """
        人脸检测，主处理函数
        :return: 成功返回人脸个数，失败返回小于零的值
        """
        ret = self.FD_SO.NL_ED_Process(self.djEMHandle, self.djEDVarIn, self.djEDVarOut)
        if ret != 0:
            print("ED Process Error Code:", ret)
            self.FD_SO.NL_EM_Exit(self.djEMHandle)
            self.FD_SO.NL_EM_UnloadModel(self.djEMHandle)
            return ret
        else:
            return int(self.djEDVarOut.num)

    def NL_EA_Process_C(self):
        """
        人脸对齐
        :return: 人脸对齐的个数，非0负数表示异常
        """
        self.djEAVarIn.num = self.djEDVarOut.num
        for i in range(self.djEDVarOut.num):
            self.djEAVarIn.faces[i] = self.djEDVarOut.faceInfos[i]

        ret = self.FD_SO.NL_EA_Process(self.djEMHandle, self.djEAVarIn, self.djEAVarOut)
        if ret != 0:
            print("EA Process Error Code: " + str(ret))
            self.FD_SO.NL_EM_Exit(self.djEMHandle)
            self.FD_SO.NL_EM_UnloadModel(self.djEMHandle)
            return ret
        else:
            return int(self.djEAVarOut.num)

    def NL_EA_Process_C_2(self, ed_var_out):
        """
        单个人脸对齐, 对人脸框面积最大的人脸，进行对齐比对
        :return: 返回人脸对齐的个数
        """
        self.djEAVarIn.num = 1
        self.djEAVarIn.faces[0] = ed_var_out
        ret = self.FD_SO.NL_EA_Process(self.djEMHandle, self.djEAVarIn, self.djEAVarOut)
        if ret != 0:
            print("EA Process Error Code: " + str(ret))
            self.FD_SO.NL_EM_Exit(self.djEMHandle)
            self.FD_SO.NL_EM_UnloadModel(self.djEMHandle)
            return ret
        else:
            return int(self.djEAVarOut.num)

    def NL_ER_Process_C(self):
        """
        人脸识别提取特征模块
        :return: 人脸特征的个数和人脸输出的所有结果， 返回（非0负数，0）表示异常
        """
        self.djERVarIn.num = self.djEAVarOut.num
        for i in range(self.djEAVarOut.num):
            self.djERVarIn.faces[i] = self.djEAVarOut.faces[i]

        ret = self.FD_SO.NL_ER_Process(self.djEMHandle, self.djERVarIn, self.djERVarOut)

        if ret != 0:
            print("ER Process Error Code: " + str(ret))
            self.FD_SO.NL_EM_Exit(self.djEMHandle)
            self.FD_SO.NL_EM_UnloadModel(self.djEMHandle)
            return ret, 0
        else:
            return int(self.djERVarOut.num), self.djERVarOut

    def NL_EC_Process_C(self, feature1, feature2):
        """
        人脸识别特征对比
        :param feature1: 第一个人脸特征
        :param feature2: 第二个人脸特征
        :return: 返回人脸相似度，非0负数表示异常
        """
        FaceSimily = c_float(0)
        PointSimily = pointer(FaceSimily)
        ret = self.FD_SO.NL_EC_Process(feature1, feature2, PointSimily)
        # print('FaceSimily: ' + str(FaceSimily))

        if ret != 0:
            print("EC Process Error Code: " + str(ret))
            self.FD_SO.NL_EM_Exit(self.djEMHandle)
            self.FD_SO.NL_EM_UnloadModel(self.djEMHandle)
            return ret
        else:
            return FaceSimily.value

    def NL_FD_Exit(self):
        """
        释放内存和模型
        :return:
        """
        ret1 = self.FD_SO.NL_EM_Exit(self.djEMHandle)
        ret2 = self.FD_SO.NL_EM_UnloadModel(self.djEMHandle)
        if ret1 or ret2:
            print("NL_TD_UnloadModel error code:", ret1, ret2)
        return ret1 or ret2