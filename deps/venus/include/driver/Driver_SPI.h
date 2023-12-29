/*
 * Project:      SPI (Serial Peripheral Interface) Driver definitions
 */

#ifndef __DRIVER_SPI_H
#define __DRIVER_SPI_H

#include "Driver_Common.h"

#define CSK_SPI_API_VERSION CSK_DRIVER_VERSION_MAJOR_MINOR(1,0)  /* API version */


/****** SPI Control Codes *****/

/*----- SPI Control Codes: Mode -----*/
#define CSK_SPI_MODE_Pos                0
#define CSK_SPI_MODE_Msk                (0xFUL << CSK_SPI_MODE_Pos)     // bit[3:0]
#define CSK_SPI_MODE_UNSET              (0x00UL << CSK_SPI_MODE_Pos)    ///< SPI Mode is kept unchanged
#define CSK_SPI_MODE_MASTER             (0x01UL << CSK_SPI_MODE_Pos)    ///< SPI Master (Output on MOSI, Input on MISO); arg = Bus Speed in bps
#define CSK_SPI_MODE_SLAVE              (0x02UL << CSK_SPI_MODE_Pos)    ///< SPI Slave  (Output on MISO, Input on MOSI)

/*----- SPI Control Codes: TX I/O -----*/
#define CSK_SPI_TXIO_Pos                4
#define CSK_SPI_TXIO_Msk                (3UL << CSK_SPI_TXIO_Pos)       // bit[5:4]
#define CSK_SPI_TXIO_UNSET              (0x00UL << CSK_SPI_TXIO_Pos)    ///< SPI TX IO is kept unchanged or default (AUTO)
#define CSK_SPI_TXIO_DMA                (0x01UL << CSK_SPI_TXIO_Pos)    ///< SPI TX with DMA
#define CSK_SPI_TXIO_PIO                (0x02UL << CSK_SPI_TXIO_Pos)    ///< SPI TX with PIO
#define CSK_SPI_TXIO_BOTH               (CSK_SPI_TXIO_DMA | CSK_SPI_TXIO_PIO)    // SPI TX with DMA & PIO
#define CSK_SPI_TXIO_AUTO               CSK_SPI_TXIO_BOTH               ///< SPI TX: DMA preferred, PIO if DMA unavailable
//#define CSK_SPI_TXIO_AUTO               (0x03UL << CSK_SPI_TXIO_Pos)    ///< SPI TX: DMA preferred, PIO if DMA unavailable

/*----- SPI Control Codes: RX I/O -----*/
#define CSK_SPI_RXIO_Pos                6
#define CSK_SPI_RXIO_Msk                (3UL << CSK_SPI_RXIO_Pos)       // bit[7:6]
#define CSK_SPI_RXIO_UNSET              (0x00UL << CSK_SPI_RXIO_Pos)    ///< SPI RX IO is kept unchanged or default (AUTO)
#define CSK_SPI_RXIO_DMA                (0x01UL << CSK_SPI_RXIO_Pos)    ///< SPI RX with DMA
#define CSK_SPI_RXIO_PIO                (0x02UL << CSK_SPI_RXIO_Pos)    ///< SPI RX with PIO
#define CSK_SPI_RXIO_BOTH               (CSK_SPI_RXIO_DMA | CSK_SPI_RXIO_PIO)    // SPI RX with DMA & PIO
#define CSK_SPI_RXIO_AUTO               CSK_SPI_RXIO_BOTH               ///< SPI RX: DMA preferred, PIO if DMA unavailable
//#define CSK_SPI_RXIO_AUTO               (0x03UL << CSK_SPI_RXIO_Pos)    ///< SPI RX: DMA preferred, PIO if DMA unavailable

