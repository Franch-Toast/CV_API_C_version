from ctypes import *
from enum import IntEnum

# 测试功能模块开关

RGB2YUV_0_TEST          = False # RGB转YUV，模式0
RGB2YUV_1_TEST          = False # RGB转YUV，模式1
YUV2RGB_0_TEST          = False # YUV转RGB888，模式0
YUV2RGB_1_TEST          = False # YUV转RGB888，模式1
YUV2RGB_2_TEST          = False # VYUY转RGB565，模式2，注意python中没有RGB5652RGB的转换，所以结果的R和B会相反。
RGB2GRAY_0_TEST         = False # RGB转GRAY
GRAY2RGB_TEST           = False # GRAY转RGB

PAD_0_TEST              = False # 边缘填充，模式0
PAD_1_TEST              = False # 边缘填充，模式1
PAD_2_TEST              = False # 边缘填充，模式2
RESIZE_0_TEST           = False # 图像缩放
CROP_TEST               = False # 图像裁剪

ROTATE_90_TEST          = False # 图像逆时针旋转90°
ROTATE_180_TEST         = False # 图像逆时针旋转180°
ROTATE_270_TEST         = False # 图像逆时针旋转270°
FLIP_LEFT_RIGHT_TEST    = False # 图像左右翻转
FLIP_TOP_BPTTOM_TEST    = False # 图像上下翻转

GAUSSIAN_BLUR_TEST      = False # 高斯滤波
MEAN_BLUR_TEST          = False # 均值滤波
MEDIAN_BLUR_TEST        = False # 中值滤波


DATA_DUMP               = True # 打印结果（不一致时）

################################### API接口声明 ##################################

lib = cdll.LoadLibrary("../lib/libls_cv.so")

class CtypesEnum(IntEnum):
    @classmethod
    def from_param(cls, obj):
        return int(obj)
class tDType(CtypesEnum):
    DTypeUndefined = 0,
    Float16 = 0x6602,  #'f', 2
    Float32 = 0x6604,  #'f', 4
    Float64 = 0x6608,  #'f', 8
    Int8 = 0x6901,     #'i', 1
    Int16 = 0x6902,    #'i', 2
    Int32 = 0x6904,    #'i', 4
    Int64 = 0x6908,    #'i', 8
    Uint8 = 0x7501,    #'u', 1
    Uint16 = 0x7502,   #'u', 2
    Uint32 = 0x7504,   #'u', 4
    Uint64 = 0x7508,   #'u', 8
    Bool = 0x6201,
    Int4 = 0x6801,

class tShape(Structure):
    _fields_ = [
            ('ndim_', c_uint32),
            ('dims_', c_uint32*3)]
class tData(Structure):
    _fields_ = [('dptr_', c_void_p),
                ('dev_type', c_uint16),
                ('dtype_', c_uint16),
                ('zero_', c_uint16),
                ('scale_', c_float),
                ('shape_', tShape)]

u8_to_int8 = lib.u8_to_int8
u8_to_int8.restype = None
u8_to_int8.argtypes = (POINTER(c_int8), POINTER(c_int8), c_uint32)

int8_to_u8 = lib.int8_to_u8
int8_to_u8.restype = None
int8_to_u8.argtypes = (POINTER(c_int8), POINTER(c_int8), c_uint32)

abs_int8 = lib.abs_int8
abs_int8.restype = None
abs_int8.argtypes = (POINTER(c_int8), POINTER(c_int8), c_uint32)

intx_to_fp32 = lib.intx_to_fp32
intx_to_fp32.restype = c_int32
intx_to_fp32.argtypes = (POINTER(c_float), c_void_p, c_uint32, c_uint32, tDType)

fp32_to_intx = lib.fp32_to_intx
fp32_to_intx.restype = c_int32
fp32_to_intx.argtypes = (c_void_p, POINTER(c_float), c_uint32, c_uint32, tDType)

transpose2d = lib.transpose2d
transpose2d.restype = c_int32
transpose2d.argtypes = (c_void_p, c_void_p, c_uint32, c_uint32, tDType)

