# CV通用函数接口说明

## 数据结构定义
### 数据类型定义

```c
typedef enum __tDType__ {
  DTypeUndefined = 0,
  Float16 = 0x6602,  //'f', 2
  Float32 = 0x6604,  //'f', 4
  Float64 = 0x6608,  //'f', 8
  Int8 = 0x6901,     //'i', 1
  Int16 = 0x6902,    //'i', 2
  Int32 = 0x6904,    //'i', 4
  Int64 = 0x6908,    //'i', 8
  Uint8 = 0x7501,    //'u', 1
  Uint16 = 0x7502,   //'u', 2
  Uint32 = 0x7504,   //'u', 4
  Uint64 = 0x7508,   //'u', 8
  Bool = 0x6201,
  Int4 = 0x6801,
} tDType;
```


### 图像类型定义

```c
typedef struct _Shape_ {
  uint32_t ndim_;
  uint32_t dims_[3];
} tShape;

typedef struct _Data_ {
  void *dptr_;
  uint16_t dev_type_;
  uint16_t dtype_;
  uint16_t zero_;
  float scale_;
  tShape shape_;
} tData;
```

## API接口定义

### 数据类型转换

#### 无符号和有符号8bit数据互转

1.	无符号数转有符号数

    a) 函数声明

`void u8_to_int8(int8_t *out, const int8_t *in, const uint32_t size);`
    
&emsp;&emsp;&emsp;b) 参数说明

```c
int8_t *out		：传入的输出内存块地址，仅支持8bit有符号数；
const int8_t *in	：传入的输入内存块地址，仅支持8bit无符号数；
const uint32_t size	：传入的待处理数据大小；
```
2.	有符号数转无符号数

    a)	函数声明

`void int8_to_u8(int8_t *out, const int8_t *in, const uint32_t size);`

&emsp;&emsp;&emsp;b) 参数说明
```c
int8_t *out		：传入的输出内存块地址，仅支持8bit无符号数；
const int8_t *in	：传入的输入内存块地址，仅支持8bit有符号数；
const uint32_t size	：传入的待处理数据大小；
```

#### 定点数与浮点数之间互转

1.	定点数转浮点数

    a)	函数声明

`int32_t intx_to_fp32(float *out, const void *in, const uint32_t size, const uint32_t scale, const tDType data_type)`

&emsp;&emsp;&emsp;b) 参数说明
```c
float* out			：返回转换后的数据，注意预留足够的内存空间
const void *in		：传入原始数据块
const uint32_t size	：传入原始数据个数
const uint32_t scale：传入原始数据对应的量化Q值
const uint32_t	dtype：传入原始数据对应的数据类型，目前支持int8/int16/int32转fp32
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```
2.	浮点数转定点数

    a)	函数声明

`int32_t fp32_to_intx(void *out, const float *in, const uint32_t size, const uint32_t scale, const tDType data_type)`

&emsp;&emsp;&emsp;b) 参数说明
```c
void *out			：返回转换后的数据，注意预留足够的内存空间
const float *in		：传入原始数据块
const uint32_t size	：传入原始数据个数
const uint32_t scale：传入原始数据对应的量化Q值
const uint32_t	dtype：传入原始数据对应的数据类型，目前支持fp32转int8/int16/int32
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```

#### 二维数据转置
1.	二维转置

    a)	函数声明

`int32_t transpose2d(void *out, const void *in, const uint32_t height, const uint32_t width, const tDType data_type)`

&emsp;&emsp;&emsp;b) 参数说明
```c
void *out 		：返回转换后的数据
const void *in		：传入原始数据块
const uint32_t height：传入原始数据的第一维大小
const uint32_t width：传入原始数据的第二位大小
const tDType data_type：传入的数据类型，输入和输出的数据类型一致，目前支持fp32/uint8/int8/int16/int32
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```

###	图像格式转换
#### RGB格式与YUV格式互转
1.	RGB转YUV

    a)	函数声明

`int32_t rgb2yuv(tData *out, const tData *in, const int32_t mode)`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out		：返回转换后的数据信息
const tData *in	：传入原始数据信息，包括数据维度，scale值，数据类型（目前只支持uint8）
const int32_t mode	：设置转换模式，目前支持BGR转YUV BT.470标准和BGR转YCbCr BT.601标准两种模式
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```
2.	YUV转RGB

&emsp;&emsp;&emsp;a) 函数声明

`int32_t yuv2rgb(tData *out, const tData *in, const int32_t mode)`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out		：返回转换后的数据信息
const tData *in	：传入原始数据信息，包括数据维度，scale值，数据类型（目前只支持uint8）
const int32_t mode	：设置转换模式，目前支持YUV4:4:4 BT.470标准转BGR和YCbCr BT.601标准转 BGR888 的两种模式以及mode = 2时，将输入的VYUY（YUV4:2:2）转换为RGB565。
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```


#### 彩色图像与灰度图像互转
1.	彩色图像转灰度图像

    a)	函数声明

