/*
 * luna.h
 *
 *  Created on: Aug 18, 2017
 *      Author: dwwang
 */

#ifndef __LUNA_LUNA_H_SIM__
#define __LUNA_LUNA_H_SIM__

#include <stdio.h>
#include <stdint.h>
#include <math.h>
#include <time.h>

#include "luna_error.h"
#include "luna_bits.h"
#include "luna_math_types.h"

#define LUNA_VER_MAJOR 3
#define LUNA_VER_MINOR 0
#define LUNA_VER_PATCH 0
#define LUNA_VER_BUILD 0
#define LUNA_VERSION   ( (LUNA_VER_MAJOR << 24) + (LUNA_VER_MINOR << 16) +  (LUNA_VER_PATCH << 8)  +  (LUNA_VER_BUILD << 0) )

#define LUNA_SHARE_MEM_AHB_BASE			(0x48000000)
#define LUNA_SHARE_MEM_AHB_BASE_MASK	(0x480FFFFF)
#define LUNA_SHARE_MEM_BASE				(0x5FE00000)
#define LUNA_PSRAM_MEM_BASE             (0x60000000)

#define _FAST_FUNC_RO           __attribute__ ((section (".sharedmem.text"))) 	//code in shared memory
#define _FAST_DATA_VI           __attribute__ ((section (".sharedmem.data"))) 	//initialized data in shared memory
#define _FAST_DATA_ZI           __attribute__ ((section (".sharedmem.bss"))) 	//zero initialized data in shared memory

#define LUNA_LOG printf

uint32_t luna_version();

void start_counter();
uint32_t get_counter();

void luna_set_check_enable(int enable);
void luna_set_sharedmem(void* addr, uint32_t size);

#endif /* __LUNA_LUNA_H_SIM__ */
