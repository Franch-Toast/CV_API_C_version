from ctypes import *
from enum import IntEnum


# 测试功能模块开关


PAD_0_TEST              = True # 边缘填充，模式0
PAD_1_TEST              = True # 边缘填充，模式1
PAD_2_TEST              = True # 边缘填充，模式2

RESIZE_0_TEST           = True # 图像缩放
CROP_TEST               = True # 图像裁剪
RGB2GRAY_0_TEST         = True # RGB图像转灰度图像
NORMALIZE_TEST          = True # 图像标准化

ROTATE_90_TEST          = True # 图像逆时针旋转90°
ROTATE_180_TEST         = True # 图像逆时针旋转180°
ROTATE_270_TEST         = True # 图像逆时针旋转270°
FLIP_LEFT_RIGHT_TEST    = True # 图像左右翻转
FLIP_TOP_BPTTOM_TEST    = True # 图像上下翻转


DATA_DUMP               = False # 打印结果（不一致时）

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
crop.argtypes = (POINTER(tData), POINTER(tData), POINTER(c_int32))

libresize = lib.resize
libresize.restype = c_int32
libresize.argtypes = (POINTER(tData), POINTER(tData), c_int32, POINTER(tData))

rotate = lib.rotate
rotate.restype = c_int32
rotate.argtypes = (POINTER(tData), POINTER(tData), c_int32)

filter = lib.filter
filter.restype = c_int32
filter.argtypes = (POINTER(tData), POINTER(tData), POINTER(tData), c_int32, POINTER(c_int8))

data_rearrangement = lib.data_rearrangement
data_rearrangement.restype = c_int32
data_rearrangement.argtypes = (POINTER(tData), POINTER(tData), c_int32)

Pad = lib.Pad
Pad.restype = c_int32
Pad.argtypes = (POINTER(tData), POINTER(tData), POINTER(c_int8), c_int32, c_uint8, POINTER(tData))

normalize = lib.normalize
normalize.restype = c_int32
normalize.argtypes = (POINTER(tData), POINTER(tData), POINTER(tData), POINTER(tData))




############################# 运算结果对比 #####################################
import torch
import torchvision                                              # 主要处理图像数据，包含一些常用的数据集、模型、转换函数等
import numpy as np
from torchvision.io import image
import torchvision.transforms as transforms                     # 提供常用的数据预处理操作
from torchvision.utils import save_image

from PIL import Image
image = Image.open("test.jpg")

print('result compare begin')
########################### Resize (mode = 0) ##################################

