/*
 * Driver_I2S.h
 *
 *  Created on: Sept. 27, 2020
 *
 */

#ifndef __DRIVER_I2S_H
#define __DRIVER_I2S_H

#include "Driver_Common.h"

#define CSK_I2S_API_VERSION CSK_DRIVER_VERSION_MAJOR_MINOR(1,0)  /* API version */

/****** I2S Control Codes *****/

/*----- I2S Control Codes: Configuration Parameters: MODE -----*/
#define CSK_I2S_MODE_Pos                                 0
#define CSK_I2S_MODE_Msk                                 (0x3UL << CSK_I2S_MODE_Pos) // bit[1:0], 2 bits
#define CSK_I2S_MODE_UNSET                               (0x0UL << CSK_I2S_MODE_Pos) // I2S mode is kept unchanged or default
#define CSK_I2S_MODE_MASTER                              (0x1UL << CSK_I2S_MODE_Pos) // I2S Master mode, arg = sample rate (if NOT 0)
#define CSK_I2S_MODE_SLAVE                               (0x2UL << CSK_I2S_MODE_Pos) // I2S Slave mode, arg = BCK / LRCK (if NOT 0) only
                                                                                     // when Right Justified mode, invalid in other cases

/*----- I2S Control Codes: Configuration Parameters: PROTOCOL -----*/
#define CSK_I2S_PROTO_Pos                                2
#define CSK_I2S_PROTO_Msk                                (0x7UL << CSK_I2S_PROTO_Pos) // bit[4:2], 3 bits
#define CSK_I2S_PROTO_UNSET                              (0x0UL << CSK_I2S_PROTO_Pos) // I2S protocol is kept unchanged or default
#define CSK_I2S_PROTO_PHILIPS                            (0x1UL << CSK_I2S_PROTO_Pos) // I2S Justified Mode(Philips)
#define CSK_I2S_PROTO_LEFT                               (0x2UL << CSK_I2S_PROTO_Pos) // Left Justified Mode
#define CSK_I2S_PROTO_RIGHT                              (0x3UL << CSK_I2S_PROTO_Pos) // Right Justified Mode
#define CSK_I2S_PROTO_PCMMODE_0                          (0x4UL << CSK_I2S_PROTO_Pos) // DSP/PCM mode 0
#define CSK_I2S_PROTO_PCMMODE_A                          CSK_I2S_PROTO_PCMMODE_0
#define CSK_I2S_PROTO_PCMMODE_1                          (0x5UL << CSK_I2S_PROTO_Pos) // DSP/PCM mode 1
#define CSK_I2S_PROTO_PCMMODE_B                          CSK_I2S_PROTO_PCMMODE_1
#define CSK_I2S_PROTO_LAST_INDEX                         0x05

/*----- I2S Control Codes: Configuration Parameters: DATA_FORMAT -----*/
#define CSK_I2S_DATA_FORMAT_Pos                          5
#define CSK_I2S_DATA_FORMAT_Msk                          (0x7UL << CSK_I2S_DATA_FORMAT_Pos) // bit[7:5], 3 bits
#define CSK_I2S_DATA_FORMAT_UNSET                        (0x0UL << CSK_I2S_DATA_FORMAT_Pos) // DATA_FORMAT is kept unchanged or default
#define CSK_I2S_DATA_FORMAT_DUAL_16BIT                   (0x1UL << CSK_I2S_DATA_FORMAT_Pos) // 16-bit {DATA1, DATA0}
#define CSK_I2S_DATA_FORMAT_24BIT_HIGH                   (0x2UL << CSK_I2S_DATA_FORMAT_Pos) // 24-bit {DATA, 8'd0}
#define CSK_I2S_DATA_FORMAT_32BIT                        (0x3UL << CSK_I2S_DATA_FORMAT_Pos) // 32-bit {DATA}
#define CSK_I2S_DATA_FORMAT_24BIT_LOW                    (0x4UL << CSK_I2S_DATA_FORMAT_Pos) // 24-bit {8'd0, DATA}
#define CSK_I2S_DATA_FORMAT_20BIT_HIGH                   (0x5UL << CSK_I2S_DATA_FORMAT_Pos) // 20-bit {DATA, 8'd0} same as 24BIT_HIGH
#define CSK_I2S_DATA_FORMAT_20BIT_LOW                    (0x6UL << CSK_I2S_DATA_FORMAT_Pos) // 20-bit {8'd0, DATA} same as 24BIT_LOW

