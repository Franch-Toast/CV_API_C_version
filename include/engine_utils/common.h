#ifndef __COMPONENT_COMMON_H__
#define __COMPONENT_COMMON_H__

#include <stdint.h>
#include <string.h>
#include <math.h>
#include "luna/luna_misc_math.h"
#include "luna/luna_basic_math.h"
#include "luna/luna_cnn_math.h"

#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) (a) < (b) ? (a) : (b)
#define SUM(a, b) ((a) + (b))

#define SATURATE_8BITS(x) ((x) > 127 ? 127 : ((x) < -128 ? -128 : (x)))
#define SATURATE_16BITS(x) ((x) > 32768 ? 32768 : ((x) < -32768 ? -32768 : (x)))
#define SATURATE_U8BITS(x) ((x) > 255 ? 255 : ((x) < 0 ? 0 : (x)))
#define SATURATE_32BITS(x) \
  ((x) > 2147483647 ? 2147483647 : ((x) < -2147483648 ? -2147483648 : (x)))

#define SHRT_MIN    (-32768)        // minimum (signed) short value
#define SHRT_MAX      32767         // maximum (signed) short value

// 对浮点数X进行四舍五入后限制在要求的数据范围内
#define SATURATE_CAST_SHORT(X) (short)MIN(MAX((int)(X + (X >= 0.f ? 0.5f : -0.5f)), SHRT_MIN), SHRT_MAX);
#define SATURATE_CAST_INT(X)   (int)MIN(MAX((int)((X) + ((X) >= 0.f ? 0.5f : -0.5f)), INT_MIN), INT_MAX)

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

#ifdef __cplusplus
extern "C" {
#endif

void u8_to_int8(int8_t *out, const uint8_t *in, const uint32_t size);

void int8_to_u8(uint8_t *out, const int8_t *in, const uint32_t size);

// 获取int8数据的绝对值
void abs_int8(int8_t *out, const int8_t *in, const uint32_t size);

// 定点转浮点，支持int8、int16、int32转fp32
int32_t intx_to_fp32(float *out, const void *in, const uint32_t size, const uint32_t scale, const tDType data_type);

// 浮点转定点，支持fp32转int8、int16、int32
int32_t fp32_to_intx(void *out, const float *in, const uint32_t size, const uint32_t scale, const tDType data_type);

// 2维数据转换，支持fp32、int8、int16、int32
int32_t transpose2d(void *out, const void *in, const uint32_t height, const uint32_t width, const tDType data_type);

// 滤波器，支持均值滤波、方框滤波、高斯滤波、中值滤波，其它方式可通过mode进行扩展
int32_t filter(tData *out, const tData *in,const tData *kernel, const int32_t mode, tData *workspace);

// 数据归一化
int32_t normalize(tData *out, const tData *in, const tData *mean, const tData *var);

// 图像缩放后数据标准化输出int8数据
int32_t image_preprocess(tData *out, const tData *in, const int32_t mode, tData *workspace,const tData *mean, const tData *var);


// 函数声明
// void dump_uint8(const char *name, uint8_t *data, int channel, int height, int width, int width_begin, int width_end, int fixq, char format);
// void dump_int8(const char *name, int8_t *data, int32_t channel, int32_t height, int32_t width, int32_t width_begin, int32_t width_end, int32_t fixq, char format);
// 判断x的低shift位是否全为0，如果全为0，则返回 x 直接右移shift位，否则返回 x 右移shift位后 + 1，即计算x>>shift向上取整
int32_t luna_quant_ceil(int32_t x, int32_t shift); 

#ifdef __cplusplus
}
#endif
#endif /* _LS_CUTLINE_API_H_ */