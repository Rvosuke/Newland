# -*- coding: utf-8 -*-
import os
from configparser import ConfigParser
from ctypes import *
from enum import Enum
import faulthandler

faulthandler.enable()


class INI_CONFIG(Structure):
    _fields_ = [("url_num", c_int), ("NewlandUrls", c_char * 256 * 6),
                ("file_num", c_int), ("NewlandFiles", c_char * 256 * 6),
                ("src_vedio", c_char), ("src_rotation", c_int),
                ("server_ip", c_char * 15), ("server_port", c_int),
                ("face_face_min_w", c_int), ("face_zt_face_min_w", c_int),
                ("xq_save_path", c_char * 256), ("log_save_path", c_char * 256),
                ("server_url", c_char * 128)]


class NL_IMAGE_TYPE_E(Enum):
    NL_IMAGE_TYPE_U8C1 = 0x0
    NL_IMAGE_TYPE_S8C1 = 0x1

    NL_IMAGE_TYPE_YUV420SP = 0x2
    NL_IMAGE_TYPE_YUV422SP = 0x3
    NL_IMAGE_TYPE_YUV420P = 0x4
    NL_IMAGE_TYPE_YUV422P = 0x5
    NL_IMAGE_TYPE_S8C2_PACKAGE = 0x6
    NL_IMAGE_TYPE_S8C2_PLANAR = 0x7

    NL_IMAGE_TYPE_S16C1 = 0x8
    NL_IMAGE_TYPE_U16C1 = 0x9

    NL_IMAGE_TYPE_U8C3_PACKAGE = 0xa
    NL_IMAGE_TYPE_U8C3_PLANAR = 0xb

    NL_IMAGE_TYPE_S32C1 = 0xc
    NL_IMAGE_TYPE_U32C1 = 0xd

    NL_IMAGE_TYPE_S64C1 = 0xe
    NL_IMAGE_TYPE_U64C1 = 0xf


class NL_SINGLE_IMG_DATA_T(Structure):
    _fields_ = [
        ('ucLineIndex', c_int), ('u8LineNum', c_int),
        ('ptSpecData', c_void_p), ('ptShowData', c_void_p),
        ('u64VirAddr', POINTER(c_ubyte)), ('u32Stride', c_uint),
        ('u32Width', c_uint), ('u32Height', c_uint), ('eImgType', c_int)
    ]


class FOCUS_POS_T(Structure):
    _fields_ = [('x', c_uint), ('y', c_uint)]


class FOCUS_AREA_T(Structure):
    _fields_ = [('tnPoints', FOCUS_POS_T * 4)]


class FOCUS_AREA_ARRAY_T(Structure):
    _fields_ = [('s32AreaNum', c_uint), ('ptAreaPos', FOCUS_AREA_T)]


class NL_BOOL(Enum):
    NL_FALSE = 0
    NL_TRUE = 1


class ENCODING_TYPE_E(Enum):
    NL_H264 = 0


class RTSP_URL_T(Structure):
    _fields_ = [('num', c_uint), ('appname', c_char * 16), ('src_type', c_int),
                ('url', (c_char * 128) * 16), ('file', (c_char * 128) * 16),
                ('key', (c_char * 128) * 16), ('ip', (c_char * 32) * 16), ('iNetRestartIime', c_int)]


class OUT_SIZE_T(Structure):
    _fields_ = [('uiOutW', c_uint), ('uiOutH', c_uint)]


class MEIDA_CONFIG_T(Structure):
    _fields_ = [('uiCameraW', c_uint), ('uiCameraH', c_uint),
                ('tOutputSize', OUT_SIZE_T * 4), ('bNeedCut', c_int),
                ('ucOutNum', c_uint), ('sTimeout', c_int), ('lOutPutPicGap', c_long)]


class IMG_DATA_T(Structure):
    _fields_ = [('pShowFrame', c_void_p), ('ucScaleNum', c_uint), ('bCutted', c_int),
                ('tnBgrData', NL_SINGLE_IMG_DATA_T * 4), ('tnBgrScaleData', NL_SINGLE_IMG_DATA_T * 4)]


class MAIN_THREAD_PARAM_T(Structure):
    _fields_ = [('u8MediaIndex', c_char_p), ('u32RgnHandle', c_uint)]


s_u8nMediaIndex = (c_uint * 16)()
s_bMainStop = 0