/*----- I2S Control Codes: Configuration Parameters: TDM_CHANNELS -----*/
#define CSK_I2S_TDM_CHS_Pos                              8
#define CSK_I2S_TDM_CHS_Msk                              (0xFUL << CSK_I2S_TDM_CHS_Pos) // bit[11:8], 4 bits
#define CSK_I2S_TDM_CHS(n)                               (((n) & 0xF) << CSK_I2S_TDM_CHS_Pos) // TDM is not used if n == 0

/*----- I2S Control Codes: Configuration Parameters: TX MODE -----*/
//#define CSK_I2S_TXMODE_Pos                               12
//#define CSK_I2S_TXMODE_Msk                               (0x7UL << CSK_I2S_TXMODE_Pos) // bit[14:12], 3 bits
//#define CSK_I2S_TXMODE_UNSET                             (0x0UL << CSK_I2S_TXMODE_Pos) // TX_MODE is kept unchanged or default
//#define CSK_I2S_TXMODE_STEREO_STEREO                     (0x1UL << CSK_I2S_TXMODE_Pos) // stereo input form IFC, stereo output to pin
//#define CSK_I2S_TXMODE_MONOL_STEREO                      (0x2UL << CSK_I2S_TXMODE_Pos) // duplicate channel L input form IFC, stereo output to pin.
//#define CSK_I2S_TXMODE_MONOR_STEREO                      (0x3UL << CSK_I2S_TXMODE_Pos) // duplicate channel R input form IFC, stereo output to pin.
//#define CSK_I2S_TXMODE_MONO_MONO                         (0x4UL << CSK_I2S_TXMODE_Pos) // mono input from IFC, mono output to pin?

/*----- I2S Control Codes: Configuration Parameters: CHANNEL DATA MIX -----*/
/* For I2S Philips/Left/Right justified, L/R channel data CAN be separated in 2 different FIFOs or mixed in 1 same FIFO.
 * For PCM mode (support TDM), all channels' data are always mixed in 1 same FIFO */
//#define CSK_I2S_CHMIX_Pos                                15
// // Channel Mix Mode is kept unchanged or default
//#define CSK_I2S_CHMIX_Msk                                (0x7UL << CSK_I2S_CHMIX_Pos) // bit[17:15], 3 bits
//#define CSK_I2S_CHMIX_UNSET                              (0x0UL << CSK_I2S_CHMIX_Pos)
//// [default] separate IN data in L/R 2 channels, separate OUT data in L/R 2 channels
//#define CSK_I2S_CHMIX_IN_SEP_OUT_SEP                     (0x1UL << CSK_I2S_CHMIX_Pos)
//// separate IN data in L/R 2 channels, mix OUT data in 1 channel
//#define CSK_I2S_CHMIX_IN_SEP_OUT_MIX                     (0x2UL << CSK_I2S_CHMIX_Pos)
//// mix IN data in 1 channel, separate OUT data in L/R 2 channels
//#define CSK_I2S_CHMIX_IN_MIX_OUT_SEP                     (0x3UL << CSK_I2S_CHMIX_Pos)
//// mix IN data in 1 channel, mix OUT data in 1 channel
//#define CSK_I2S_CHMIX_IN_MIX_OUT_MIX                     (0x4UL << CSK_I2S_CHMIX_Pos)

//#define CSK_I2S_MIXIN_Pos                               15
// // IN Channel Mix Mode is kept unchanged or default
//#define CSK_I2S_MIXIN_Msk                               (0x3UL << CSK_I2S_MIXIN_Pos) // bit[16:15], 2 bits
//#define CSK_I2S_MIXIN_UNSET                             (0x0UL << CSK_I2S_MIXIN_Pos)
//// [default] Not mixed, separate IN data in L/R 2 channels
//#define CSK_I2S_MIXIN_NOT                               (0x1UL << CSK_I2S_MIXIN_Pos)
//// mix IN data in Left channel
//#define CSK_I2S_MIXIN_LEFT                              (0x2UL << CSK_I2S_MIXIN_Pos)
//// mix IN data in Right channel (DON'T SUPPORTED by venus6001 I2S)
//#define CSK_I2S_MIXIN_RIGHT                             (0x3UL << CSK_I2S_MIXIN_Pos)

