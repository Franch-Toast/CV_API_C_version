/*
 * Driver_VAD.h
 *
 *  Created on: 2021年9月10日
 *      Author: USER
 */

#ifndef INCLUDE_DRIVER_DRIVER_VAD_H_
#define INCLUDE_DRIVER_DRIVER_VAD_H_

#include "Driver_Common.h"
#include "venus_cp.h"

typedef struct {
    uint8_t iir_overflow   : 1;
    uint8_t mem_bypassed   : 1;
    uint8_t vad_found      : 1;
    uint8_t end_addr_valid : 1;
    uint8_t rsv            : 4;
} HAL_VAD_StateTypeDef;

/**************IIR PARAMETER**************/
typedef enum {
    VAD_IIR1 = 0,
    VAD_IIR2,
    VAD_IIR3,
    VAD_IIR4,
    VAD_IIR5,
} VAD_IIR;

typedef struct _VAD_IIR_PARAMETER{
    uint8_t iir_filter_order;
    uint8_t iir_b_coef_shft;
    uint32_t vad_iir_b1;
    uint32_t vad_iir_b2;
    uint32_t vad_iir_b3;
    uint32_t vad_iir_ma2;
    uint32_t vad_iir_ma3;
} VAD_IIR_PARAMETER;

/**************AMPL PARAMETER**************/
typedef enum {
    VAD_PRE_AMPL,
    VAD_POST_AMPL,
} VAD_AMPL;

typedef struct _VAD_AMPL_PARAMETER{
    uint8_t ampl_by_8;
    uint8_t ampl_ratio;
} VAD_AMPL_PARAMETER;

/**************DEC PARAMETER**************/
typedef struct {
    bool critr0_en;
    bool critr1_en;
    bool critr2_en;
    bool critr3_en;
    bool critr4_en;
    bool critr5_en;
    bool critr6_en;
    bool critr7_en;
    bool critr8_en;
} VAD_DEC_EN;

typedef struct _VAD_DEC_PARAMETER{
    uint16_t zch_tol;
    uint16_t zch_minamp;
    uint16_t zch_maxamp;
    uint16_t amp_l;
    uint16_t amp_h;
    uint16_t zcr_l;
    uint16_t zcr_h;
    uint8_t  minlen_trans_neg;
    uint8_t  minlen_trans_pos;
    uint8_t  minlen;
    uint8_t  maxsilence;
} VAD_DEC_PARAMETER;

typedef enum {
    HAL_VAD_CHANNEL_1 = 0,
    HAL_VAD_CHANNEL_2,
} HAL_VAD_ChannleTypeDef;

typedef enum {
	HAL_VAD_SUBBLOCKS_2 = 0,
	HAL_VAD_SUBBLOCKS_3 = 1,
} HAL_VAD_SubblockTypeDef;

/// Get start address
#define __HAL_VAD_GET_START_ADDR(s_addr)   \
do { \
    s_addr = IP_VAD->REG_START_ADDR.all; \
}while(0)

/// Get current address
#define __HAL_VAD_GET_CUR_ADDR(c_addr)   \
do { \
    c_addr = IP_VAD->REG_CUR_ADDR.all; \
}while(0)

/// Get end address
#define __HAL_VAD_GET_END_ADDR(e_addr)   \
do { \
    e_addr = IP_VAD->REG_END_ADDR.bit.END_ADDR; \
}while(0)

/// Waiting end address valid
#define __HAL_VAD_STOP_VALID()   \
do { \
    IP_VAD->REG_CTRL.bit.SRAM_WR_STOP = 0x1; \
    while(!IP_VAD->REG_STATE.bit.END_ADDR_VALID); \
    IP_VAD->REG_STATE.bit.END_ADDR_VALID = 0x1; \
}while(0)

/// Set trace back length
#define __HAL_TRACBK_LEN(len)   \
do { \
    IP_VAD->REG_TRACBK_LEN.bit.TRACBK_LEN = len; \
}while(0)

#define __HAL_SUBBLK_TYPE(type)   \
do { \
    IP_VAD->REG_BLKCTRL.bit.BLK_TYPE = type; \
}while(0)

#define __HAL_SUBBLK_LEN(len)   \
do { \
    IP_VAD->REG_BLKCTRL.bit.SUBBLK_SAMP_LEN = len; \
}while(0)

#define VAD_INNER_SRAM_BASE          0x46E10000
#define VAD_INNER_SRAM_SIZE          32768 // bytes

int32_t HAL_VAD_Init(void);

int32_t HAL_VAD_Open(HAL_VAD_ChannleTypeDef channel);

int32_t HAL_VAD_Close(void);

HAL_VAD_StateTypeDef HAL_VAD_Status(void);

int32_t HAL_VAD_IIR_ParameterConfig(VAD_IIR iir, VAD_IIR_PARAMETER* para, bool en);

int32_t HAL_VAD_AMPL_ParameterConfig(VAD_AMPL ampl, VAD_AMPL_PARAMETER* para, bool en);

int32_t HAL_VAD_DEC_ParameterConfig(VAD_DEC_EN* dec, VAD_DEC_PARAMETER* para);

#endif /* INCLUDE_DRIVER_DRIVER_VAD_H_ */