/*----- SPI Control Codes: Mode Parameters: Frame Format -----*/
#define CSK_SPI_FRAME_FORMAT_Pos         8
#define CSK_SPI_FRAME_FORMAT_Msk        (0xFUL << CSK_SPI_FRAME_FORMAT_Pos) // bit[11:8]
#define CSK_SPI_FRM_FMT_UNSET           (0UL << CSK_SPI_FRAME_FORMAT_Pos)   ///< SPI Frame Format is kept unchanged or default
#define CSK_SPI_CPOL0_CPHA0             (1UL << CSK_SPI_FRAME_FORMAT_Pos)   ///< Clock Polarity 0, Clock Phase 0 (default)
#define CSK_SPI_CPOL0_CPHA1             (2UL << CSK_SPI_FRAME_FORMAT_Pos)   ///< Clock Polarity 0, Clock Phase 1
#define CSK_SPI_CPOL1_CPHA0             (3UL << CSK_SPI_FRAME_FORMAT_Pos)   ///< Clock Polarity 1, Clock Phase 0
#define CSK_SPI_CPOL1_CPHA1             (4UL << CSK_SPI_FRAME_FORMAT_Pos)   ///< Clock Polarity 1, Clock Phase 1
//#define CSK_SPI_TI_SSI                  (5UL << CSK_SPI_FRAME_FORMAT_Pos)   ///< Texas Instruments Frame Format
//#define CSK_SPI_MICROWIRE               (6UL << CSK_SPI_FRAME_FORMAT_Pos)   ///< National Microwire Frame Format

/*----- SPI Control Codes: Mode Parameters: Data Bits -----*/
#define CSK_SPI_DATA_BITS_Pos            12
#define CSK_SPI_DATA_BITS_Msk           (0x3FUL << CSK_SPI_DATA_BITS_Pos)       // bit[17:12]
#define CSK_SPI_DATA_BITS_UNSET         (0UL << CSK_SPI_DATA_BITS_Pos)          ///< Number of Data bits is kept unchanged
#define CSK_SPI_DATA_BITS(n)            (((n) & 0x3F) << CSK_SPI_DATA_BITS_Pos) ///< Number of Data bits

/*----- SPI Control Codes: Mode Parameters: Bit Order -----*/
#define CSK_SPI_BIT_ORDER_Pos            18
#define CSK_SPI_BIT_ORDER_Msk           (3UL << CSK_SPI_BIT_ORDER_Pos)      // bit[19:18]
#define CSK_SPI_BIT_ORDER_UNSET         (0UL << CSK_SPI_BIT_ORDER_Pos)      ///< SPI Bit order is kept unchanged or default
#define CSK_SPI_MSB_LSB                 (1UL << CSK_SPI_BIT_ORDER_Pos)      ///< SPI Bit order from MSB to LSB (default)
#define CSK_SPI_LSB_MSB                 (2UL << CSK_SPI_BIT_ORDER_Pos)      ///< SPI Bit order from LSB to MSB

/*----- SPI Control Codes: Exclusive Controls -----*/
/*----- exclusive operations, CANNOT coexist with other Control Codes -----*/
#define CSK_SPI_EXCL_OP_Pos             20
#define CSK_SPI_EXCL_OP_Msk             (0xFUL << CSK_SPI_EXCL_OP_Pos)      // bit[23:20]
#define CSK_SPI_EXCL_OP_UNSET           (0UL << CSK_SPI_EXCL_OP_Pos)        ///< NO exclusive operations
#define CSK_SPI_SET_BUS_SPEED           (1UL << CSK_SPI_EXCL_OP_Pos)        ///< Set Bus Speed in bps; arg = value
#define CSK_SPI_GET_BUS_SPEED           (2UL << CSK_SPI_EXCL_OP_Pos)        ///< Get Bus Speed in bps
#define CSK_SPI_ABORT_TRANSFER          (3UL << CSK_SPI_EXCL_OP_Pos)        ///< Abort current data transfer, arg:
                                                                            // 1 = remain state; 0 = clean state
/*----- SPI Control Codes: Miscellaneous Controls -----*/