//#define CSK_I2S_MIXOUT_Pos                              17
// // OUT Channel Mix Mode is kept unchanged or default
//#define CSK_I2S_MIXOUT_Msk                              (0x3UL << CSK_I2S_MIXOUT_Pos) // bit[18:17], 2 bits
//#define CSK_I2S_MIXOUT_UNSET                            (0x0UL << CSK_I2S_MIXOUT_Pos)
//// [default] Not mixed, separate OUT data in L/R 2 channels
//#define CSK_I2S_MIXOUT_NOT                              (0x1UL << CSK_I2S_MIXOUT_Pos)
//// mix OUT data in Left channel
//#define CSK_I2S_MIXOUT_LEFT                             (0x2UL << CSK_I2S_MIXOUT_Pos)
//// mix OUT data in Right channel (DON'T SUPPORTED by venus6001 I2S)
//#define CSK_I2S_MIXOUT_RIGHT                            (0x3UL << CSK_I2S_MIXOUT_Pos)

/*----- I2S Control Codes: Configuration Parameters: RX CHANNEL CONFIG -----*/
/* VALID ONLY for I2S Philips/Left/Right justified.
 * For PCM mode (support TDM), all channels' data are always mixed */
#define CSK_I2S_RXCH_Pos                                12
#define CSK_I2S_RXCH_Msk                                (0x3UL << CSK_I2S_RXCH_Pos) // bit[13:12], 2 bits
#define CSK_I2S_RXCH_UNSET                              (0x0UL << CSK_I2S_RXCH_Pos) // RXCH CONFIG is kept unchanged or default
#define CSK_I2S_RXCH_SEPA                               (0x1UL << CSK_I2S_RXCH_Pos) // RX channels'data are separate, read out respectively
#define CSK_I2S_RXCH_MIXED                              (0x2UL << CSK_I2S_RXCH_Pos) // RX channels'data are mixed, read out together

/*----- I2S Control Codes: Configuration Parameters: TX CHANNEL (and SRC) CONFIG -----*/
/* VALID ONLY for I2S Philips/Left/Right justified.
 * For PCM mode (support TDM), all channels' data are always mixed */
#define CSK_I2S_TXCH_Pos                                14
#define CSK_I2S_TXCH_Msk                                (0x7UL << CSK_I2S_TXCH_Pos) // bit[16:14], 3 bits
#define CSK_I2S_TXCH_UNSET                              (0x0UL << CSK_I2S_TXCH_Pos) // TXCH CONFIG is kept unchanged or default
#define CSK_I2S_TXCH_MONO_SRC_MONO                      (0x1UL << CSK_I2S_TXCH_Pos) // mono channel data, sent to mono channel or one of L/R channels
#define CSK_I2S_TXCH_STEREO_SRC_MONO                    (0x2UL << CSK_I2S_TXCH_Pos) // mono channel data, duplicated and sent to both L&R channels
#define CSK_I2S_TXCH_STEREO_SRC_STEREO                  (0x3UL << CSK_I2S_TXCH_Pos) // stereo channel data, sent to L&R channels respectively

/*----- I2S Control Codes: Exclusive Controls -----*/
/*----- exclusive operations, CANNOT coexist with other Control Codes -----*/
#define CSK_I2S_EXCL_OP_Pos                 21
#define CSK_I2S_EXCL_OP_Msk                 (0x7UL << CSK_I2S_EXCL_OP_Pos)      // bit[23:21], 3 bits
#define CSK_I2S_EXCL_OP_UNSET               (0UL << CSK_I2S_EXCL_OP_Pos)        // NO exclusive operations
#define CSK_I2S_ABORT_TRANSFER              (1UL << CSK_I2S_EXCL_OP_Pos)        // Abort current data transfer, arg indicates IN,OUT,ECHO channels
                                                                                // arg = (ch_bmp_echo << 16)|(ch_bmp_out << 8)|(ch_bmp_in)
#define CSK_I2S_GET_SAMP_RATE               (2UL << CSK_I2S_EXCL_OP_Pos)        // Get sample rate, return sample rate
#define CSK_I2S_SET_SAMP_RATE               (3UL << CSK_I2S_EXCL_OP_Pos)        // Set sample rate, arg = sample rate
#define CSK_I2S_SET_ECHO_PARAMS             (4UL << CSK_I2S_EXCL_OP_Pos)        // Set ECHO parameters, arg = pointer to ECHO_PARAMS

