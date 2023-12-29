#ifndef __CV_UTILS_H__
#define __CV_UTILS_H__

#include <stdint.h>
#include "common.h"

#ifdef __cplusplus
extern "C" {
#endif


// 图像映射，RGB=>YUV
int32_t rgb2yuv(tData *out, const tData *in, const int32_t mode);

// 图像映射，YUV=>RGB
int32_t yuv2rgb(tData *out, const tData *in, const int32_t mode);

// 图像裁剪，支持矩形框，四个点坐标由box给定
int32_t crop(tData *out, const tData *in, const int32_t *box);

// 图像缩放，先支持bilinear方式
int32_t resize(tData *out, const tData *in, const int32_t mode, tData *workspace);

// 图像旋转，支持90、180、270度旋转，也可支持围绕水平或垂直轴翻转
int32_t rotate(tData *out, const tData *in, const int32_t mode);

// 图像映射，RGB=>GRAY
int32_t rgb2gray(tData *out, const tData *in, const int32_t mode);

// 图像映射，GRAY=>RGB
int32_t gray2rgb(tData *out, const tData **in, const int32_t mode);

// 图像通道分离，支持取RGB图像中的任一维度，或者取RGB均值输出
int32_t channel_split(tData *out, const tData *in, const int32_t mode);

// 图像通道融合,支持灰度图像转换为彩色图像
int32_t channel_merge(tData *out, const tData **in, const int32_t mode);

// 图像数据重排，RGBRGBRGB => RRRGGGBBB
int32_t data_rearrangement(tData *out, const tData *in, const int32_t mode);

// 边缘填充，借鉴onnx定义，pads数组对应每个维度的填充数，支持填充0，镜像填充，尾部填充三种方式
int32_t Pad(tData *out, const tData *in, const int8_t *pads, const int32_t mode, const uint8_t fill_data, tData *workspace);

#ifdef __cplusplus
}
#endif
#endif /* _LS_CUTLINE_API_H_ */