/****** SPI specific error codes *****/
#define CSK_SPI_ERROR_MODE              (CSK_DRIVER_ERROR_SPECIFIC - 1)     ///< Specified Mode not supported
#define CSK_SPI_ERROR_FRAME_FORMAT      (CSK_DRIVER_ERROR_SPECIFIC - 2)     ///< Specified Frame Format not supported
#define CSK_SPI_ERROR_DATA_BITS         (CSK_DRIVER_ERROR_SPECIFIC - 3)     ///< Specified number of Data bits not supported
#define CSK_SPI_ERROR_BIT_ORDER         (CSK_DRIVER_ERROR_SPECIFIC - 4)     ///< Specified Bit order not supported

typedef enum _emIOMode {
   NO_IO = 0,
   DMA_IO = 1,
   PIO_IO = 2
} emIOMode;

/**
 \brief SPI Status
 */
typedef struct _CSK_SPI_STATUS_BIT
{
    uint32_t busy :1;       ///< Transmitter/Receiver busy flag
    //uint32_t data_lost :1;  ///< Data lost: Receive overflow / Transmit underflow (cleared on start of transfer operation)
    uint32_t data_ovf :1;  ///< Data Overflow: receiver overflow (cleared on start of transfer operation)
    uint32_t data_unf :1;  ///< Data Underflow: transmit underflow (cleared on start of transfer operation)
    uint32_t rsvd1 :1;
    uint32_t tx_mode :2;   ///< Current TX mode: 0 = NO data TX, 1 = DMA, 2 = PIO
    uint32_t rx_mode :2;   ///< Current RX mode: 0 = NO data RX, 1 = DMA, 2 = PIO
    //TODO: add other status flags?
} CSK_SPI_STATUS_BIT;

// SPI status
typedef union {
    uint32_t all;
    CSK_SPI_STATUS_BIT bit;
} CSK_SPI_STATUS;

//------------------------------------------------------------------------------------------
///****** SPI Event *****/
#define CSK_SPI_EVENT_TRANSFER_COMPLETE (1UL << 0)  ///< Data Transfer completed
#define CSK_SPI_EVENT_DATA_LOST         (1UL << 1)  ///< Data lost: Receive overflow / Transmit underflow
#define CSK_SPI_EVENT_SLV_CMD_R         (1UL << 3)  ///< Slave mode, receive read command
#define CSK_SPI_EVENT_SLV_CMD_W         (1UL << 4)  ///< Slave mode, receive write command
#define CSK_SPI_EVENT_SLV_CMD_S         (1UL << 5)  ///< Slave mode, receive read status command


/**
 \fn          void CSK_SPI_SignalEvent_t (uint32_t event, uint32_t usr_param)
 \brief       Signal SPI Events.
 \param[in]   event        SPI event notification mask
 \param[in]   usr_param    user parameter
 \return      none
*/
typedef void
(*CSK_SPI_SignalEvent_t)(uint32_t event, uint32_t usr_param);

//------------------------------------------------------------------------------------------
/**
 \fn          CSK_DRIVER_VERSION SPI_GetVersion (void)
 \brief       Get driver version.
 \return      \ref CSK_DRIVER_VERSION
*/
CSK_DRIVER_VERSION
SPI_GetVersion();

/**
 \fn          int32_t SPI_Initialize (void *spi_dev, CSK_SPI_SignalEvent_t cb_event, uint32_t usr_param)
 \brief       Initialize SPI Interface.
 \param[in]   spi_dev  Pointer to SPI device instance
 \param[in]   cb_event  Pointer to \ref CSK_SPI_SignalEvent_t
 \param[in]   usr_param  User-defined value, acts as last parameter of cb_event
 \return      \ref execution_status
*/
int32_t
SPI_Initialize(void *spi_dev, CSK_SPI_SignalEvent_t cb_event, uint32_t usr_param);

