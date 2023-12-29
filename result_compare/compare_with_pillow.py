from ctypes import *
from enum import IntEnum


# 测试功能模块开关

PAD_0_TEST              = True # 边缘填充，模式0
RESIZE_0_TEST           = True # 图像缩放
CROP_TEST               = True # 图像裁剪
RGB2GRAY_TEST           = True # RGB转GRAY

ROTATE_90_TEST          = True # 图像逆时针旋转90°
ROTATE_180_TEST         = True # 图像逆时针旋转180°
ROTATE_270_TEST         = True # 图像逆时针旋转270°
FLIP_LEFT_RIGHT_TEST    = True # 图像左右翻转
FLIP_TOP_BPTTOM_TEST    = True # 图像上下翻转

GAUSSIAN_BLUR_TEST      = True # 高斯滤波
MEAN_BLUR_TEST          = True # 均值滤波
MEDIAN_BLUR_TEST        = True # 中值滤波
MIN_BLUR_TEST           = True # 最小值滤波
MAX_BLUR_TEST           = True # 最大值滤波

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

############################# 运算结果对比 #####################################
import numpy as np
from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps
# im = Image.open('test.jpg')                                    # 读取的图像数据格式为BGRBGRBGR
im = Image.open('./test.jpg')

img = np.array(im)
R = np.expand_dims(img[:,:,0], axis=2)
G = np.expand_dims(img[:,:,1], axis=2)
B = np.expand_dims(img[:,:,2], axis=2)
img = np.concatenate((B, G, R), axis = 2)                       # BGRBGRBGR==>RGBRGBRGB


print('result compare begin')
########################### RGB to Gray ##################################

if RGB2GRAY_TEST:
    # check consistence of rgb2gray result
    om = im.convert('L')                                           # 彩色转灰度图像
    gray = np.array(om)
    om.save("./pillow/rgb2gray_0_pillow.bmp")

    mode = 0
    img = np.array(im)
    R = np.expand_dims(img[:,:,0], axis=2)
    G = np.expand_dims(img[:,:,1], axis=2)
    B = np.expand_dims(img[:,:,2], axis=2)
    img = np.concatenate((B, G, R), axis = 2)                       # BGRBGRBGR==>RGBRGBRGB

    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data = tData()
    input_data.scale_ = 1.0
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    output_data = tData()
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)
    ret = rgb2gray(byref(output_data), byref(input_data), mode)
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == np.expand_dims(gray, axis=2)
    print("result diffs between PIL and c of rgb2gray(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./pillow/rgb2gray_{}_python.txt".format(mode), gray.reshape(-1, result.shape[2]), fmt="%d")
        np.savetxt("./pillow/rgb2gray_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")



########################### Resize (mode = 0) ##################################