if RESIZE_0_TEST:

    # check consistence of resize result
    transform = transforms.Compose([
        transforms.Resize((800, 600)),
        transforms.ToTensor(),
    ])
    resize_result = transform(image)
    save_image(resize_result, "./torchvision/result_resize.bmp")                  # 图像缩放
    resize_result = resize_result * 255
    resize_result_np = resize_result.numpy().astype(np.uint8)

    mode = 0
    img = np.array(image)
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

    ret = libresize(byref(output_data), byref(input_data), mode, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == resize_result_np.transpose(1, 2, 0)
    print("result diffs between torchvision and c of resize(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./torchvision/resize_{}_python.txt".format(mode), resize_result.reshape(-1, resize_result.shape[2]), fmt="%d")
        np.savetxt("./torchvision/resize_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")
    # np.savetxt("./torchvision/./resize_python_torch.txt", resize_result_np.transpose(1, 2, 0)[:,:,2].reshape(resize_result_np.transpose(1, 2, 0).shape[0], resize_result_np.transpose(1, 2, 0).shape[1]), fmt="%d")


################################ crop ##########################################

if CROP_TEST:
# check consistence of crop result
    
    img = np.array(image)
    data = bytearray(img)
    carr_data = c_byte * len(data)
    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    crop_size = 1000 #超过图片大小，torchvision会在边缘填充0，c语言版本会直接截断
    crop_size_half = crop_size // 2
    transform = transforms.Compose([
        transforms.CenterCrop(crop_size),
        transforms.ToTensor(),
    ])
    CenterCrop = transform(image)
    save_image(CenterCrop, "./torchvision/result_CenterCrop.bmp")          # 中心点裁剪
    CenterCrop = CenterCrop * 255
    CenterCrop_np = CenterCrop.numpy()
    CenterCrop_np = CenterCrop_np.transpose(1, 2, 0).astype(np.uint8)

    h_hiddle = img.shape[0] // 2
    w_hiddle = img.shape[1] // 2
    box_array = (c_int32 * 4)(w_hiddle - crop_size_half, h_hiddle - crop_size_half, w_hiddle + crop_size_half, h_hiddle + crop_size_half)
    box = pointer(box_array)

    output_data = tData()
    p_buff = bytearray(crop_size * crop_size *3)
    carr_share = c_byte * len(p_buff)
    output_data.dptr_ = cast(carr_share(*p_buff), c_void_p)

    ret = crop(byref(output_data), byref(input_data), box.contents)
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == CenterCrop_np
    print("result diffs between torchvision and c of crop:{}, percentage：{:.2f}%"\
        .format(np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./torchvision/crop_python.txt", CenterCrop_np.reshape(-1, CenterCrop_np.shape[2]), fmt="%d")
        np.savetxt("./torchvision/crop_clib.txt", result.reshape(-1, result.shape[2]), fmt="%d")

############################### Pad (mode=0) ###################################

if PAD_0_TEST:

    # check consistence of pad result, constant
    pads_param = (7, 8, 9, 10)
    pads_array = (c_int8 * 4)(pads_param[1], pads_param[0], pads_param[3], pads_param[2])
    fill_data = 180

    transform = transforms.Compose([
        transforms.Pad(pads_param, fill=fill_data, padding_mode='constant'),#可以传入1，2，4个参数，1：四周填充，2：左右、上下填充，4：左上右下填充
        transforms.ToTensor(),
    ])
    pad_result = transform(image)
    save_image(pad_result, "./torchvision/result_pad_0.bmp")                        # 边缘填充
    pad_result = pad_result * 255
    pad_result_np = pad_result.numpy()
    pad_result_np = pad_result_np.transpose(1, 2, 0).astype(np.uint8)

    mode = 0
    img = np.array(image)
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

    ret = Pad(byref(output_data), byref(input_data), p_pads.contents, mode, fill_data, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == pad_result_np
    print("result diffs between torchvision and c of Pad(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./torchvision/Pad_{}_python.txt".format(mode), pad_result_np.reshape(-1, pad_result_np.shape[2]), fmt="%d")
        np.savetxt("./torchvision/Pad_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")

############################## Pad (mode=1) ####################################

if PAD_1_TEST:

    # check consistence of pad result, edge

    pads_param = (7, 8, 9, 10)
    pads_array = (c_int8 * 4)(pads_param[1], pads_param[0], pads_param[3], pads_param[2])
    fill_data = 180

    transform = transforms.Compose([
        transforms.Pad(pads_param, padding_mode='edge'),
        transforms.ToTensor(),
    ])
    pad_result = transform(image)
    save_image(pad_result, "./torchvision/result_pad_1.bmp")                        # 边缘填充
    pad_result = pad_result * 255
    pad_result_np = pad_result.numpy()
    pad_result_np = pad_result_np.transpose(1, 2, 0).astype(np.uint8)

    mode = 1
    img = np.array(image)
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

    ret = Pad(byref(output_data), byref(input_data), p_pads.contents, mode, fill_data, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == pad_result_np
    print("result diffs between torchvision and c of Pad(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./torchvision/Pad_{}_python.txt".format(mode), pad_result_np.reshape(-1, pad_result_np.shape[2]), fmt="%d")
        np.savetxt("./torchvision/Pad_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")

############################## Pad (mode=2) ####################################

if PAD_2_TEST:

    # check consistence of pad result, reflect

    pads_param = (7, 8, 9, 10)
    pads_array = (c_int8 * 4)(pads_param[1], pads_param[0], pads_param[3], pads_param[2])
    fill_data = 180

    transform = transforms.Compose([
        transforms.Pad(pads_param, padding_mode='reflect'),
        transforms.ToTensor(),
    ])
    pad_result = transform(image)
    save_image(pad_result, "./torchvision/result_pad_2.bmp")                        # 边缘填充
    pad_result = pad_result * 255
    pad_result_np = pad_result.numpy()
    pad_result_np = pad_result_np.transpose(1, 2, 0).astype(np.uint8)

    mode = 2
    img = np.array(image)
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

    ret = Pad(byref(output_data), byref(input_data), p_pads.contents, mode, fill_data, byref(workspace))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_uint8)), shape=output_data.shape_.dims_)

    compare = result == pad_result_np
    print("result diffs between torchvision and c of Pad(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./torchvision/Pad_{}_python.txt".format(mode), pad_result_np.reshape(-1, pad_result_np.shape[2]), fmt="%d")
        np.savetxt("./torchvision/Pad_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")

############################## Normalize #######################################

if NORMALIZE_TEST:


    # check consistence of normalize result
    mean = (0.4914, 0.4822, 0.4465) #(-2.693, -5.039, -14.1425)
    var = (0.229, 0.224, 0.225)# (58.395, 57.12, 57.375)
    # var = (1, 1, 1)
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean, var),
    ])
    Normalize = transform(image)
    
    # Normalize = transform(image).permute(1, 2, 0).numpy()
    # np.savetxt("./torchvision/origin_tensor_var1.txt", Normalize.reshape(-1, Normalize.shape[2]), fmt="%3f")

    # transform = transforms.Compose([
    #     transforms.ToTensor(),
    # ])
    # data1 = transform(image)

    save_image(Normalize, "./torchvision/result_normalize.bmp")            # 归一化
    Normalize = (Normalize * 128 + 0.5)
    
    Normalize_np = np.floor(Normalize.numpy())
    Normalize_np = Normalize_np.transpose(1, 2, 0).astype(np.int8)

    img = np.array(image)
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


    transform = transforms.Compose([
        transforms.ToTensor(),
    ])
    # temp = transform(image).permute(1, 2, 0).numpy()
    # np.savetxt("./torchvision/origin_tensor.txt", temp.reshape(-1, temp.shape[2]), fmt="%3f")
    # temp_test = (temp * 255).numpy()

    # data2 = (transform(image) * 255).permute(1, 2, 0).numpy().astype(np.uint8)

    # compare = data2==img
    # compare = np.sum(compare == False)
    
    data1 = (transform(image) * 255 - 128).permute(1, 2, 0).numpy().astype(np.int8)

    data = bytearray(data1)
    carr_data = c_byte * len(data)
    input_data = tData()
    input_data.shape_.ndim_ = 3
    input_data.shape_.dims_ = (img.shape[0], img.shape[1], img.shape[2])
    input_data.dptr_ = cast(carr_data(*data), c_void_p)

    mean_data = tData()
    mean_array = (c_int16 * 3)(round((mean[0] * 255 - 128) * 256), round((mean[1] * 255 - 128) * 256), round((mean[2] * 255 - 128) * 256))
    mean_data.scale_ = 8
    p_mean = pointer(mean_array)
    mean_data.dptr_ = cast(p_mean , c_void_p)

    # p_mean = pointer(mean_array)

    var_data = tData()
    var_array = (c_int16 * 3)(round(var[0] * 255 * 512), round(var[1] * 255 * 512), round(var[2] * 255 * 512))
    p_var = pointer(var_array)
    var_data.scale_ = 9
    var_data.dptr_ = cast(p_var , c_void_p)
    # p_var = pointer(var_array)

    ret = normalize(byref(output_data), byref(input_data), byref(mean_data), byref(var_data))
    result = np.ctypeslib.as_array(cast(output_data.dptr_, POINTER(c_int8)), shape=output_data.shape_.dims_)

    compare = result == Normalize_np
    print("result diffs between torchvision and c of Normalize:{}, percentage：{:.2f}%"\
        .format(np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./torchvision/Normalize_python.txt", Normalize_np.reshape(-1, Normalize_np.shape[2]), fmt="%d")
        np.savetxt("./torchvision/Normalize_clib.txt", result.reshape(-1, result.shape[2]), fmt="%d")

########################### RGB2Gray (mode=0) ##################################

if RGB2GRAY_0_TEST:
    
    
    transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.ToTensor(),
    ])
    grayscale = transform(image)
    save_image(grayscale, "./torchvision/result_rgb2gray.bmp")  
    # omg = np.array(grayscale)

    grayscale_result = grayscale * 255
    grayscale_result_np = grayscale_result.numpy()
    omg = grayscale_result_np.transpose(1, 2, 0).astype(np.uint8)

    img = np.array(image)
    R = np.expand_dims(img[:,:,0], axis=2)
    G = np.expand_dims(img[:,:,1], axis=2)
    B = np.expand_dims(img[:,:,2], axis=2)
    img = np.concatenate((B, G, R), axis = 2)

    mode = 0
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

    
    compare = result == omg
    print("result diffs between torchvision and c of rgb2gray(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./torchvision/rgb2gray_{}_python.txt".format(mode), omg.reshape(-1, omg.shape[2]), fmt="%d")
        np.savetxt("./torchvision/rgb2gray_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")