rgb2yuv = lib.rgb2yuv
rgb2yuv.restype = c_int32
rgb2yuv.argtypes = (POINTER(tData), POINTER(tData), c_int32)

yuv2rgb = lib.yuv2rgb
yuv2rgb.restype = c_int32
yuv2rgb.argtypes = (POINTER(tData), POINTER(tData), c_int32)

rgb2gray = lib.rgb2gray
rgb2gray.restype = c_int32
rgb2gray.argtypes = (POINTER(tData), POINTER(tData), c_int32)

gray2rgb = lib.gray2rgb
gray2rgb.restype = c_int32
gray2rgb.argtypes = (POINTER(tData), POINTER(POINTER(tData)), c_int32)

crop = lib.crop
crop.restype = c_int32
crop.argtypes = (POINTER(tData), POINTER(tData), POINTER(c_int))

libresize = lib.resize
libresize.restype = c_int32
libresize.argtypes = (POINTER(tData), POINTER(tData), c_int32, POINTER(tData))

rotate = lib.rotate
rotate.restype = c_int32
rotate.argtypes = (POINTER(tData), POINTER(tData), c_int32)

filter = lib.filter
filter.restype = c_int32
filter.argtypes = (POINTER(tData), POINTER(tData), POINTER(tData), c_int32, POINTER(tData))

data_rearrangement = lib.data_rearrangement
data_rearrangement.restype = c_int32
data_rearrangement.argtypes = (POINTER(tData), POINTER(tData), c_int32)

Pad = lib.Pad
Pad.restype = c_int32
Pad.argtypes = (POINTER(tData), POINTER(tData), POINTER(c_int8), c_int32, c_int8, POINTER(tData))

normalize = lib.normalize
normalize.restype = c_int32
normalize.argtypes = (POINTER(tData), POINTER(tData), POINTER(c_int8), POINTER(c_int16))

################################### 运算结果对比 #########################################
import cv2
import numpy as np
img = cv2.imread('./test.jpg', 1)                                           # load image

print('result compare begin')
############################# RGB to YUV (mode = 0) #####################################