/* The following I2S Control Codes are NOT IMPLEMENTED by I2S driver unless otherwise stated , for future use -----*/

/*----- I2S Control Codes: Configuration Parameters: BCK_OUTPUT_GATE_AFTER_SENT -----*/
#define CSK_I2S_BCKOUT_GATE_Pos                          24
#define CSK_I2S_BCKOUT_GATE_Msk                          (0x1UL << CSK_I2S_BCKOUT_GATE_Pos) // bit[24], 1 bit
#define CSK_I2S_BCKOUT_GATE_NOGATE                       (0x0UL << CSK_I2S_BCKOUT_GATE_Pos) // No gate
#define CSK_I2S_BCKOUT_GATE_GATED                        (0x1UL << CSK_I2S_BCKOUT_GATE_Pos) // Gated (no output after sent)

/*----- I2S Control Codes: Configuration Parameters: BIT_ORDER -----*/
#define CSK_I2S_BIT_ORDER_Pos                            25
#define CSK_I2S_BIT_ORDER_Msk                            (0x1UL << CSK_I2S_BIT_ORDER_Pos) // bit[25], 1 bit
#define CSK_I2S_BIT_ORDER_MSB                            (0x0UL << CSK_I2S_BIT_ORDER_Pos) // MSB first
#define CSK_I2S_BIT_ORDER_LSB                            (0x1UL << CSK_I2S_BIT_ORDER_Pos) // LSB first

/*----- I2S Control Codes: Configuration Parameters: DEBUG_MODE -----*/
#define CSK_I2S_DBGMODE_Pos                              26
#define CSK_I2S_DBGMODE_Msk                              (0x1UL << CSK_I2S_DBGMODE_Pos) // bit[26], 1 bit
#define CSK_I2S_DBGMODE_NORMAL                           (0x0UL << CSK_I2S_DBGMODE_Pos) // Normal
#define CSK_I2S_DBGMODE_LOOPBACK                         (0x1UL << CSK_I2S_DBGMODE_Pos) // Loop back (for debug only, not work for DAI)

/*----- I2S Control Codes: Configuration Parameters: SWAP_IN_CHLR -----*/
#define CSK_I2S_IN_CHLR_Pos                              27
#define CSK_I2S_IN_CHLR_Msk                              (0x1UL << CSK_I2S_IN_CHLR_Pos) // bit[27], 1 bit
#define CSK_I2S_IN_CHLR_NORM                             (0x0UL << CSK_I2S_IN_CHLR_Pos) // NOT swap IN L/R channel
#define CSK_I2S_IN_CHLR_SWAP                             (0x1UL << CSK_I2S_IN_CHLR_Pos) // swap IN L/R channel

/*----- I2S Control Codes: Configuration Parameters: SWAP_OUT_CHLR -----*/
#define CSK_I2S_OUT_CHLR_Pos                             28
#define CSK_I2S_OUT_CHLR_Msk                             (0x1UL << CSK_I2S_SWAP_LROUT_Pos) // bit[28], 1 bit
#define CSK_I2S_OUT_CHLR_NORM                            (0x0UL << CSK_I2S_SWAP_LROUT_Pos) // NOT swap OUT L/R channel
#define CSK_I2S_OUT_CHLR_SWAP                            (0x1UL << CSK_I2S_SWAP_LROUT_Pos) // swap OUT L/R channel

/*----- I2S Control Codes: Configuration Parameters: LRCK_POL -----*/
#define CSK_I2S_LRCK_POL_Pos                             29
#define CSK_I2S_LRCK_POL_Msk                             (0x1UL << CSK_I2S_LRCK_POL_Pos) // bit[29], 1 bit
#define CSK_I2S_LRCK_POL_NORM                            (0x0UL << CSK_I2S_LRCK_POL_Pos) // Normal (Low Idle?)
#define CSK_I2S_LRCK_POL_INVT                            (0x1UL << CSK_I2S_LRCK_POL_Pos) // Invert (High Idle?)

