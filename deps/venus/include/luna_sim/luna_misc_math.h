/***************************************************************************
 * luna_misc_math.h                                                        *
 *                                                                         *
 * Copyright (C) 2020 listenai Co.Ltd                   			       *
 * All rights reserved.                                                    *
 ***************************************************************************/
#ifndef LIBS_LUNA_LUNA_MISC_MATH_H_SIM_
#define LIBS_LUNA_LUNA_MISC_MATH_H_SIM_

#include "luna_math_types.h"

#ifndef MASK_SIM_TYPEDEF
typedef enum {
	LUNA_ACTIVATION_SIGMOID 	= 0,
	LUNA_ACTIVATION_RELU,
	LUNA_ACTIVATION_PRELU,

	LUNA_ACTIVATION_END
} LUNA_ACTIVATION;
#endif //MASK_SIM_TYPEDEF

int32_t LUNA_API_SIM(luna_matT_add_vector_q15)(const q15_t *src1, const q15_t *src2, q15_t *dst, uint32_t m, uint32_t n, uint32_t shift);
int32_t LUNA_API_SIM(luna_matT_add_vector_q31)(const q31_t *src1, const q31_t *src2, q31_t *dst, uint32_t m, uint32_t n, uint32_t shift);

int32_t LUNA_API_SIM(luna_sigmoid)(const q15_t *src, q15_t *dst, uint32_t size);
int32_t LUNA_API_SIM(luna_tanh)(const q15_t *src, q15_t *dst, uint32_t size);

int32_t LUNA_API_SIM(luna_relu_q7_int8)(const q7_t *src, int8_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_relu_q7_int16)(const q7_t *src, int16_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_relu_q7_int32)(const q7_t *src, int32_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_relu_q15_int8)(const q15_t *src, int8_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_relu_q15_int16)(const q15_t *src, int16_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_relu_q15_int32)(const q15_t *src, int32_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_relu_q31_int8)(const q31_t *src, int8_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_relu_q31_int16)(const q31_t *src, int16_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_relu_q31_int32)(const q31_t *src, int32_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_prelu_q7_int8)(const q7_t *src, uint32_t slope, int8_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_prelu_q7_int16)(const q7_t *src, uint32_t slope, int16_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_prelu_q7_int32)(const q7_t *src, uint32_t slope, int32_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_prelu_q15_int8)(const q15_t *src, uint32_t slope, int8_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_prelu_q15_int16)(const q15_t *src, uint32_t slope, int16_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_prelu_q15_int32)(const q15_t *src, uint32_t slope, int32_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_prelu_q31_int8)(const q31_t *src, uint32_t slope, int8_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_prelu_q31_int16)(const q31_t *src, uint32_t slope, int16_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_prelu_q31_int32)(const q31_t *src, uint32_t slope, int32_t *dst, uint32_t size, uint32_t post_shift);
int32_t LUNA_API_SIM(luna_memcpy)(void* dst, void* src, int size);
int32_t LUNA_API_SIM(luna_memset)(void *dst, q7_t value, uint32_t size);

#endif /* LIBS_LUNA_LUNA_MISC_MATH_H_SIM_ */