if RGB2YUV_0_TEST:
    #check consistence of rgb2yuv(mode=0) result
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)                      #RGB888=>YUV4:4:4
    cv2.imwrite("./opencv/result_rgb2yuv_0.bmp", yuv)

    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    output_data = tData()
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)

    mode = 0
    ret = rgb2yuv(byref(output_data), byref(input_data), mode)
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == yuv
    print("result diffs between opencv and clib of rgb2yuv(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/rgb2yuv_{}_python.txt".format(mode), yuv.reshape(-1, yuv.shape[2]), fmt="%d")
        np.savetxt("./opencv/rgb2yuv_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


############################# RGB to YUV (mode = 1) #####################################

if RGB2YUV_1_TEST:

    #check consistence of rgb2yuv(mode=1) result
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)                    #RGB888=>YUV4:4:4
    cv2.imwrite("./opencv/result_rgb2yuv_1.bmp", yuv)

    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    output_data = tData()
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)

    mode = 1
    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data.dptr_ = cast(carr_data(*data), c_void_p)
    ret = rgb2yuv(byref(output_data), byref(input_data), mode)
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == yuv
    print("result diffs between opencv and clib of rgb2yuv(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/rgb2yuv_{}_python.txt".format(mode), yuv.reshape(-1, yuv.shape[2]), fmt="%d")
        np.savetxt("./opencv/rgb2yuv_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


############################# YUV to RGB (mode = 0) #####################################

if YUV2RGB_0_TEST:

    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    output_data = tData()
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)
    output_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])

    #check consistence of yuv2bgr(mode=0) result
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)  
    bgr1 = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)                     #YUV4:4:4=>RGB888
    cv2.imwrite("./opencv/result_yuv2rgb_0.bmp", bgr1)

    mode = 0
    data = bytearray(yuv)
    carr_data = c_byte * len(data)
    input_data.dptr_ = cast(carr_data(*data), c_void_p)
    ret = yuv2rgb(byref(output_data), byref(input_data), mode)
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == bgr1
    print("result diffs between opencv and clib of yuv2rgb(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/yuv2rgb_{}_python.txt".format(mode), bgr1.reshape(-1, bgr1.shape[2]), fmt="%d")
        np.savetxt("./opencv/yuv2rgb_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


############################# YUV to RGB (mode = 1) #####################################

if YUV2RGB_1_TEST == True:

    #check consistence of yuv2bgr(mode=1) result
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)  
    bgr2 = cv2.cvtColor(yuv, cv2.COLOR_YCrCb2BGR)                     #YUV4:4:4=>RGB888
    cv2.imwrite("./opencv/result_yuv2rgb_1.bmp", bgr2)

    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    data = bytearray(yuv)
    carr_data = c_byte * len(data)
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    output_data = tData()
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)
    output_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])

    mode = 1
    
    ret = yuv2rgb(byref(output_data), byref(input_data), mode)
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == bgr2
    print("result diffs between opencv and clib of yuv2rgb(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/yuv2rgb_{}_python.txt".format(mode), bgr2.reshape(-1, bgr2.shape[2]), fmt="%d")
        np.savetxt("./opencv/yuv2rgb_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


############################## RGB to Gray (mode=0) #####################################

if RGB2GRAY_0_TEST:

    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    output_data = tData()
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)


    #check consistence of rgb2gray(mode=0) result
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                    #RGB => GRAY
    cv2.imwrite("./opencv/result_rgb2gray_0.bmp", gray)

    mode = 0
    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data.dptr_ = cast(carr_data(*data), c_void_p)
    ret = rgb2gray(byref(output_data), byref(input_data), mode)
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == np.expand_dims(gray, axis=2)
    print("result diffs between opencv and clib of rgb2gray(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/rgb2gray_{}_python.txt".format(mode), gray, fmt="%d")
        np.savetxt("./opencv/rgb2gray_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


################################# Gray to RGB ###########################################

if GRAY2RGB_TEST == True:

    #check consistence of gray2rgb(mode=0) result
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    bgr3 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)                   #GRAY=>RGB
    cv2.imwrite("./opencv/result_gray2rgb_0.bmp", bgr3)

    output_data = tData()
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)

    mode = 0
    data = bytearray(gray)
    carr_data = c_byte * len(data)
    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (gray.shape[0], gray.shape[1], 1)
    input_data.dptr_ = cast(carr_data(*data), c_void_p)
    test_data = pointer(input_data)
    ret = gray2rgb(byref(output_data), byref(test_data), mode)
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == bgr3
    print("result diffs between opencv and clib of gray2rgb(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/gray2rgb_{}_python.txt".format(mode), bgr3.reshape(-1, bgr3.shape[2]), fmt="%d")
        np.savetxt("./opencv/gray2rgb_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")

############################### Rotate 90 (mode=0) ######################################

if ROTATE_90_TEST:

    # 逆时针90度

    #check consistence of rotate(90) result
    rotate_90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)            #顺时针旋转90度
    cv2.imwrite("./opencv/result_rotate_90.bmp", rotate_90)

    mode = 2
    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    input_data.dptr_ = cast(carr_data(*data), c_void_p)
    output_data = tData()
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)
    ret = rotate(byref(output_data), byref(input_data), mode)
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == rotate_90
    print("result diffs between opencv and clib of ROTATE_90_CLOCKWISE(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/rotate_90_{}_python.txt".format(mode), rotate_90.reshape(-1, rotate_90.shape[2]), fmt="%d")
        np.savetxt("./opencv/rotate_90_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")

############################## Rotate 180 (mode=1) ######################################

if ROTATE_180_TEST:

    # 180度

    #check consistence of rotate(180) result
    rotate_180 = cv2.rotate(img, cv2.ROTATE_180)                    #顺时针旋转180度
    cv2.imwrite("./opencv/result_rotate_180.bmp", rotate_180)

    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    output_data = tData()
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)

    mode = 1
    ret = rotate(byref(output_data), byref(input_data), mode)
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == rotate_180
    print("result diffs between opencv and clib of ROTATE_180_CLOCKWISE(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/rotate_180_{}_python.txt".format(mode), rotate_180.reshape(-1, rotate_180.shape[2]), fmt="%d")
        np.savetxt("./opencv/rotate_180_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")