`int32_t rgb2gray(tData *out, const tData *in, const int32_t mode)`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out		：返回转换后的数据信息
const tData *in	：传入原始数据信息，包括数据维度，scale值，数据类型（目前只支持uint8）
const int32_t mode	：设置转换模式，目前支持加权系数转换、取平均值、取最大值、取最小值四种模式
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```
2.	灰度图像转彩色图像

    a)	函数声明

`int32_t gray2rgb(tData *out, const tData **in, const int32_t mode)`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out		：返回转换后的数据信息（uint8数据类型）
const tData *in	：传入原始数据信息，包括数据维度，scale值，数据类型（目前只支持uint8）
const int32_t mode	：设置转换模式，目前仅支持单通道复制三份
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```
#### 图像数据重排

&emsp;&emsp;&emsp;a) 函数声明

`int32_t data_rearrangement(tData *out, const tData *in, const int32_t mode)`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out		：返回转换后的数据信息（uint8数据类型）
const tData *in	：传入原始数据信息，包括数据维度，scale值，数据类型（目前只支持uint8）
const int32_t mode	：设置转换模式，目前支持HWC转换为CHW
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```
###	图像变换类
#### 图像缩放

&emsp;&emsp;&emsp;a) 函数声明

`int32_t resize(tData *out, const tData *in, const int32_t mode, tData *workspace)`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out		：返回转换后的数据信息（uint8数据类型）
const tData *in	：传入原始数据信息，包括数据维度，scale值，数据类型（目前只支持uint8）
const int32_t mode：设置缩放模式，目前只支持双线性插值模式
tData *workspace	：传入临时内存空间，用于中间数据缓存
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```

#### 图像裁剪（矩形框）

&emsp;&emsp;&emsp;a) 函数声明

`int32_t crop(tData *out, const tData *in, const int32_t box[4])`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out		：返回转换后的数据信息（uint8数据类型）
const tData *in	：传入原始数据信息，包括数据维度，scale值，数据类型（目前只支持uint8）
const int32_t box[4]：设置矩形框坐标，box=(左，上，右，下)，原点在左上角
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```
#### 图像旋转

&emsp;&emsp;&emsp;a) 函数声明

`int32_t rotate(tData *out, const tData *in, const int32_t mode)`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out		：返回转换后的数据信息（uint8数据类型）
const tData *in	：传入原始数据信息，包括数据维度，scale值，数据类型（目前只支持uint8）
const int32_t mode：设置旋转模式，目前支持顺时针90、180、270度、水平翻转和垂直翻转五种模式
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```
#### 边缘填充

&emsp;&emsp;&emsp;a) 函数声明

`int32_t Pad(tData *out, const tData *in, const int32_t *pads, const int32_t mode, const uint8_t fill_data, tData *workspace)`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out		：返回填充后的数据信息（uint8数据类型）
const tData *in	：传入原始数据信息，包括数据维度，scale值，数据类型（目前只支持uint8）
const int32_t *pads	：传入各维度填充的个数，按顺序分别(上，左，下，右)
const int32_t mode：设置填充模式，目前支持固定值、尾部填充、镜像填充三种方式
const uint8 fill_data：固定值填充模式下生效，对应填充的固定值
tData *workspace	：传入临时内存空间，用于中间数据缓存
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```
#### 图像归一化

&emsp;&emsp;&emsp;a) 函数声明

`int32_t normalize(tData *out, const tData *in, const tData *mean, const tData *var)`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out		：返回归一化后的数据信息（int8数据类型）
const tData *in	：传入原始数据信息，包括数据维度，scale值，数据类型（目前只支持int8）
const tData *mean	：传入统计出的数据均值信息(mean->dptr_)，均值数据的大小支持int16，同时需要传入对应的scale。
const tData *var	：传入统计出的数据方差信息(var->dptr_)，方差数据的大小支持int16，同时需要传入对应的scale。
注意输入输出数据的排布均为HWC，支持RGB和GRAY两种类型
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```
###	图像处理类
#### 均值滤波

&emsp;&emsp;&emsp;a) 函数声明

`int32_t filter(tData *out, const tData *in, const tData *kernel, const int32_t mode, tData *workspace)`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out		：返回处理后的数据信息（uint8数据类型）
const tData *in	：传入原始数据信息，包括数据维度，scale值，数据类型（目前只支持uint8）
const tData *kernel：传入滤波器的kernel，只需要定义传入的kernel_size即可。要求kernel_size小于等于5，kernel的数值和scale自行定义是无效的，会在函数内部重新计算并被覆盖。
const int32_t mode	：设置滤波方式，均值滤波mode = 0（目前支持均值滤波、高斯滤波、中值滤波、最大值滤波、最小值滤波）
tData *workspace	：传入临时内存空间，用于中间数据缓存，注意内存空间的大小需要传入workspace->shape_.dims[0]
注意输入输出数据的排布均为HWC，支持RGB和GRAY格式
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```
#### 高斯滤波

&emsp;&emsp;&emsp;a) 函数声明

`int32_t filter(tData *out, const tData *in, const tData *kernel, const int32_t mode, tData *workspace)`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out		：返回处理后的数据信息（uint8数据类型）
const tData *in	：传入原始数据信息，包括数据维度，scale值，数据类型（目前只支持uint8）
const tData *kernel：传入滤波器的kernel，只需要定义传入的kernel_size即可。要求kernel_size小于等于5，kernel的数值和scale自行定义是无效的，会在函数内部重新计算并被覆盖。
const int32_t mode	：设置滤波方式，高斯滤波mode = 1（目前支持均值滤波、高斯滤波、中值滤波、最大值滤波、最小值滤波）
tData *workspace	：传入临时内存空间，用于中间数据缓存，注意内存空间的大小需要传入workspace->shape_.dims[0]
注意输入输出数据的排布均为HWC，支持RGB和GRAY格式
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```
#### 均值滤波