########################### Rotate 90 (mode=0) ##################################

if ROTATE_90_TEST:

    # 逆时针90度

    transform = transforms.Compose([
    transforms.RandomRotation(degrees=(90, 90), expand=True, center=(1080/2, 1904/2)),   # expand=False旋转的棱角消失，保持原图像的大小，否则变大
    transforms.ToTensor(),
    ])
    
    rotate_90 = transform(image)
    save_image(rotate_90, "./torchvision/result_rotate_90.bmp")                        # 边缘填充
    rotate_90_result = rotate_90 * 255
    rotate_90_result_np = rotate_90_result.numpy()
    rotate_90_result_np = rotate_90_result_np.transpose(1, 2, 0).astype(np.uint8)

    img = np.array(image)

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

    compare = result == rotate_90_result_np
    print("result diffs between torchvision and c of ROTATE_90_CLOCKWISE(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./torchvision/rotate_90_{}_python.txt".format(mode), rotate_90.reshape(-1, rotate_90.shape[2]), fmt="%d")
        np.savetxt("./torchvision/rotate_90_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")

########################### Rotate 180 (mode=1) ##################################

if ROTATE_180_TEST:

    # 180度
    transform = transforms.Compose([
    transforms.RandomRotation(degrees=(180, 180), expand=True, center=(1080/2, 1904/2)),   # expand=False旋转的棱角消失，保持原图像的大小，否则变大
    transforms.ToTensor(),
    ])
    
    rotate_180 = transform(image)
    save_image(rotate_180, "./torchvision/result_rotate_180.bmp")                        # 边缘填充
    rotate_180_result = rotate_180 * 255
    rotate_180_result_np = rotate_180_result.numpy()
    rotate_180_result_np = rotate_180_result_np.transpose(1, 2, 0).astype(np.uint8)
    
    img = np.array(image)
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

    compare = result == rotate_180_result_np
    print("result diffs between torchvision and c of ROTATE_180_CLOCKWISE(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./torchvision/rotate_180_{}_python.txt".format(mode), rotate_180.reshape(-1, rotate_180.shape[2]), fmt="%d")
        np.savetxt("./torchvision/rotate_180_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")
    
