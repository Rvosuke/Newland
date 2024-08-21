# -*- coding: utf-8 -*-
from ctypes import *
import os
import cv2
import numpy as np
from .ft2 import ft


# -----------人脸多属性结构体定义------------------
class Struct_Handle(Structure):
    _fields_ = [("pvModel", c_void_p), ("pvBuf", c_void_p), ("qwBufLen", c_longlong)]


class Struct_MAP_VarIn(Structure):
    _fields_ = [("dwMode", c_int), ("pubyIm", c_char_p), ("dwBatchSize", c_int), ("dwWidth", c_int),
                ("dwHeight", c_int), ("dwChannel", c_int), ("pfX", c_float * 2 * 128), ("pfY", c_float * 2 * 128)]


class Struct_MAP_Ver(Structure):
    _fields_ = [("dwMajorVer", c_int), ("dwMinorVer", c_int), ("dwRevisonVer", c_int), ("dwReleaseFlag", c_int),
                ("dwModelMinVerFlag", c_int)]


class Struct_MAP_VarOut(Structure):
    _fields_ = [("dwNum", c_int), ("pdwGender", c_int * 128), ("pdwAge", c_int * 128), ("pdwPitch", c_int * 128),
                ("pdwYaw", c_int * 128), ("pdwEmotion", c_int * 128), ("pdwGlasses", c_int * 128),
                ("pdwMask", c_int * 128),
                ("pdwOcclusion", c_int * 128), ("pfBlur", c_float * 128), ("pfBrightness", c_float * 128),
                ("pfGenderConfidence", c_float * 128), ("pfEmotionConfidence", c_float * 128),
                ("pfGlassesConfidence", c_float * 128),
                ("pfMaskConfidence", c_float * 128), ("pfOcclusionConfidence", c_float * 128),
                ("pfX", c_float * 2 * 128), ("pfY", c_float * 2 * 128)]