############################## Rotate 270 (mode=2) ######################################

if ROTATE_270_TEST == True:    
    
    # 270
    #check consistence of rotate(270) result
    rotate_270 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)    #逆时针旋转90度
    cv2.imwrite("./opencv/result_rotate_270.bmp", rotate_270)

    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    output_data = tData()
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)

    mode = 0
    ret = rotate(byref(output_data), byref(input_data), mode)
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == rotate_270
    print("result diffs between opencv and clib of ROTATE_270_CLOCKWISE(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/rotate_270_{}_python.txt".format(mode), rotate_270.reshape(-1, rotate_270.shape[2]), fmt="%d")
        np.savetxt("./opencv/rotate_270_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


############################# FLIP_TOP_BPTTOM (mode=3) ##################################

if FLIP_TOP_BPTTOM_TEST:

    #check consistence of flip_top_bottom result
    flip_top_bottom = cv2.flip(img, 0)    # 上下翻转
    cv2.imwrite("./opencv/result_flip_top_bottom.bmp", flip_top_bottom)

    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    output_data = tData()
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)

    mode = 3
    ret = rotate(byref(output_data), byref(input_data), mode)
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == flip_top_bottom
    print("result diffs between opencv and clib of flip_top_bottom(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/flip_top_bottom_{}_python.txt".format(mode), flip_top_bottom.reshape(-1, flip_top_bottom.shape[2]), fmt="%d")
        np.savetxt("./opencv/flip_top_bottom_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")

############################# FLIP_LEFT_RIGHT (mode=4) ##################################