/*----- I2S Control Codes: Configuration Parameters: BCK_POL -----*/
#define CSK_I2S_BCK_POL_Pos                              30
#define CSK_I2S_BCK_POL_Msk                              (0x1UL << CSK_I2S_BCK_POL_Pos) // bit[30], 1 bit
#define CSK_I2S_BCK_POL_NORM                             (0x0UL << CSK_I2S_BCK_POL_Pos) // Left High Right Low
#define CSK_I2S_BCK_POL_INVT                             (0x1UL << CSK_I2S_BCK_POL_Pos) // Left Low Right High


/****** I2S specific error codes *****/
#define CSK_I2S_ERROR_MODE              (CSK_DRIVER_ERROR_SPECIFIC - 1)     // Specified Mode not supported
#define CSK_I2S_ERROR_PROTOCOL          (CSK_DRIVER_ERROR_SPECIFIC - 2)     // Specified Protocol not supported
#define CSK_I2S_ERROR_DATA_FORMAT       (CSK_DRIVER_ERROR_SPECIFIC - 3)     // Specified Data Format not supported
#define CSK_I2S_ERROR_RXCH_CONFIG       (CSK_DRIVER_ERROR_SPECIFIC - 4)     // Specified RX Channel Config not supported
#define CSK_I2S_ERROR_TXCH_CONFIG       (CSK_DRIVER_ERROR_SPECIFIC - 5)     // Specified TX Channel Config not supported


//------------------------------------------------------------------------------------------
//// I2S IN channel index for audio recording
//typedef enum {
//    I2S_CH_IN0 = 0,
//    I2S_CH_INL = I2S_CH_IN0, // left channel
//    I2S_CH_IN1,
//    I2S_CH_INR = I2S_CH_IN1, // right channel
//    I2S_CHCNT_IN
//} I2S_CH_IN;
//
//// I2S OUT channel index for audio playback
//typedef enum {
//    I2S_CH_OUT0 = 0,
//    I2S_CH_OUTL = I2S_CH_OUT0, // left channel
//    I2S_CH_OUT1,
//    I2S_CH_OUTR = I2S_CH_OUT1, // right channel
//    I2S_CHCNT_OUT
//} I2S_CH_OUT;
//
//// I2S LR channel index for audio recording / palyback
//typedef enum {
//    I2S_CH0 = 0,
//    I2S_CH_LEFT = I2S_CH0, // left channel
//    I2S_CH1,
//    I2S_CH_RIGHT = I2S_CH1, // right channel
//    I2S_CHCNT
//} I2S_CH;
//
//#define I2S_CH_BMP_LEFT    (0x1 << I2S_CH_LEFT)
//#define I2S_CH_BMP_RIGHT   (0x1 << I2S_CH_RIGHT)
//#define I2S_CH_BMP_STEREO  (I2S_CH_BMP_LEFT | I2S_CH_BMP_RIGHT)

//#define I2S_CH_BMP_LEFT    CH_BMP_LEFT
//#define I2S_CH_BMP_RIGHT   CH_BMP_RIGHT
//#define I2S_CH_BMP_STEREO  CH_BMP_STEREO

// supported protocol of CSK I2S
typedef enum {
    I2S_PROTO_UNKNOWN       =   0,
    I2S_PROTO_PHILIPS       =   (CSK_I2S_PROTO_PHILIPS >> CSK_I2S_PROTO_Pos),
    I2S_PROTO_LEFT          =   (CSK_I2S_PROTO_LEFT >> CSK_I2S_PROTO_Pos),
    I2S_PROTO_RIGHT         =   (CSK_I2S_PROTO_RIGHT >> CSK_I2S_PROTO_Pos),
    I2S_PROTO_PCMMODE_0     =   (CSK_I2S_PROTO_PCMMODE_0 >> CSK_I2S_PROTO_Pos),
    I2S_PROTO_PCMMODE_A     =   I2S_PROTO_PCMMODE_0,
    I2S_PROTO_PCMMODE_1     =   (CSK_I2S_PROTO_PCMMODE_1 >> CSK_I2S_PROTO_Pos),
    I2S_PROTO_PCMMODE_B     =   I2S_PROTO_PCMMODE_1,
    I2S_PROTO_COUNT
} I2S_PROTOCOL;

// supported sample rate array of CSK I2S
static const uint32_t csk_i2s_samp_rates[] = {
        96000,
        48000,
        24000,
        32000,
        16000,
        8000,
        44100,
        22050,
        11025
};