class NlFaceMultiAttr(object):

    def __init__(self, libNamePath):
        if not os.path.exists(libNamePath):
            print("library file not exit! " + str(libNamePath))
            return -1001
        else:
            self.MAP_SO = cdll.LoadLibrary(libNamePath)  # linux版本

        # ---------人脸属性指定参数-------------------
        self.showResult = True
        # 指定函数参数类型
        self.MAP_SO.NL_MAP_GetVer.argtypes = (POINTER(Struct_Handle), POINTER(Struct_MAP_Ver))
        self.MAP_SO.NL_MAP_GetVer.restype = c_int
        self.MAP_SO.NL_MAP_Command.argtypes = (POINTER(Struct_Handle), c_char_p)
        self.MAP_SO.NL_MAP_Command.restype = c_int
        self.MAP_SO.NL_MAP_Init.argtypes = (POINTER(Struct_Handle),)
        self.MAP_SO.NL_MAP_Init.restype = c_int
        self.MAP_SO.NL_MAP_Process.argtypes = (
            POINTER(Struct_Handle), POINTER(Struct_MAP_VarIn), POINTER(Struct_MAP_VarOut))
        self.MAP_SO.NL_MAP_Process.restype = c_int
        self.MAP_SO.NL_MAP_Exit.argtypes = (POINTER(Struct_Handle),)
        self.MAP_SO.NL_MAP_Exit.restype = c_int
        self.MAP_SO.NL_MAP_UnloadModel.argtypes = (POINTER(Struct_Handle),)
        self.MAP_SO.NL_MAP_UnloadModel.restype = c_int

        # 人脸属性，初始化：结构体变量和函数
        self.ret = 0  # 返回值
        self.faceNum = 1  # 测试人脸的个数
        self.djMAPHandle = Struct_Handle()  # 句柄结构体变量定义
        self.djMAPVarIn = Struct_MAP_VarIn()  # 输入结构体变量定义
        self.djMAPVarOut = Struct_MAP_VarOut()  # 输出结构体变量定义

    def NL_EM_ComInit(self, rootPath):
        """
        人脸多属性初始化，加载模型和配置文件
        :param rootPath: 配置文件路径，以及模型路径
        :return:
        """
        if not os.path.exists(rootPath):
            print("NL_EM_ComInit Config or model file not exit!")
            return -2501
        ret = self.MAP_SO.NL_MAP_Command(self.djMAPHandle, rootPath)
        if ret != 0:
            print("NL_EM_ComInit Command error code: " + str(ret))
            return ret
        ret = self.MAP_SO.NL_MAP_Init(self.djMAPHandle)
        if ret != 0:
            print("NL_EM_ComInit Init error code: " + str(ret))
            ret = self.MAP_SO.NL_MAP_Exit(self.djMAPHandle)
            ret = self.MAP_SO.NL_MAP_UnloadModel(self.djMAPHandle)
            return ret

    def NL_EM_InputImg(self, inputImg):
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

    def NL_EM_InitVarIn(self, src_RGB):
        """
        人脸多属性输入源参数设置
        :param src_RGB: 读取的一帧图片，或者一张图片
        :return: 返回0，非0负数表示异常
        """
        h, w, c = src_RGB.shape
        self.djMAPVarIn.dwMode = 1  # dwMode=1 表示输入大图，0表示输入裁剪后的图
        self.djMAPVarIn.dwChannel = c
        self.djMAPVarIn.dwWidth = w
        self.djMAPVarIn.dwHeight = h
        self.djMAPVarIn.pubyIm = src_RGB.astype(np.uint8).tostring()
        self.djMAPVarIn.dwBatchSize = self.faceNum
        if h > 1:
            return 0
        else:
            print("NL_FD_InitVarIn Error!")
            return -1001

    def NL_EM_bbox(self, fFDCoordinates, img):
        """
        人脸坐标信息，每4个点代表一张人脸，也可以通过人脸检测的SDK得到对应的坐标, 目前只识别单个人脸，可以扩展
        :param bbox: 利用人脸检测，获得的坐标信息，如果没有利用人脸检测，则需要改写此函数，将self.fFDCoordinates
                     改写，比如，self.fFDCoordinates = [294, 184, 366, 278, 170, 176, 242, 276, 542, 176, 620, 274, 38, 316, 118, 422,
                      666, 316, 748, 420, 294, 36, 368, 136, 670, 174, 752, 278, 40, 178, 118, 276,
                      422, 40, 490, 136, 168, 322, 246, 418, 546, 40, 622, 132, 48, 42, 106, 134,
                      674, 36, 744, 126, 164, 50, 232, 142, 538, 322, 622, 424, 292, 322, 374, 422,
                      412, 166, 506, 276] 共10个人脸，self.faceNum要等于10.

        :param img: 视频流一帧图片，为了画出人脸框
        :return: 将重绘的图片返回
        """

        # 对图片中的人脸位置进行赋值给djMAPVarIn
        for i in range(self.faceNum):
            self.djMAPVarIn.pfX[i][0] = fFDCoordinates[i * 4]
            self.djMAPVarIn.pfY[i][0] = fFDCoordinates[i * 4 + 1]
            self.djMAPVarIn.pfX[i][1] = fFDCoordinates[i * 4 + 2]
            self.djMAPVarIn.pfY[i][1] = fFDCoordinates[i * 4 + 3]
        return img

    def NL_EM_Process_C(self):
        """
        人脸多属性处理函数
        :return: 返回人脸个数，非0负数表示异常
        """
        ret = self.MAP_SO.NL_MAP_Process(self.djMAPHandle, self.djMAPVarIn, self.djMAPVarOut)
        if ret != 0:
            print("Process Error code:" + str(ret))
            return ret
        return int(self.djMAPVarOut.dwNum)

    def result_show_2(self):
        """
        单个人脸多属性结果输出
        :return: 返回人脸多属性信息列表
        """
        user_em_info = []
        em_obj = {}
        for i in range(int(self.djMAPVarOut.dwNum)):
            em_obj['gender'] = self.djMAPVarOut.pdwGender[i]
            em_obj['age'] = self.djMAPVarOut.pdwAge[i]
            em_obj['emotion'] = self.djMAPVarOut.pdwEmotion[i]
            em_obj['mask'] = self.djMAPVarOut.pdwMask[i]
            em_obj['glasses'] = self.djMAPVarOut.pdwGlasses[i]
            em_obj['occlusion'] = self.djMAPVarOut.pdwOcclusion[i]
            em_obj['blur'] = self.djMAPVarOut.pfBlur[i]
            em_obj['brightness'] = self.djMAPVarOut.pfBrightness[i]
            user_em_info.append(em_obj)
            break
        print(user_em_info)
        return user_em_info

    def result_show(self, img):
        """
        多人脸多属性结果输出
        :return: 返回标识后的结果图片和人脸多属性的结果信息列表
        """
        user_em_info = []
        em_obj = {}
        emotion = ['生气', '恶心', '害怕', '开心', '无表情', '伤心', '惊讶', '哈欠']
        for i in range(int(self.djMAPVarOut.dwNum)):
            em_obj['gender'] = self.djMAPVarOut.pdwGender[i]
            em_obj['age'] = self.djMAPVarOut.pdwAge[i]
            em_obj['emotion'] = self.djMAPVarOut.pdwEmotion[i]
            em_obj['mask'] = self.djMAPVarOut.pdwMask[i]
            em_obj['glasses'] = self.djMAPVarOut.pdwGlasses[i]
            em_obj['occlusion'] = self.djMAPVarOut.pdwOcclusion[i]
            em_obj['blur'] = self.djMAPVarOut.pfBlur[i]
            em_obj['brightness'] = self.djMAPVarOut.pfBrightness[i]
            user_em_info.append(em_obj)
            if em_obj['gender'] == 0:
                gender = '男'
            elif em_obj['gender'] == 1:
                gender = '女'
            if int(em_obj['glasses']) == 0:
                glasses = '没有戴眼镜'
            elif int(em_obj['glasses']) == 1:
                glasses = '戴眼镜'
            elif int(em_obj['glasses']) == 2:
                glasses = '戴有色眼镜'
            else:
                glasses = ''
            if int(em_obj['mask']) == 0:
                mask = '没有戴口罩'
            else:
                mask = '戴口罩'
            obj_pfx = self.djMAPVarOut.pfX[i]
            obj_pfy = self.djMAPVarOut.pfY[i]
            #显示人脸你属性分析结果