if FLIP_LEFT_RIGHT_TEST == True:

    #check consistence of flip_left_right result
    flip_left_right = cv2.flip(img, 1)    # 左右翻转
    cv2.imwrite("./opencv/result_flip_left_right.bmp", flip_left_right)

    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    input_data.dptr_ = cast(carr_data(*data), c_void_p)
    
    output_data = tData()
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)

    mode = 4
    ret = rotate(byref(output_data), byref(input_data), mode)
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == flip_left_right
    print("result diffs between opencv and clib of flip_left_right(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/flip_left_right_{}_python.txt".format(mode), flip_left_right.reshape(-1, flip_left_right.shape[2]), fmt="%d")
        np.savetxt("./opencv/flip_left_right_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


############################### Resize (mode = 0) #######################################

if RESIZE_0_TEST:
    #check consistence of resize result
    resize_result = cv2.resize(img, (600, 800))                            #彩色图像尺寸缩放到(800, 600)
    cv2.imwrite("./opencv/result_resize.bmp", resize_result)

    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    output_data = tData()
    output_data.shape_.ndim_ = 3
    output_data.shape_.dims_ = (800, 600, img.shape[2])
    p_buff = bytearray(800*600*img.shape[2])
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)

    workspace = tData()
    p_workspace  = bytearray(6553600)
    carr_workspace = c_byte * len(p_workspace)
    workspace.shape_.ndim_ = 1
    workspace.shape_.dims_[0] = 6553600
    workspace.dptr_ = cast(carr_workspace(*p_workspace), c_void_p)

    mode = 0
    ret = libresize(byref(output_data), byref(input_data), mode, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == resize_result
    print("result diffs between opencv and clib of resize(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/resize_{}_python.txt".format(mode), resize_result.reshape(-1, resize_result.shape[2]), fmt="%d")
        np.savetxt("./opencv/resize_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")

################################# Blur (mode = 0) #######################################

if MEAN_BLUR_TEST:

    # #check consistence of medianBlur result
    medianblur = cv2.medianBlur(img, 5, None)                       #均值滤波   cv2.medianBlur(src, ksize, dst=None)
    cv2.imwrite("./opencv/result_medianBlur.bmp", medianblur)
    omg = np.array(medianblur)
 
    kernel_size = 5
    kernel_data = np.ones((kernel_size**2, 1), dtype=np.int8)
    kernel = tData()

    kernel.scale_ =  1
    kernel_data = kernel_data * 81                                   # 每次要进行更改
    kernel.shape_.ndim_ = 2
    kernel.shape_.dims_ = (kernel_size, kernel_size)
    carr_kernel = c_byte * kernel_size**2
    kernel.dptr_ = cast(carr_kernel(*kernel_data), c_void_p)

    data = bytearray(img)
    carr_data = c_byte * len(data)

    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    workspace = tData()
    p_workspace  = bytearray(65536000)
    carr_workspace = c_byte * len(p_workspace)
    workspace.shape_.ndim_ = 1
    workspace.shape_.dims_[0] = 65536000
    workspace.dptr_ = cast(carr_workspace(*p_workspace), c_void_p)

    output_data = tData()
    output_data.scale_ = 1.0
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)

    mode = 0
    ret = filter(byref(output_data), byref(input_data), byref(kernel), mode, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)


    compare = result == omg
    print("result diffs between opencv and clib of blur_filter(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))

    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/blur_filter_{}_python.txt".format(mode), omg.reshape(-1, omg.shape[2]), fmt="%d")
        np.savetxt("./opencv/blur_filter_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


################################# Blur (mode = 1) #######################################

if GAUSSIAN_BLUR_TEST:

    import math # 用于获取pi

    cv_gaussiankernel = cv2.getGaussianKernel(5,1.1)
    cv_gaussiankernel_two = np.matmul(cv_gaussiankernel,cv_gaussiankernel.T)
    cv_gaussiankernel_two /= np.sum(cv_gaussiankernel_two)
    # 用于验证高斯核

    #check consistence of GaussianBlur result
    om = cv2.GaussianBlur(img, (5, 5), 1.1,1.1)                 #高斯滤波   cv2.GaussianBlur(src, ksize, sigmaX, sigmaY, borderType)
    cv2.imwrite("./opencv/result_GaussianBlur.bmp", om)
    omg = np.array(om)

    blur_filter = omg

    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data.dptr_ = cast(carr_data(*data), c_void_p)


    mode = 1
    kernel_data = np.ones((25, 1), dtype=np.int8)

    # 下面是对高斯核的计算

    sigma = 1.1
    origin_data = np.zeros(25) # 初始化一个25长度的小数数组
    count = 0


    carr_data = c_float * len(origin_data) # 定义了类型 浮点型数组
    # carr_data = c_byte * len(kernel_temp2)

    c_float_p = POINTER(c_float)
    origin = c_float_p(carr_data(*origin_data))
    
    kernel_data = kernel_data * 82
    kernel = tData()

    # kernel.scale_ = math.floor(np.log2(127 / origin_data[int(25/2)]))

    kernel.shape_.ndim_ = 2
    kernel.shape_.dims_ = (5, 5)
    carr_kernel = c_byte * 25
    kernel.dptr_ = cast(carr_kernel(*kernel_data), c_void_p)


    output_data = tData()
    output_data.scale_ = 1.0
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)

    workspace = tData()
    p_workspace  = bytearray(65536000)
    carr_workspace = c_byte * len(p_workspace)
    workspace.shape_.ndim_ = 1
    workspace.shape_.dims_[0] = 65536000
    workspace.dptr_ = cast(carr_workspace(*p_workspace), c_void_p)

    ret = filter(byref(output_data), byref(input_data), byref(kernel), mode, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == blur_filter
    print("result diffs between opencv and clib of Gaussian_filter(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP :
        np.savetxt("./opencv/blur_filter_{}_python.txt".format(mode), blur_filter.reshape(-1, blur_filter.shape[2]), fmt="%d")
        np.savetxt("./opencv/blur_filter_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")
    

################################# Blur (mode = 2) #######################################

if MEDIAN_BLUR_TEST:
    
    om = cv2.medianBlur(img,3)
    cv2.imwrite("./opencv/result_medianBlur.bmp", om)

    omg = np.array(om)

    data = bytearray(img)
    carr_data = c_byte * len(data)
    # np.savetxt("./opencv/./compare_test_data.txt",data,fmt="%d")
    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    input_data.dptr_ = cast(carr_data(*data), c_void_p)


    kernel_data = np.ones((9, 1), dtype=np.int8)
    kernel_data = kernel_data * 85
    kernel = tData()
    kernel.scale_ = 7
    kernel.shape_.ndim_ = 2
    kernel.shape_.dims_ = (3, 3)
    carr_kernel = c_byte * 9
    kernel.dptr_ = cast(carr_kernel(*kernel_data), c_void_p)

    workspace = tData()
    p_workspace  = bytearray(65536000)
    carr_workspace = c_byte * len(p_workspace)
    workspace.shape_.ndim_ = 1
    workspace.shape_.dims_[0] = 65536000
    workspace.dptr_ = cast(carr_workspace(*p_workspace), c_void_p)


    mode = 2
    output_data = tData()
    output_data.scale_ = 1.0
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)


    ret = filter(byref(output_data), byref(input_data), byref(kernel), mode, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)
    # img_result = Image.fromarray(result)
    # img_result.save("./opencv/blur_filter_c.bmp")

    compare = result == omg
    print("result diffs between opencv and clib of median_filter(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/median_filter_{}_python.txt".format(mode), omg.reshape(-1, omg.shape[2]), fmt="%d")
        np.savetxt("./opencv/median_filter_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")

################################# Pad (mode=0) ##########################################

if PAD_0_TEST:

    pads_param = (9,7,10,8) # 左上右下
    pads_array = (c_int8 * 4)(pads_param[1], pads_param[0], pads_param[3], pads_param[2]) # 传入函数的值，上左下右

    # 常数0填充
    om = cv2.copyMakeBorder(img, 7, 8, 9, 10, cv2.BORDER_CONSTANT, value=(0,0,0))
    cv2.imwrite("./opencv/result_pad_0.bmp", om)

    omg = np.array(om)

    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    input_data.dptr_ = cast(carr_data(*data), c_void_p)


    p_pads = pointer(pads_array)

    output_data = tData()
    data_size = (img.shape[0] + pads_array[0] + pads_array[2]) * (img.shape[1] + pads_array[1] + pads_array[3]) * img.shape[2]
    p_buff = bytearray(data_size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)

    workspace = tData()
    p_workspace  = bytearray(6553600)
    carr_workspace = c_byte * len(p_workspace)
    workspace.shape_.ndim_ = 1
    workspace.shape_.dims_[0] = 6553600
    workspace.dptr_ = cast(carr_workspace(*p_workspace), c_void_p)

    mode = 0
    fill_data = 0 # 填充常数0
    ret = Pad(byref(output_data), byref(input_data), p_pads.contents, mode, fill_data, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == omg
    print("result diffs between opencv and clib of Pad(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/Pad_{}_python.txt".format(mode), omg.reshape(-1, omg.shape[2]), fmt="%d")
        np.savetxt("./opencv/Pad_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")

################################# Pad (mode=1) ##########################################

if PAD_1_TEST:

    # check consistence of pad result, edge

    # edge填充
    om = cv2.copyMakeBorder(img, 7, 8, 9, 10, cv2.BORDER_REPLICATE)
    cv2.imwrite("./opencv/result_pad_1.bmp", om)

    omg = np.array(om)

    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    pads_param = (9,7,10,8) # 左上右下
    pads_array = (c_int8 * 4)(pads_param[1], pads_param[0], pads_param[3], pads_param[2]) # 传入函数的值，上左下右

    p_pads = pointer(pads_array)

    output_data = tData()
    data_size = (img.shape[0] + pads_array[0] + pads_array[2]) * (img.shape[1] + pads_array[1] + pads_array[3]) * img.shape[2]
    p_buff = bytearray(data_size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)

    workspace = tData()
    p_workspace  = bytearray(6553600)
    carr_workspace = c_byte * len(p_workspace)
    workspace.shape_.ndim_ = 1
    workspace.shape_.dims_[0] = 6553600
    workspace.dptr_ = cast(carr_workspace(*p_workspace), c_void_p)

    mode = 1
    fill_data = c_byte(0) # 填充常数0
    ret = Pad(byref(output_data), byref(input_data), p_pads.contents, mode, fill_data, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == omg
    print("result diffs between opencv and clib of Pad(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/Pad_{}_python.txt".format(mode), omg.reshape(-1, omg.shape[2]), fmt="%d")
        np.savetxt("./opencv/Pad_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")

################################# Pad (mode=2) ##########################################

if PAD_2_TEST:

    # check consistence of pad result, reflect

    # reflect填充
    om = cv2.copyMakeBorder(img, 7, 8, 9, 10, cv2.BORDER_REFLECT)
    cv2.imwrite("./opencv/result_pad_2.bmp", om)

    omg = np.array(om)

    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    pads_param = (9,7,10,8) # 左上右下
    pads_array = (c_int8 * 4)(pads_param[1], pads_param[0], pads_param[3], pads_param[2]) # 传入函数的值，上左下右

    p_pads = pointer(pads_array)

    output_data = tData()
    data_size = (img.shape[0] + pads_array[0] + pads_array[2]) * (img.shape[1] + pads_array[1] + pads_array[3]) * img.shape[2]
    p_buff = bytearray(data_size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)

    workspace = tData()
    p_workspace  = bytearray(6553600)
    carr_workspace = c_byte * len(p_workspace)
    workspace.shape_.ndim_ = 1
    workspace.shape_.dims_[0] = 6553600
    workspace.dptr_ = cast(carr_workspace(*p_workspace), c_void_p)

    mode = 2
    fill_data = 0 # 填充常数0
    ret = Pad(byref(output_data), byref(input_data), p_pads.contents, mode, fill_data, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == omg
    print("result diffs between opencv and clib of Pad(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/Pad_{}_python.txt".format(mode), omg.reshape(-1, omg.shape[2]), fmt="%d")
        np.savetxt("./opencv/Pad_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")



##################################### crop ##############################################

if CROP_TEST:
# check consistence of crop result

    # check consistence of crop result
    crop_param = (100,20,901,801) # 左，上，右，下

    
    om = cv2.getRectSubPix(img,(901-100,801-20),(int((100+901)/2),int((20+801)/2)))
    cv2.imwrite("./opencv/result_crop.bmp", om)

    omg = np.array(om)

    box_array = (c_int32 * 4)(crop_param[0], crop_param[1], crop_param[2], crop_param[3])
    box = pointer(box_array)

    # mode = 0
    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    output_data = tData()
    p_buff = bytearray((crop_param[2] - crop_param[0]) * (crop_param[3] - crop_param[1]) *3)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)

    ret = crop(byref(output_data), byref(input_data), box.contents)
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == omg   # 注意超出图片范围，PIL会填充0，c代码直接截断
    print("result diffs between opencv and clib of crop:{}, percentage：{:.2f}%"\
        .format(np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./opencv/crop_python.txt", omg.reshape(-1, omg.shape[2]), fmt="%d")
        np.savetxt("./opencv/crop_clib.txt", result.reshape(-1, result.shape[2]), fmt="%d")

    
print('result compare completed')


##################################### YUV转RGB565，模式2 ###########################################

if YUV2RGB_2_TEST == True:

    
    with open('./srcWaveId_640x480.yuv','rb') as fp:
        data_bytes = fp.read(640*480*2)
    
    data_temp = np.frombuffer(data_bytes,'B')


    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (480, 640, 3)
    data = bytearray(data_temp)
    carr_data = c_byte * len(data)
    input_data.dptr_ = cast(carr_data(*data_temp), c_void_p)

    output_data = tData()
    p_buff = bytearray(614400)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)
    output_data.shape_.dims_ = (480, 640, 2)

    mode = 2
    
    ret = yuv2rgb(byref(output_data), byref(input_data), mode)
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    temp = cv2.cvtColor(result, cv2.COLOR_BGR5652RGB)# 将获取的BGR565数据转换为RGB888
    cv2.imwrite("./opencv/result_yuv2rgb_test.bmp", temp)# 将RGB888转为可以查看的位图