// I2S status bit definitions
typedef struct _CSK_I2S_STATUS_BIT
{
    uint32_t rx_busy :1;       // Receiver busy flag
    uint32_t tx_busy :1;       // Transmitter busy flag
    uint32_t ech_busy :1;      // ECHO Receiver busy flag
    uint32_t rx_ovf :1;     // Receiver overflow (cleared on start of Receive operation)
    uint32_t tx_unf :1;     // Transmit underflow (cleared on start of Send operation)
    uint32_t ech_ovf :1;     // ECHO Receiver overflow (cleared on start of ECHO Receive operation)
    uint32_t master :1;     // 0 = slave, 1 = master
    uint32_t reserved :25;
} CSK_I2S_STATUS_BIT;

// I2S status
typedef union {
    uint32_t all;
    CSK_I2S_STATUS_BIT bit;
} CSK_I2S_STATUS;


///****** I2S Event *****/
#define CSK_I2S_EVENT_RECEIVE_COMPLETE      (0x1UL << 0) ///< Data Receive completed
#define CSK_I2S_EVENT_TRANSMIT_COMPLETE     (0x1UL << 1) ///< Data Transmit completed

#define CSK_I2S_EVENT_RX_FIFO_OVERRUN       (0x1UL << 2) ///< Data Receive overflow
#define CSK_I2S_EVENT_TX_FIFO_UNDERRUN      (0x1UL << 3) ///< Data Transmit underflow
#define CSK_I2S_EVENT_RX_FIFO_FULL          (0x1UL << 4) ///< Data Receive full
#define CSK_I2S_EVENT_TX_FIFO_EMPTY         (0x1UL << 5) ///< Data Transmit empty

#define CSK_I2S_EVENT_ECHO_RX_COMPLETE      (0x1UL << 6) ///< ECHO Data Receive completed
#define CSK_I2S_EVENT_OTHER_ERROR           (0x1UL << 7) ///< Other Error


/**
 \fn          void CSK_I2S_SignalEvent_t (uint32_t event, uint32_t usr_param)
 \brief       Signal I2S Events.
 \param[in]   event_info I2S event and channel information
              bit[7:0] is event type, bit[15:8] is I2S channel number,
              bit[16] indicate the direction, 1 = IN, 0 = OUT
              (NOTE: I2S IN channels and OUT ones are numbered separately)
 \param[in]   usr_param    user parameter
 \return      none
*/
typedef void
(*CSK_I2S_SignalEvent_t)(uint32_t event_info, uint32_t usr_param);

//------------------------------------------------------------------------------------------
/**
 \fn          CSK_DRIVER_VERSION I2S_GetVersion (void)
 \brief       Get driver version.
 \return      \ref CSK_DRIVER_VERSION
*/
CSK_DRIVER_VERSION
I2S_GetVersion();

/**
 \fn          int32_t I2S_Initialize (void *i2s_dev, CSK_I2S_SignalEvent_t cb_event, uint32_t usr_param)
 \brief       Initialize I2S Interface.
 \param[in]   i2s_dev  Pointer to I2S device instance
 \param[in]   cb_event  Pointer to \ref CSK_I2S_SignalEvent_t
 \param[in]   usr_param  User-defined value, acts as last parameter of cb_event
 \return      \ref execution_status
*/
//int32_t
//I2S_Initialize(void *i2s_dev, CSK_I2S_SignalEvent_t cb_event, uint32_t usr_param,
//                uint8_t ch_bmp_in, uint8_t ch_bmp_out, uint8_t use_alt_in);

// bit[0]=1 indicates to use alternate IN channel, else use normal IN channel for I2Sx
#define I2S_INIT_FLAG_USE_ALT_IN   (0x1 << 0)
//// bit[1]=1 indicates to need ECHO data while TX audio data through the ECHO channel
//#define I2S_INIT_FLAG_NEED_ECHO   (0x1 << 1)

int32_t
I2S_Initialize(void *i2s_dev, CSK_I2S_SignalEvent_t cb_event, uint32_t usr_param,
                uint8_t ch_bmp_in, uint8_t ch_bmp_out, uint8_t ch_bmp_echo, uint8_t init_flag);

/**
 \fn          int32_t I2S_Uninitialize (void)
 \brief       De-initialize I2S Interface.
 \param[in]   i2s_dev  Pointer to I2S device instance
 \return      \ref execution_status
*/
int32_t
I2S_Uninitialize(void *i2s_dev);