/**
 \fn          int32_t SPI_Uninitialize (void)
 \brief       De-initialize SPI Interface.
 \param[in]   spi_dev  Pointer to SPI device instance
 \return      \ref execution_status
*/
int32_t
SPI_Uninitialize(void *spi_dev);

/**
 \fn          int32_t SPI_PowerControl (void *spi_dev, CSK_POWER_STATE state)
 \brief       Control SPI Interface Power.
 \param[in]   spi_dev  Pointer to SPI device instance
 \param[in]   state  Power state
 \return      \ref execution_status
*/
int32_t
SPI_PowerControl(void *spi_dev, CSK_POWER_STATE state);

/**
 \fn          int32_t SPI_Send (void *spi_dev, const void *data, uint32_t num)
 \brief       Start sending data to SPI transmitter.
 \param[in]   spi_dev  Pointer to SPI device instance
 \param[in]   data  Pointer to buffer with data to send to SPI transmitter
 \param[in]   num   Number of data items to send
 \return      \ref execution_status
*/
int32_t
SPI_Send(void *spi_dev, const void *data, uint32_t num);

/**
 \fn          int32_t SPI_Receive (void *spi_dev, void *data, uint32_t num)
 \brief       Start receiving data from SPI receiver.
 \param[in]   spi_dev  Pointer to SPI device instance
 \param[out]  data  Pointer to buffer for data to receive from SPI receiver
 \param[in]   num   Number of data items to receive
 \return      \ref execution_status
*/
int32_t
SPI_Receive(void *spi_dev, void *data, uint32_t num);

/**
 \fn          int32_t SPI_Transfer (void *spi_dev, const void *data_out, void *data_in, uint32_t num)
 \brief       Start sending/receiving data to/from SPI transmitter/receiver.
 \param[in]   spi_dev  Pointer to SPI device instance
 \param[in]   data_out  Pointer to buffer with data to send to SPI transmitter
 \param[out]  data_in   Pointer to buffer for data to receive from SPI receiver
 \param[in]   num       Number of data items to transfer
 \return      \ref execution_status
*/
int32_t
SPI_Transfer(void *spi_dev, const void *data_out, void *data_in, uint32_t num);

/**
 \fn          uint32_t SPI_GetDataCount (void *spi_dev)
 \brief       Get transferred data count.
 \param[in]   spi_dev  Pointer to SPI device instance
 \return      number of data items transferred
*/
uint32_t
SPI_GetDataCount(void *spi_dev);

/**
 \fn          int32_t SPI_Control (void *spi_dev, uint32_t control, uint32_t arg)
 \brief       Control SPI Interface.
 \param[in]   spi_dev  Pointer to SPI device instance
 \param[in]   control  Operation
 \param[in]   arg      Argument of operation (optional)
 \return      common \ref execution_status and driver specific \ref spi_execution_status
*/
int32_t
SPI_Control(void *spi_dev, uint32_t control, uint32_t arg);

/**
 \fn          CSK_SPI_STATUS SPI_GetStatus (void *spi_dev)
 \brief       Get SPI status.
 \param[in]   spi_dev  Pointer to SPI device instance
 \param[out]  status  Pointer to CSK_SPI_STATUS buffer
 \return      \ref execution_status
 */
int32_t
SPI_GetStatus(void *spi_dev, CSK_SPI_STATUS *status);


//------------------------------------------------------------------------------------------
/**
 \fn          void* SPI0()
 \brief       Get SPI0 device instance
 \return      SPI0 device instance
 */
void* SPI0();

/**
 \fn          void* SPI1()
 \brief       Get SPI1 device instance
 \return      SPI1 device instance
 */
void* SPI1();

///**
// \fn          void* SPI2()
// \brief       Get SPI2 device instance
// \return      SPI2 device instance
// */
//void* SPI2();

//
//NOTES:
// for SPI TX/RX IO on platform CP,
// only PIO is supported on SPI0, and both DMA and PIO are supported on SPI1!
//

#endif /* __DRIVER_SPI_H */