#             if 0 < int(obj_pfx[0]) + 10 < 640 and 0 < int(obj_pfy[0]) - 30 < 480:
            img = ft.draw_text(img, (int(obj_pfx[1]) + 0, int(obj_pfy[0]) + 30),
                               '{}'.format(gender),int((int(obj_pfx[1]) - int(obj_pfx[0])) / 8), (255, 0, 0))
            img = ft.draw_text(img, (int(obj_pfx[1]) + 0, int(obj_pfy[0]) + 60),
                               '{}岁'.format(em_obj['age']),int((int(obj_pfx[1]) - int(obj_pfx[0])) / 8), (255, 0, 0))
            img = ft.draw_text(img, (int(obj_pfx[1]) + 0, int(obj_pfy[0]) + 90),
                               '{}'.format(emotion[em_obj['emotion']]),int((int(obj_pfx[1]) - int(obj_pfx[0])) / 8),(255,0,0))
            img = ft.draw_text(img, (int(obj_pfx[1]) + 0, int(obj_pfy[0]) + 120),
                               '{}'.format(glasses),int((int(obj_pfx[1]) - int(obj_pfx[0])) / 8), (255, 0, 0))
    
#             img = ft.draw_text(img, (int(obj_pfx[0]) + 10, int(obj_pfy[0]) - 30),
#                                '{},{}岁{}'.format(gender, em_obj['age'], mask),
#                                int((int(obj_pfx[1]) - int(obj_pfx[0])) / 8), (255, 0, 0))
#             img = ft.draw_text(img, (int(obj_pfx[0]) + 10, int(obj_pfy[0]) - 60),
#                                '{}'.format(glasses),
#                                int((int(obj_pfx[1]) - int(obj_pfx[0])) / 8), (255, 0, 0))
#             img = ft.draw_text(img, (int(self.djMAPVarOut.pfX[i][0]) + 10, int(self.djMAPVarOut.pfY[i][0]) - 90),
#                                    '{}'.format(emotion[em_obj['emotion']]),
#                                    int((int(obj_pfx[1]) - int(obj_pfx[0])) / 8), (255, 0, 0))
        return img

    def NL_EM_Exit(self):
        """
        释放内存和释放模型
        :return:
        """
        ret = self.MAP_SO.NL_MAP_Exit(self.djMAPHandle)
        ret = self.MAP_SO.NL_MAP_UnloadModel(self.djMAPHandle)
        if ret != 0:
            print("UnloadModel Error code:", ret)
            return ret
        return ret