&emsp;&emsp;&emsp;a) 函数声明

`int32_t filter(tData *out, const tData *in, const tData *kernel, const int32_t mode, tData *workspace)`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out		：返回处理后的数据信息（uint8数据类型）
const tData *in	：传入原始数据信息，包括数据维度，scale值，数据类型（目前只支持uint8）
const tData *kernel：传入滤波器的kernel，只需要定义传入的kernel_size即可。要求kernel_size小于等于5，kernel的数值和scale自行定义是无效的。
const int32_t mode	：设置滤波方式，均值滤波mode = 2（目前支持均值滤波、高斯滤波、中值滤波、最大值滤波、最小值滤波）
tData *workspace	：传入临时内存空间，用于中间数据缓存，注意内存空间的大小需要传入workspace->shape_.dims[0]
注意输入输出数据的排布均为HWC，支持RGB和GRAY格式
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```

iv.	最小值滤波

&emsp;&emsp;&emsp;a) 函数声明

`int32_t filter(tData *out, const tData *in, const tData *kernel, const int32_t mode, tData *workspace)`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out		：返回处理后的数据信息（uint8数据类型）
const tData *in	：传入原始数据信息，包括数据维度，scale值，数据类型（目前只支持uint8）
const tData *kernel：传入滤波器的kernel，只需要定义传入的kernel_size即可。要求kernel_size小于等于5，kernel的数值和scale自行定义是无效的。
const int32_t mode	：设置滤波方式，最小值滤波mode = 3（目前支持均值滤波、高斯滤波、中值滤波、最大值滤波、最小值滤波）
tData *workspace	：传入临时内存空间，用于中间数据缓存，注意内存空间的大小需要传入workspace->shape_.dims[0]
注意输入输出数据的排布均为HWC，支持RGB和GRAY格式
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```
v.	最大值滤波

&emsp;&emsp;&emsp;a) 函数声明

`int32_t filter(tData *out, const tData *in, const tData *kernel, const int32_t mode, tData *workspace)`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out		：返回处理后的数据信息（uint8数据类型）
const tData *in	：传入原始数据信息，包括数据维度，scale值，数据类型（目前只支持uint8）
const tData *kernel：传入滤波器的kernel，只需要定义传入的kernel_size即可。要求kernel_size小于等于5，kernel的数值和scale自行定义是无效的。
const int32_t mode	：设置滤波方式，均值滤波mode = 4（目前支持均值滤波、高斯滤波、中值滤波、最大值滤波、最小值滤波）
tData *workspace	：传入临时内存空间，用于中间数据缓存，注意内存空间的大小需要传入workspace->shape_.dims[0]
注意输入输出数据的排布均为HWC，支持RGB和GRAY格式
函数返回执行结果状态，返回0代表API执行成功，其余为错误码
```

###	常用操作
#### 对图像缩放，转为int8后标准化输出int8数据

&emsp;&emsp;&emsp;a) 函数声明

`int32_t Common_processing_operations(tData *out, const tData *in, const int32_t mode, tData *workspace, const tData *mean, const tData *var)`

&emsp;&emsp;&emsp;b) 参数说明
```c
tData *out : 操作处理结果存放结构体，输出数据为int8，对图像的缩放要求存在其中;
tData *in : 源数据的存放结构体，输入数据为uint8;
int32_t mode : resize函数中的模式，暂时没有任何用处，填什么都可以;
tData *workspace :数据暂存区，暂存区的大小填写在workspace->shape_.dims_[0]中;
tData *mean : 三个通道的平均值数据，数据存在dptr_地址，共三个int16数据(为了更加精确)，数据的scale存放在mean->scale_;
tData *var : 同上，存放三个通道的标准差数据，数据存在dptr_地址，共三个int16数据，数据的scale存放在var->scale_中;
3.	返回值
int32_t : 返回0代表执行成功，其余为失败。
```


## 封装库说明
1. 本次发布提供libcv.so和libcv.a两个库，分别对应linux仿真平台和csk6平台库。
2. 目前cv篇函数和通用函数大多数是c语言通用版本实现，部分函数调用了luna加速库。下一步全部替换为luna加速库，支持luna加速计算。**<font color = red>注意所有函数的内存分配均采用静态管理，所有内存包括临时空间都由外部预先分配好；</font>**
3. 可使用result_compare文件夹中的测试代码对c语言封装库与python库(opencv/torchvision/PIL)运算结果进行比对（误差率，测试图片为result_compare/test.jpg）