if RESIZE_0_TEST:
    # check consistence of resize result
    om = im.resize((600, 800))                                      # 图像缩放
    om.save("./pillow/resize_pillow.bmp")
    omg = np.array(om)
    R = np.expand_dims(omg[:,:,0], axis=2)
    G = np.expand_dims(omg[:,:,1], axis=2)
    B = np.expand_dims(omg[:,:,2], axis=2)
    resize_result = np.concatenate((B, G, R), axis = 2)                       # BGRBGRBGR==>RGBRGBRGB

    mode = 0
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
    p_workspace  = bytearray(65536000)
    carr_workspace = c_byte * len(p_workspace)
    workspace.shape_.ndim_ = 1
    workspace.shape_.dims_[0] = 65536000
    workspace.dptr_ = cast(carr_workspace(*p_workspace), c_void_p)

    ret = libresize(byref(output_data), byref(input_data), mode, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == resize_result
    print("result diffs between PIL and c of resize(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./pillow/resize_{}_python.txt".format(mode), resize_result.reshape(-1, resize_result.shape[2]), fmt="%d")
        np.savetxt("./pillow/resize_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


########################### crop ##################################

if CROP_TEST:

    # check consistence of crop result
    crop_param = (100,20,900,800)
    om = im.crop(crop_param)                                   # 矩形框裁剪，box=(左，上，右，下)，原点在左上角
    om.save("./pillow/crop_pillow.bmp")
    omg = np.array(om)
    R = np.expand_dims(omg[:,:,0], axis=2)
    G = np.expand_dims(omg[:,:,1], axis=2)
    B = np.expand_dims(omg[:,:,2], axis=2)
    CenterCrop_np = np.concatenate((B, G, R), axis = 2)                       # BGRBGRBGR==>RGBRGBRGB

    box_array = (c_int32 * 4)(crop_param[0], crop_param[1], crop_param[2], crop_param[3])
    box = pointer(box_array)

    mode = 0
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

    compare = result == CenterCrop_np   # 注意超出图片范围，PIL会填充0，c代码直接截断
    print("result diffs between PIL and c of crop:{}, percentage：{:.2f}%"\
        .format(np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("crop_{}_python.txt".format(mode), CenterCrop_np.reshape(-1, CenterCrop_np.shape[2]), fmt="%d")
        np.savetxt("crop_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


########################### Rotate 90 (mode=0) ##################################

if ROTATE_90_TEST:

    # check consistence of rotate90 result
    om = im.rotate(90, expand=True)                                 # 逆时针90度旋转
    om.save("./pillow/rotate_90_pillow.bmp")
    omg = np.array(om)
    R = np.expand_dims(omg[:,:,0], axis=2)
    G = np.expand_dims(omg[:,:,1], axis=2)
    B = np.expand_dims(omg[:,:,2], axis=2)
    rotate_90 = np.concatenate((B, G, R), axis = 2)                       # BGRBGRBGR==>RGBRGBRGB

    mode = 0
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
    print("result diffs between PIL and c of ROTATE_90_CLOCKWISE(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./pillow/rotate_90_{}_python.txt".format(mode), rotate_90.reshape(-1, rotate_90.shape[2]), fmt="%d")
        np.savetxt("./pillow/rotate_90_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


########################### Rotate 180 (mode=1) ##################################

if ROTATE_180_TEST:

    # check consistence of rotate180 result
    om = im.rotate(180, expand=True)                                # 逆时针180度旋转
    om.save("./pillow/rotate_180_pillow.bmp")

    omg = np.array(om)
    R = np.expand_dims(omg[:,:,0], axis=2)
    G = np.expand_dims(omg[:,:,1], axis=2)
    B = np.expand_dims(omg[:,:,2], axis=2)
    rotate_180 = np.concatenate((B, G, R), axis = 2)                       # BGRBGRBGR==>RGBRGBRGB

    mode = 1
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

    compare = result == rotate_180
    print("result diffs between PIL and c of ROTATE_180_CLOCKWISE(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./pillow/rotate_180_{}_python.txt".format(mode), rotate_180.reshape(-1, rotate_180.shape[2]), fmt="%d")
        np.savetxt("./pillow/rotate_180_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


########################### Rotate 270 (mode=2) ##################################

if ROTATE_270_TEST:  

    # check consistence of rotate270 result
    om = im.rotate(270, expand=True)                                # 顺时针90度旋转
    om.save("./pillow/rotate_270_pillow.bmp")

    omg = np.array(om)
    R = np.expand_dims(omg[:,:,0], axis=2)
    G = np.expand_dims(omg[:,:,1], axis=2)
    B = np.expand_dims(omg[:,:,2], axis=2)
    rotate_270 = np.concatenate((B, G, R), axis = 2)                       # BGRBGRBGR==>RGBRGBRGB

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

    compare = result == rotate_270
    print("result diffs between PIL and c of ROTATE_270_CLOCKWISE(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./pillow/rotate_270_{}_python.txt".format(mode), rotate_270.reshape(-1, rotate_270.shape[2]), fmt="%d")
        np.savetxt("./pillow/rotate_270_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


# ############################## FLIP_TOP_BPTTOM (mode=3) #####################################

if FLIP_TOP_BPTTOM_TEST:

    # check consistence of flip_top_bottom result
    om = im.transpose(Image.FLIP_TOP_BOTTOM)                        # 上下翻转
    om.save("./pillow/flip_top_bottom_pillow.bmp")

    omg = np.array(om)
    R = np.expand_dims(omg[:,:,0], axis=2)
    G = np.expand_dims(omg[:,:,1], axis=2)
    B = np.expand_dims(omg[:,:,2], axis=2)
    flip_top_bottom = np.concatenate((B, G, R), axis = 2)                       # BGRBGRBGR==>RGBRGBRGB

    mode = 3
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

    compare = result == flip_top_bottom
    print("result diffs between PIL and c of flip_top_bottom(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./pillow/flip_top_bottom_{}_python.txt".format(mode), flip_top_bottom.reshape(-1, flip_top_bottom.shape[2]), fmt="%d")
        np.savetxt("./pillow/flip_top_bottom_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


########################### FLIP_LEFT_RIGHT (mode=4) ##################################

if FLIP_LEFT_RIGHT_TEST:

    # check consistence of flip_left_right result
    om = im.transpose(Image.FLIP_LEFT_RIGHT)                        # 左右翻转
    om.save("./pillow/flip_left_right_pillow.bmp")

    omg = np.array(om)
    R = np.expand_dims(omg[:,:,0], axis=2)
    G = np.expand_dims(omg[:,:,1], axis=2)
    B = np.expand_dims(omg[:,:,2], axis=2)
    flip_left_right = np.concatenate((B, G, R), axis = 2)                       # BGRBGRBGR==>RGBRGBRGB

    mode = 4
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

    compare = result == flip_left_right
    print("result diffs between PIL and c of flip_left_right(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./pillow/flip_left_right_{}_python.txt".format(mode), flip_left_right.reshape(-1, flip_left_right.shape[2]), fmt="%d")
        np.savetxt("./pillow/flip_left_right_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")



########################### Blur (mode = 0) ##################################

if MEAN_BLUR_TEST:

    # check consistence of blur result
    om = im.filter(ImageFilter.BLUR)                                # 图像模糊效果,均值滤波，kernel=(5,5)，不pad
    om.save("./pillow/mean_blur_0_pillow.bmp")


    omg = np.array(om)
    R = np.expand_dims(omg[:,:,0], axis=2)
    G = np.expand_dims(omg[:,:,1], axis=2)
    B = np.expand_dims(omg[:,:,2], axis=2)
    blur_filter = np.concatenate((B, G, R), axis = 2)                       # BGRBGRBGR==>RGBRGBRGB
 

    mode = 0
    kernel_size = 5
    kernel_data = np.ones((kernel_size**2, 1), dtype=np.int8)
    kernel = tData()
    # kernel.scale_ =  math.floor(np.log2(127 / (1/kernel_size**2)))
    kernel.scale_ =  1
    kernel_data = kernel_data * 81                                   # 每次要进行更改
    kernel.shape_.ndim_ = 2
    kernel.shape_.dims_ = (kernel_size, kernel_size)
    carr_kernel = c_byte * kernel_size**2
    kernel.dptr_ = cast(carr_kernel(*kernel_data), c_void_p)

    data = bytearray(img)
    carr_data = c_byte * len(data)
    # np.savetxt("./compare_test_data.txt",data,fmt="%d")
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
    ret = filter(byref(output_data), byref(input_data), byref(kernel), mode, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)
    # img_result = Image.fromarray(result)
    # img_result.save("./pillow/blur_filter_c.bmp")

    compare = result == blur_filter
    print("result diffs between PIL and c of blur_filter(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))


########################### Blur (mode = 1) ##################################

if GAUSSIAN_BLUR_TEST:

    
    om = im.filter(ImageFilter.GaussianBlur(radius = 5))                        # 高斯模糊

    om.save("./pillow/gaussian_blur_pillow.bmp")
    omg = np.array(om)
    R = np.expand_dims(omg[:,:,0], axis=2)
    G = np.expand_dims(omg[:,:,1], axis=2)
    B = np.expand_dims(omg[:,:,2], axis=2)
    blur_filter = np.concatenate((B, G, R), axis = 2)                       # BGRBGRBGR==>RGBRGBRGB

    mode = 1 

    kernel_size = 5
    kernel_data = np.ones((kernel_size**2, 1), dtype=np.int8)
    kernel = tData()
    # kernel.scale_ =  math.floor(np.log2(127 / (1/kernel_size**2)))
    kernel.scale_ =  1
    kernel_data = kernel_data * 81                                   # 在内部计算，外部给不给值都是无所谓的
    kernel.shape_.ndim_ = 2
    kernel.shape_.dims_ = (kernel_size, kernel_size)
    carr_kernel = c_byte * kernel_size**2
    kernel.dptr_ = cast(carr_kernel(*kernel_data), c_void_p)

    data = bytearray(img)
    carr_data = c_byte * len(data)
    # np.savetxt("./compare_test_data.txt",data,fmt="%d")
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
    ret = filter(byref(output_data), byref(input_data), byref(kernel), mode, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)
    # img_result = Image.fromarray(result)
    # img_result.save("./pillow/blur_filter_c.bmp")

    compare = result == blur_filter
    print("result diffs between PIL and c of gaussian_filter(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    # np.savetxt("./c_processed_r_pil.txt", result[:,:,2].reshape(result.shape[0], result.shape[1]), fmt="%d")
    # np.savetxt("./python_processed_r_pil.txt", blur_filter[:,:,2].reshape(blur_filter.shape[0], blur_filter.shape[1]), fmt="%d")


########################### Blur (mode = 2) ##################################

if MEDIAN_BLUR_TEST:

    # check consistence of MedianFilter result
    om = im.filter(ImageFilter.MedianFilter(size=3))                # 中值滤波
    om.save("./pillow/median_blur_pillow.bmp")

    omg = np.array(om)
    R = np.expand_dims(omg[:,:,0], axis=2)
    G = np.expand_dims(omg[:,:,1], axis=2)
    B = np.expand_dims(omg[:,:,2], axis=2)
    median_filter = np.concatenate((B, G, R), axis = 2)                       # BGRBGRBGR==>RGBRGBRGB



    mode = 2
    data = bytearray(img)
    carr_data = c_byte * len(data)
    # np.savetxt("./compare_test_data.txt",data,fmt="%d")
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

    output_data = tData()
    output_data.scale_ = 1.0
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)
    ret = filter(byref(output_data), byref(input_data), byref(kernel), mode, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)
    # img_result = Image.fromarray(result)
    # img_result.save("./pillow/blur_filter_c.bmp")

    compare = result == median_filter
    print("result diffs between PIL and c of median_filter(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./pillow/median_filter_{}_python.txt".format(mode), median_filter.reshape(-1, median_filter.shape[2]), fmt="%d")
        np.savetxt("./pillow/median_filter_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")
    

########################### Blur (mode = 3) ##################################


if MIN_BLUR_TEST:

    # # check consistence of MinFilter result
    om = im.filter(ImageFilter.MinFilter(size=3))                   # 最小值滤波
    om.save("./pillow/min_blur_pillow.bmp")

    omg = np.array(om)
    R = np.expand_dims(omg[:,:,0], axis=2)
    G = np.expand_dims(omg[:,:,1], axis=2)
    B = np.expand_dims(omg[:,:,2], axis=2)
    Min_filter = np.concatenate((B, G, R), axis = 2)                       # BGRBGRBGR==>RGBRGBRGB



    mode = 3
    data = bytearray(img)
    carr_data = c_byte * len(data)
    # np.savetxt("./compare_test_data.txt",data,fmt="%d")
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

    output_data = tData()
    output_data.scale_ = 1.0
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)
    ret = filter(byref(output_data), byref(input_data), byref(kernel), mode, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)
    # img_result = Image.fromarray(result)
    # img_result.save("./pillow/blur_filter_c.bmp")

    compare = result == Min_filter
    print("result diffs between PIL and c of Min_filter(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
   

########################### Blur (mode = 3) ##################################

if MAX_BLUR_TEST:

    # # check consistence of MaxFilter result
    om = im.filter(ImageFilter.MaxFilter(size=3))                   # 最大值滤波
    om.save("./pillow/max_filter_pillow.bmp")

    omg = np.array(om)
    R = np.expand_dims(omg[:,:,0], axis=2)
    G = np.expand_dims(omg[:,:,1], axis=2)
    B = np.expand_dims(omg[:,:,2], axis=2)
    Max_filter = np.concatenate((B, G, R), axis = 2)                       # BGRBGRBGR==>RGBRGBRGB



    mode = 4
    data = bytearray(img)
    carr_data = c_byte * len(data)
    # np.savetxt("./compare_test_data.txt",data,fmt="%d")
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

    output_data = tData()
    output_data.scale_ = 1.0
    p_buff = bytearray(img.size)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)
    ret = filter(byref(output_data), byref(input_data), byref(kernel), mode, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)
    # img_result = Image.fromarray(result)
    # img_result.save("./pillow/blur_filter_c.bmp")

    compare = result == Max_filter
    print("result diffs between PIL and c of Max_filter(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))

########################### Pad (mode=0) ##################################

if PAD_0_TEST:

    pads_param = (7,8,9,10) # 左上右下
    pads_array = (c_int8 * 4)(pads_param[1], pads_param[0], pads_param[3], pads_param[2]) # 传入函数的值，上左下右

    om = ImageOps.expand(im,pads_param,fill = 0) # 填充0 
    om.save("./pillow/pad_0_pillow.bmp")

    omg = np.array(om)


    # C代码测试

    mode = 0

    # 开头进行过一次变换，所以这里再变换一次，变换回来
    R = np.expand_dims(img[:,:,0], axis=2)
    G = np.expand_dims(img[:,:,1], axis=2)
    B = np.expand_dims(img[:,:,2], axis=2)
    img = np.concatenate((B, G, R), axis = 2)  

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

    fill_data = 0 # 填充常数0

    ret = Pad(byref(output_data), byref(input_data), p_pads.contents, mode, fill_data, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == omg
    print("result diffs between PIL and c of Pad(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("Pad_{}_python.txt".format(mode), omg.reshape(-1, omg.shape[2]), fmt="%d")
        np.savetxt("Pad_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")

######################################################################################

print('result compare completed')