class NLRtspApi(object):
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
            self.media_so = cdll.LoadLibrary(libNamePath)

        self.media_so.read_ini.argtypes = (c_char_p,)
        self.media_so.read_ini.restype = c_int
        self.media_so.get_url_num_from_ini.restype = c_int
        self.media_so.get_url_from_ini.argtypes = (c_int,)
        self.media_so.get_url_from_ini.restype = c_char_p
        self.media_so.nl_media_data_release.argtypes = (POINTER(NL_SINGLE_IMG_DATA_T),)
        self.media_so.nl_media_data_release.restype = c_int
        # self.media_so.nl_media_vgs_quad_rangle.argtypes = (c_char_p, POINTER(FOCUS_AREA_ARRAY_T), NL_BOOL, c_int, c_int, c_void_p)
        # self.media_so.nl_media_vgs_quad_rangle.restype = c_int
        self.media_so.nl_media_init.restype = c_int
        self.media_so.nl_media_resource_config.argtypes = (POINTER(c_uint), c_uint, POINTER(MEIDA_CONFIG_T), POINTER(RTSP_URL_T),
                                                           c_uint, c_uint, c_int, c_int)
        self.media_so.nl_media_resource_config.restype = c_int
        self.media_so.nl_media_start.argtypes = (POINTER(c_uint), c_uint)
        self.media_so.nl_media_start.restype = c_int
        self.media_so.nl_media_read.argtypes = (c_uint, POINTER(IMG_DATA_T))
        self.media_so.nl_media_read.restype = c_int
        self.media_so.nl_media_stop.restype = c_int

        self.ini_config = INI_CONFIG()
        self.single_img_data = NL_SINGLE_IMG_DATA_T()
        self.image_type_e = 0xa
        self.focus_pos = FOCUS_POS_T()
        self.focus_area = FOCUS_AREA_T()
        self.focus_area_array = FOCUS_AREA_ARRAY_T()
        self.rtsp_url = RTSP_URL_T()
        self.out_size = OUT_SIZE_T()
        self.media_config = (MEIDA_CONFIG_T * 16)()
        self.img_data_0 = IMG_DATA_T()
        self.img_data_1 = IMG_DATA_T()

    def read_ini(self, path):
        """
        读取ini配置文件
        """
        ret = self.media_so.read_ini(path)
        if ret != 0:
            print("read NL_PIG.ini ERR!\n")
            return -1
        else:
            return int(ret)

    def get_url_num_from_ini(self):
        """
        获取rtsp地址个数
        """
        rtsp_url_num = self.media_so.get_url_num_from_ini()
        if rtsp_url_num:
            return rtsp_url_num

    def get_url_from_ini(self, n):
        """
        获取rtsp的地址
        """
        rtsp_url = self.media_so.get_url_from_ini(n)
        if rtsp_url:
            return rtsp_url
        else:
            return None

    def nl_media_data_release(self, single_img_data):
        """
        释放nl_media_read获取的mmz内存，在nl_media_read后或者算法处理后必须调用该接口释放内存，否则会造成内存泄露
        """
        ret = self.media_so.nl_media_data_release(single_img_data)
        if ret != 0:
            print('释放失败')
        else:
            return int(ret)

    def nl_media_init(self):
        """
        初始化媒体模块
        """
        ret = self.media_so.nl_media_init()
        if ret != 0:
            print('初始化媒体模块失败')
            return -1
        else:
            return int(ret)

    def nl_media_resource_config(self, ptMediaIndex, u8MediaLines, url_dict):
        """
        1.分配媒体句柄
        2.海思资源配置（sys、vdec、vpss、vo）
        """
        self.rtsp_url.num = u8MediaLines
        self.rtsp_url.src_type = 0
        self.rtsp_url.iNetRestartIime = 10
        print(int(url_dict['url_num']))
        for i in range(int(url_dict['url_num'])):
            print(url_dict['urls'][i])
            for index, s in enumerate(url_dict['urls'][i]):
                self.rtsp_url.url[i][index] = c_char(s)
        tMedia = self.media_config
        for i in range(u8MediaLines):
            # tMedia[i].uiCameraW = 1920
            # tMedia[i].uiCameraH = 1080
            tMedia[i].tOutputSize[0].uiOutW = 1280
            tMedia[i].tOutputSize[0].uiOutH = 960
            tMedia[i].tOutputSize[1].uiOutW = 640
            tMedia[i].tOutputSize[1].uiOutH = 480
            # tMedia[i].tOutputSize[0].uiOutW = 640
            # tMedia[i].tOutputSize[0].uiOutH = 480

            tMedia[i].sTimeout = 300
            tMedia[i].ucOutNum = 2
            # tMedia[i].eType = type_list[i]
            tMedia[i].bNeedCut = 0
            # tMedia[i].bNeedShow = 0

        ret = self.media_so.nl_media_resource_config(ptMediaIndex, u8MediaLines, tMedia, self.rtsp_url, 1920, 1080, 0, 2)
        if ret != 0:
            print('配置失败')
            return -1
        else:
            return int(ret)

    def nl_media_start(self, ptMediaIndex, u8MediaLines):
        """
        启动rtsp客户端，通过url地址访问摄像头，开始接收摄像头传过来的视频流
        启动海思相关线程
        """

        ret = self.media_so.nl_media_start(ptMediaIndex, u8MediaLines)
        if ret != 0:
            print('启动失败')
            return -1
        else:
            return int(ret)

    def nl_media_read(self, u8MediaIndex):
        """
        如果read的通道需要show的话，那么一定要调用show接口，否则会造成内存溢出，如果不需要read的话就不要show了
        """
        if u8MediaIndex == 0:
            read_img_data = self.img_data_0
        elif u8MediaIndex == 1:
            read_img_data = self.img_data_1
        else:
            read_img_data = self.img_data_0
        ret = self.media_so.nl_media_read(u8MediaIndex, read_img_data)
        if ret != 0:
            # print('读取失败')
            return -1
        else:
            return int(ret)

    def nl_media_show(self, u8MediaIndex, pShowData):
        """
        通过调用HI_MPI_VO_SendFrame接口显示视频帧并释放一帧通道图像
        """
        ret = self.media_so.nl_media_show(u8MediaIndex, pShowData)
        if ret != 0:
            print('显示失败')
            return -1
        else:
            return int(ret)

    def nl_media_stop(self):
        """
        退出媒体通路（1.关闭相关线程;2.销毁相关资源）
        """
        ret = self.media_so.nl_media_stop()
        if ret != 0:
            print('退出媒体通路失败')
            return -1
        else:
            return int(ret)


# if __name__ == '__main__':

    # for i in range(nl_rtsp_api.img_data.ucScaleNum):
    #     nl_rtsp_api.nl_free_mmz_cached(nl_rtsp_api.img_data.tnBgrScaleData[i])