/**
 \fn          int32_t I2S_PowerControl (void *i2s_dev, CSK_POWER_STATE state)
 \brief       Control I2S Interface Power.
 \param[in]   i2s_dev  Pointer to I2S device instance
 \param[in]   state  Power state
 \return      \ref execution_status
*/
int32_t
I2S_PowerControl(void *i2s_dev, CSK_POWER_STATE state);

/**
 \fn          int32_t I2S_Send (void *i2s_dev, const void *data, uint32_t num)
 \brief       Start sending data to I2S out channel.
 \param[in]   i2s_dev  Pointer to I2S device instance
 \param[in]   ch_no  I2S channel number (data is sent on the channel)
 \param[in]   data  Pointer to buffer with data to be sent
 \param[in]   num   Number of data items to send
 \return      \ref execution_status
*/

// bit[0]=1 indicates Start sending immediately, or else
//  it will NOT transfer data until I2S_Enable_Channels is called
#define I2S_TX_FLAG_START_NOW   (0x1 << 0)

int32_t
I2S_Send(void *i2s_dev, const uint32_t *data, uint32_t num, uint8_t ch_bmp, uint8_t tx_flag);

int32_t
I2S_Send_LLP(void *i2s_dev, AUDIO_BUFFER_USER *bufs, uint32_t buf_cnt, uint8_t ch_bmp, uint8_t tx_flag);

// multiple channels' audio data are interlaced in memory, and played back through respective channels
//int32_t
//I2S_Mul_Send(void *i2s_dev, uint32_t *ch_nums, uint32_t ch_cnt,
//            const void *data, uint32_t num);

// multiple channels' audio data are interlaced in memory, and played back through respective channels
//int32_t
//I2S_Mul_Send_LLP(void *i2s_dev, uint32_t *ch_nums, uint32_t ch_cnt,
//                AUDIO_BUFFER_USER *bufs, uint32_t buf_cnt);

/**
 \fn          int32_t I2S_Receive (void *i2s_dev, void *data, uint32_t num)
 \brief       Start receiving data from I2S in channel.
 \param[in]   i2s_dev  Pointer to I2S device instance
 \param[in]   ch_no  I2S channel number (data is received on the channel)
 \param[out]  data  Pointer to buffer for data to receive from I2S in channel
 \param[in]   num   Number of data items to receive
 \return      \ref execution_status
*/

// bit[0]=1 indicates Start receiving immediately, or else
// it will NOT transfer data until I2S_Enable_Channels is called
#define I2S_RX_FLAG_START_NOW   (0x1 << 0)

int32_t
I2S_Receive(void *i2s_dev, uint32_t *data, uint32_t num, uint8_t ch_bmp, uint8_t rx_flag);

int32_t
I2S_Receive_LLP(void *i2s_dev, AUDIO_BUFFER_USER *bufs, uint32_t buf_cnt, uint8_t ch_bmp, uint8_t rx_flag);

int32_t
I2S_Echo_Receive(void *i2s_dev, uint32_t *data, uint32_t num, uint8_t ch_bmp);

int32_t
I2S_Echo_Receive_LLP(void *i2s_dev, AUDIO_BUFFER_USER *bufs, uint32_t buf_cnt, uint8_t ch_bmp);

/**
 \fn          int32_t I2S_Abort_Channels (void *i2s_dev, uint8_t ch_bmp_in, uint8_t ch_bmp_out)
 \brief       Abort data transfer of I2S in and/or out channels if any.
 \param[in]   i2s_dev  Pointer to I2S device instance
 \param[in]   ch_bmp_in  I2S in channel bitmap (bit0 for I2S_CH_IN0, bit1 for I2S_CH_IN1, ...)
 \param[in]   ch_bmp_out  I2S out channel bitmap (bit0 for I2S_CH_OUT0, bit1 for I2S_CH_OUT1, ...)
 \return      \ref execution_status
*/
int32_t
I2S_Abort_Channels(void *i2s_dev, uint8_t ch_bmp_in, uint8_t ch_bmp_out, uint8_t ch_bmp_echo);

