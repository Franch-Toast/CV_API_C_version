/** @file */

// xos_params.h - user-settable compile time parameters for XOS.

// Copyright (c) 2015-2020 Cadence Design Systems, Inc.
//
// Permission is hereby granted, free of charge, to any person obtaining
// a copy of this software and associated documentation files (the
// "Software"), to deal in the Software without restriction, including
// without limitation the rights to use, copy, modify, merge, publish,
// distribute, sublicense, and/or sell copies of the Software, and to
// permit persons to whom the Software is furnished to do so, subject to
// the following conditions:
//
// The above copyright notice and this permission notice shall be included
// in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
// IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
// CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
// TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
// SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


#ifndef XOS_PARAMS_H
#define XOS_PARAMS_H

#include <xtensa/config/core.h>

#include "xos_types.h"

#ifdef __cplusplus
extern "C" {
#endif


//-----------------------------------------------------------------------------
///
/// Number of thread priority levels. At this time XOS supports a maximum of
/// 32 priority levels (0 - 31).
///
//-----------------------------------------------------------------------------
#ifndef XOS_NUM_PRIORITY
#define XOS_NUM_PRIORITY                16       // Default is 16
#endif


//-----------------------------------------------------------------------------
///
/// Debug flags - Set to 1 to enable debug mode (and more verbose operation).
/// Can be set individually, or define XOS_DEBUG_ALL=1 to enable all of them.
///
/// - XOS_DEBUG           -- Generic OS debug
/// - XOS_COND_DEBUG      -- Condition objects debug
/// - XOS_EVENT_DEBUG     -- Event objects debug
/// - XOS_MSGQ_DEBUG      -- Message queue debug
/// - XOS_MUTEX_DEBUG     -- Mutex objects debug
/// - XOS_SEM_DEBUG       -- Semaphore objects debug
/// - XOS_THREAD_DEBUG    -- Thread module debug
/// - XOS_TIMER_DEBUG     -- Timer module debug
/// - XOS_DEBUG_VERBOSE   -- Enable verbose debug prints. This is NOT enabled
///                          by XOS_DEBUG_ALL. Turning this on generates lots
///                          of debug output and also drastically changes the
///                          system's timing.
///
/// WARNING: Enabling one or more of these flags will affect system performance
/// and timing.
///
/// NOTE: Not all of these have been fully implemented.
///
//-----------------------------------------------------------------------------
#ifndef XOS_DEBUG_VERBOSE
#define XOS_DEBUG_VERBOSE               UINT32_C(0)
#endif

#ifndef XOS_DEBUG_ALL
#define XOS_DEBUG_ALL                   UINT32_C(0)
#endif

#if XOS_DEBUG_ALL

#define XOS_DEBUG                       UINT32_C(1)
#define XOS_THREAD_DEBUG                UINT32_C(1)
#define XOS_TIMER_DEBUG                 UINT32_C(1)
#define XOS_COND_DEBUG                  UINT32_C(1)
#define XOS_MUTEX_DEBUG                 UINT32_C(1)
#define XOS_SEM_DEBUG                   UINT32_C(1)
#define XOS_EVENT_DEBUG                 UINT32_C(1)
#define XOS_MSGQ_DEBUG                  UINT32_C(1)

#else

#ifndef XOS_DEBUG
#define XOS_DEBUG                       UINT32_C(0)
#endif
#ifndef XOS_THREAD_DEBUG
#define XOS_THREAD_DEBUG                UINT32_C(0)
#endif
#ifndef XOS_TIMER_DEBUG
#define XOS_TIMER_DEBUG                 UINT32_C(0)
#endif
#ifndef XOS_COND_DEBUG
#define XOS_COND_DEBUG                  UINT32_C(0)
#endif
#ifndef XOS_MUTEX_DEBUG
#define XOS_MUTEX_DEBUG                 UINT32_C(0)
#endif
#ifndef XOS_SEM_DEBUG
#define XOS_SEM_DEBUG                   UINT32_C(0)
#endif
#ifndef XOS_EVENT_DEBUG
#define XOS_EVENT_DEBUG                 UINT32_C(0)
#endif
#ifndef XOS_MSGQ_DEBUG
#define XOS_MSGQ_DEBUG                  UINT32_C(0)
#endif

#endif


//-----------------------------------------------------------------------------
///
/// Set this option to 1 to enable runtime statistics collection for XOS.
/// NOTE: Enabling this option does have some impact on runtime performance
/// and OS footprint.
///
//-----------------------------------------------------------------------------
#ifndef XOS_OPT_STATS
#define XOS_OPT_STATS                   UINT32_C(1)
#endif


//-----------------------------------------------------------------------------
///
/// Set this option to 1 to enable statistics tracking for message queues.
/// Enabling this causes message queue objects to increase in size and adds
/// some overhead to message queue processing.
///
//-----------------------------------------------------------------------------
#ifndef XOS_OPT_MSGQ_STATS
#define XOS_OPT_MSGQ_STATS              UINT32_C(0)
#endif


//-----------------------------------------------------------------------------
///
/// Set this option to 1 to enable statistics tracking for block memory pools.
/// Enabling this causes block pool objects to increase in size and adds a
/// small overhead to alloc/free operations.
///
//-----------------------------------------------------------------------------
#ifndef XOS_OPT_BLOCKMEM_STATS
#define XOS_OPT_BLOCKMEM_STATS          UINT32_C(0)
#endif


//-----------------------------------------------------------------------------
///
/// Size of interrupt stack in bytes. Shared by all interrupt handlers. Must be
/// sized to handle worst case nested interrupts. This is also used by the idle
/// thread so must exist even if interrupts are not configured.
///
//-----------------------------------------------------------------------------
#ifndef XOS_INT_STACK_SIZE
#if XCHAL_HAVE_INTERRUPTS
#define XOS_INT_STACK_SIZE              UINT32_C(8192)
#else
#define XOS_INT_STACK_SIZE              UINT32_C(32)
#endif
#endif


//-----------------------------------------------------------------------------
///
/// Default maximum interrupt level at which XOS primitives may be called.
/// It is the level at which interrupts are disabled by default.
/// See also description of xos_set_int_pri_level().
///
//-----------------------------------------------------------------------------
#ifndef XOS_MAX_OS_INTLEVEL
#if defined XCHAL_EXCM_LEVEL
#define XOS_MAX_OS_INTLEVEL             XCHAL_EXCM_LEVEL
#else
#define XOS_MAX_OS_INTLEVEL             XCHAL_NUM_INTLEVELS
#endif
#endif


//-----------------------------------------------------------------------------
///
/// Set this to 1 to enable stack checking. The stack is filled with a pattern
/// on thread creation, and the stack is checked at certain times during system
/// operation.
/// WARNING: Enabling this option can have some impact on runtime performance.
///
//-----------------------------------------------------------------------------
#ifndef XOS_OPT_STACK_CHECK
#if XOS_DEBUG
#define XOS_OPT_STACK_CHECK             UINT32_C(1)
#else
#define XOS_OPT_STACK_CHECK             UINT32_C(0)
#endif
#endif


//-----------------------------------------------------------------------------
///
/// Set XOS_CLOCK_FREQ to the system clock frequency if this is known ahead of
/// time. Otherwise, call xos_set_clock_freq() to set it at run time.
///
//-----------------------------------------------------------------------------
#ifndef XOS_CLOCK_FREQ
#define XOS_CLOCK_FREQ                  UINT32_C(1000000)
#endif
#define XOS_DEFAULT_CLOCK_FREQ          XOS_CLOCK_FREQ


//-----------------------------------------------------------------------------
///
/// Set this option to 1 to enable software prioritization of interrupts. The
/// priority scheme applied is that a higher interrupt number at the same level
/// will have higher priority.
///
//-----------------------------------------------------------------------------
#ifndef XOS_OPT_INTERRUPT_SWPRI
#define XOS_OPT_INTERRUPT_SWPRI         UINT32_C(0)
#endif


//-----------------------------------------------------------------------------
///
/// Set this option to 1 to use the thread-safe version of the C runtime library.
/// You may need to enable this if you call C library functions from multiple
/// threads -- see the documentation for the relevant C library to determine if
/// this is necessary. This option increases the size of the TCB.
/// NOTE: At this time only the newlib and xclib libraries are supported for
/// thread safety.
///
//-----------------------------------------------------------------------------
#include <xtensa/config/system.h>

#ifndef XOS_OPT_THREAD_SAFE_CLIB

#if XSHAL_CLIB == XTHAL_CLIB_XCLIB
#define XOS_OPT_THREAD_SAFE_CLIB        UINT32_C(1)
#elif XSHAL_CLIB == XTHAL_CLIB_NEWLIB
#define XOS_OPT_THREAD_SAFE_CLIB        UINT32_C(1)
#else
#define XOS_OPT_THREAD_SAFE_CLIB        UINT32_C(0)
#endif

#endif


//-----------------------------------------------------------------------------
///
/// Set this option to 1 to enable the wait timeout feature. This allows waits
/// on waitable objects to expire after a specified timeout.
///
//-----------------------------------------------------------------------------
#ifndef XOS_OPT_WAIT_TIMEOUT
#define XOS_OPT_WAIT_TIMEOUT            UINT32_C(1)
#endif


//-----------------------------------------------------------------------------
///
/// Set this option to 1 to enable threads waiting on timer objects. If this
/// feature is not used, turning it off will make timer objects smaller, and
/// reduce the time taken by timer expiry processing (by a small amount).
///
//-----------------------------------------------------------------------------
#ifndef XOS_OPT_TIMER_WAIT
#define XOS_OPT_TIMER_WAIT              UINT32_C(1)
#endif


//-----------------------------------------------------------------------------
///
/// Set this option to 1 to enable timer event processing in a separate thread
/// instead of in the timer interrupt handler. Processing in a thread allows
/// the interrupt handler to finish faster and allows potentially blocking OS
/// calls, but does require more memory for the timer thread TCB and stack.
///
//-----------------------------------------------------------------------------
#ifndef XOS_OPT_TIMER_THREAD
#define XOS_OPT_TIMER_THREAD            UINT32_C(0)
#endif


//-----------------------------------------------------------------------------
///
/// Use this option to specify the stack size in bytes for the timer thread.
/// Make sure the size is large enough to handle user-supplied timer callbacks.
/// This value is ignored if XOS_OPT_TIMER_THREAD is zero.
///
//-----------------------------------------------------------------------------
#ifndef XOS_TIMER_THREAD_STACK_SIZE
#define XOS_TIMER_THREAD_STACK_SIZE     (XOS_STACK_MIN_SIZE_NO_CP + 0x100)
#endif


//-----------------------------------------------------------------------------
///
/// Set this option to 1 to enable time-slicing between multiple threads at
/// the same priority. If this option is enabled then after every slice period
/// the timer handler will switch out the current thread if there is another
/// ready thread at the same priority, and allow the latter thread to run.
/// Execution will be round robin switched among all threads at the same
/// priority.
///
/// The time slice interval is a multiple of the timer tick period, and is
/// determined by the value of XOS_TIME_SLICE_TICKS.
///
/// This feature is most useful if fixed duration timer ticks are used.
/// If dynamic ticking is enabled, then time slicing will work unpredictably
/// because the interval between ticks will vary. In such cases it may be
/// better to turn time slicing off.
///
//-----------------------------------------------------------------------------
#ifndef XOS_OPT_TIME_SLICE
#define XOS_OPT_TIME_SLICE              UINT32_C(1)
#endif


//-----------------------------------------------------------------------------
///
/// Number of timer ticks per time slice interval. This setting is used only if
/// the option XOS_OPT_TIME_SLICE is enabled. Setting this to a higher number
/// will increase the time slice interval. The valid range for this setting is
/// 1 to 50. Specifying a number outside the range will cause it to be capped
/// within the range limit.
///
//-----------------------------------------------------------------------------
#ifndef XOS_TIME_SLICE_TICKS
#define XOS_TIME_SLICE_TICKS            UINT32_C(1)
#endif


//-----------------------------------------------------------------------------
///
/// Set this option to 1 to enable debugging of block memory pool operations.
/// This option will enable additional checks during alloc/free, and will also
/// enable the internal consistency check via xos_block_pool_check().
///
/// Enabling this option will add a small overhead to alloc/free operations.
///
//-----------------------------------------------------------------------------
#ifndef XOS_BLOCKMEM_DEBUG
#define XOS_BLOCKMEM_DEBUG              UINT32_C(0)
#endif


//-----------------------------------------------------------------------------
///
/// Set this option to 1 to enable priority inversion protection for mutexes.
/// This option must be enabled to use mutex priority inheritance and priority
/// protection. 
///
/// Enabling this option will add to both code and data size and runtime.
///
//-----------------------------------------------------------------------------
#ifndef XOS_OPT_MUTEX_PRIORITY
#define XOS_OPT_MUTEX_PRIORITY          UINT32_C(1)
#endif


//-----------------------------------------------------------------------------
///
/// Setting this option to 1 causes all interrupts to go to a wrapper function
/// which then dispatches them to the appropriate handlers.
/// NOTE: This is an experimental feature.
///
//-----------------------------------------------------------------------------
#define XOS_USE_INT_WRAPPER             UINT32_C(0)


//-----------------------------------------------------------------------------
///
/// Setting this option to 1 enables system event logging. The event log must
/// be configured and enabled for event logging to work. If the event log is
/// not enabled, this option will do nothing.
///
//-----------------------------------------------------------------------------
#ifndef XOS_OPT_LOG_SYSEVENT
#define XOS_OPT_LOG_SYSEVENT            UINT32_C(0)
#endif


//-----------------------------------------------------------------------------
///
/// Setting this option to 1 enables the use of C11 atomics. Enabling this will
/// require compiling to the C11 standard (-std=c11 compiler option). Note that
/// C11 atomics are supported only by the Xtensa C Library (xclib).
///
//-----------------------------------------------------------------------------
#ifndef XOS_OPT_C11_ATOMICS
#define XOS_OPT_C11_ATOMICS             0
#endif


//-----------------------------------------------------------------------------
///
/// Setting this option to 1 enables thread local storage similar to pthreads
/// thread-specific keys. If this option is enabled, the number of keys is
/// specified by XOS_TLS_NUM_KEYS. The thread-specific values are stored in
/// the TCB, so specifying a larger value for XOS_TLS_NUM_KEYS could increase
/// the size of the TCB by a considerable amount.
///
//-----------------------------------------------------------------------------
#ifndef XOS_OPT_THREAD_LOCAL_STORAGE
#define XOS_OPT_THREAD_LOCAL_STORAGE    1
#endif

#ifndef XOS_TLS_NUM_KEYS
#define XOS_TLS_NUM_KEYS                4
#endif


#ifdef __cplusplus
}
#endif

#endif  // XOS_PARAMS_H