########################### Rotate 270 (mode=2) ##################################

if ROTATE_270_TEST:    
    
    # 270

    transform = transforms.Compose([
    transforms.RandomRotation(degrees=(270, 270), expand=True, center=(1080/2, 1904/2)),   # expand=False旋转的棱角消失，保持原图像的大小，否则变大
    transforms.ToTensor(),
    ])
    
    rotate_270 = transform(image)
    save_image(rotate_270, "./torchvision/result_rotate_270.bmp")                        # 边缘填充
    rotate_270_result = rotate_270 * 255
    rotate_270_result_np = rotate_270_result.numpy()
    rotate_270_result_np = rotate_270_result_np.transpose(1, 2, 0).astype(np.uint8)

    img = np.array(image)
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

    compare = result == rotate_270_result_np
    print("result diffs between torchvision and c of ROTATE_270_CLOCKWISE(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./torchvision/rotate_270_{}_python.txt".format(mode), rotate_270.reshape(-1, rotate_270.shape[2]), fmt="%d")
        np.savetxt("./torchvision/rotate_270_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


######################## FLIP_TOP_BPTTOM (mode=3) ################################

if FLIP_TOP_BPTTOM_TEST:

    transform = transforms.Compose([
    transforms.RandomVerticalFlip(p=1),
    transforms.ToTensor(),
    ])
    
    Flip_TB = transform(image)
    save_image(Flip_TB, "./torchvision/result_flip_top_bottom.bmp")                        
    Flip_TB_result = Flip_TB * 255
    Flip_TB_result_np = Flip_TB_result.numpy()
    Flip_TB_result_np = Flip_TB_result_np.transpose(1, 2, 0).astype(np.uint8)


    img = np.array(image)

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

    compare = result == Flip_TB_result_np
    print("result diffs between torchvision and c of flip_top_bottom(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./torchvision/flip_top_bottom_{}_python.txt".format(mode),Flip_TB_result_np.reshape(-1, Flip_TB_result_np.shape[2]), fmt="%d")
        np.savetxt("./torchvision/flip_top_bottom_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")


########################## FLIP_LEFT_RIGHT (mode=4) #################################

if FLIP_LEFT_RIGHT_TEST:

    transform = transforms.Compose([
    transforms.RandomHorizontalFlip(p=1),
    transforms.ToTensor(),
    ])
    
    Flip_LR = transform(image)
    save_image(Flip_LR, "./torchvision/result_flip_left_right.bmp")

    Flip_LR_result = Flip_LR * 255
    Flip_LR_result_np = Flip_LR_result.numpy()
    Flip_LR_result_np = Flip_LR_result_np.transpose(1, 2, 0).astype(np.uint8)

    img = np.array(image)
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

    compare = result == Flip_LR_result_np
    print("result diffs between torchvision and c of flip_left_right(mode:{}):{}, percentage：{:.2f}%"\
        .format(mode, np.sum(compare == False), np.sum(compare == False)*100/result.size))
    if np.sum(compare==False) and DATA_DUMP:
        np.savetxt("./torchvision/flip_left_right_{}_python.txt".format(mode), Flip_LR_result_np.reshape(-1, Flip_LR_result_np.shape[2]), fmt="%d")
        np.savetxt("./torchvision/flip_left_right_{}_clib.txt".format(mode), result.reshape(-1, result.shape[2]), fmt="%d")

print('result compare completed')