/**
 \fn          int32_t I2S_Enable_Channels (void *i2s_dev, uint8_t ch_bmp_in, uint8_t ch_bmp_out)
 \brief       Enable I2S in and/or out channels, and data are started to transfer on the lines
              from now on if I2s_Receive_XXX and/or I2s_Send_XXX are called before.
 \param[in]   i2s_dev  Pointer to I2S device instance
 \param[in]   ch_bmp_in  I2S in channel bitmap (bit0 for I2S_CH_IN0, bit1 for I2S_CH_IN1, ...)
 \param[in]   ch_bmp_out  I2S out channel bitmap (bit0 for I2S_CH_OUT0, bit1 for I2S_CH_OUT1, ...)
 \return      \ref execution_status
*/
int32_t
I2S_Enable_Channels(void *i2s_dev, uint8_t ch_bmp_in, uint8_t ch_bmp_out);

/**
 \fn          int32_t I2S_Disable_Channels (void *i2s_dev, uint8_t ch_bmp_in, uint8_t ch_bmp_out)
 \brief       Disable I2S in and/or out channels (and data transfer on the lines are suspended if any).
 \param[in]   i2s_dev  Pointer to I2S device instance
 \param[in]   ch_bmp_in  I2S in channel bitmap (bit0 for I2S_CH_IN0, bit1 for I2S_CH_IN1, ...)
 \param[in]   ch_bmp_out  I2S out channel bitmap (bit0 for I2S_CH_OUT0, bit1 for I2S_CH_OUT1, ...)
 \return      \ref execution_status
*/
int32_t
I2S_Disable_Channels(void *i2s_dev, uint8_t ch_bmp_in, uint8_t ch_bmp_out);

/**
 \fn          uint32_t I2S_GetTxCount (void *i2s_dev)
 \brief       Get transferred data count.
 \param[in]   i2s_dev  Pointer to I2S device instance
 \return      number of data items transferred if positive,
              error value if negative.
*/
int32_t
I2S_GetTxCount(void *i2s_dev, uint8_t ch_bmp);

/**
 \fn          uint32_t I2S_GetRxCount (void *i2s_dev)
 \brief       Get transferred data count.
 \param[in]   i2s_dev  Pointer to I2S device instance
 \return      number of data items transferred if positive,
              error value if negative.
*/
int32_t
I2S_GetRxCount(void *i2s_dev, uint8_t ch_bmp);

/**
 \fn          uint32_t I2S_GetEchoCount
 \brief       Get transferred echo data count.
 \param[in]   i2s_dev  Pointer to I2S device instance
 \return      number of data items transferred if positive,
              error value if negative.
*/
int32_t
I2S_GetEchoCount(void *i2s_dev, uint8_t ch_bmp);

/**
 \fn          int32_t I2S_Control (void *i2s_dev, uint32_t control, uint32_t arg)
 \brief       Control I2S Interface.
 \param[in]   i2s_dev  Pointer to I2S device instance
 \param[in]   control  Operation
 \param[in]   arg  Argument of operation (optional), i.e. the speed of i2s when as master
 \return      common \ref execution_status and driver specific \ref i2s execution_status
*/
int32_t
I2S_Control(void *i2s_dev, uint32_t control, uint32_t arg);

/**
 \fn          int32_t I2S_GetStatus (void *spi_dev, CSK_I2S_STATUS *status)
 \brief       Get I2S status.
 \param[in]   i2s_dev  Pointer to I2S device instance
 \param[out]  status  Pointer to CSK_I2S_STATUS buffer
 \return      \ref execution_status
 */
int32_t
I2S_GetStatus(void *i2s_dev, CSK_I2S_STATUS *status);


// EQ API
int32_t I2S_EQ_Set_Coef_Array(void *i2s_dev, uint32_t *eqcoefs, uint32_t num);
int32_t I2S_EQ_Set_Coef(void *i2s_dev, uint32_t index, uint32_t eqcoef);
int32_t I2S_EQ_Enable(void *i2s_dev, uint32_t stages);
int32_t I2S_EQ_Disble(void *i2s_dev);
int32_t I2S_EQ_Clear(void *i2s_dev, uint8_t wait_done);

//------------------------------------------------------------------------------------------
/**
 \fn          void* I2S0()
 \brief       Get I2S0 device instance
 \return      I2S0 device instance
 */
void* I2S0();

/**
 \fn          void* I2S1()
 \brief       Get I2S1 device instance
 \return      I2S1 device instance
 */
void* I2S1();

/**
 \fn          void* I2S2()
 \brief       Get I2S2 device instance
 \return      I2S2 device instance
 */
void* I2S2();

#endif /* __DRIVER_I2S_H */
