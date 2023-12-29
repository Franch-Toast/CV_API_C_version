/** @file */

// xos_types.h - XOS type definitions.

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

// NOTE: Do not include this file directly in your application. Including
// xos.h will automatically include this file.


#ifndef XOS_TYPES_H
#define XOS_TYPES_H

#if !defined(_ASMLANGUAGE) && !defined(__ASSEMBLER__)

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>

//-----------------------------------------------------------------------------
// The following are defined here because of the variations in the C libraries
// that we need to work with.
//    - Not all of them have stdbool.h
//    - Not all of them define NULL as (void *)0
//-----------------------------------------------------------------------------


//-----------------------------------------------------------------------------
///
/// XOS define for NULL value. This makes the NULL value independent of the
/// C library (not all of them define NULL the same way).
///
//-----------------------------------------------------------------------------
#if (defined __cplusplus) && (__cplusplus == 201103L)
#define XOS_NULL    nullptr
#elif (defined __cplusplus)
#define XOS_NULL    (0)
#else
#define XOS_NULL    ((void *)0)
#endif


//-----------------------------------------------------------------------------
///
/// XOS definition of 'bool' type. Some C libraries do not support stdbool.h.
///
//-----------------------------------------------------------------------------
#ifndef __cplusplus

#ifndef bool
// parasoft-begin-suppress MISRA2012-RULE-21_1_c-2 "Required here."
#define bool        _Bool
#define false       0        ///< XOS definition of 'false'
#define true        1        ///< XOS definition of 'true'
// parasoft-end-suppress MISRA2012-RULE-21_1_c-2 "Required here".
#endif

#endif

#ifdef __cplusplus
}
#endif

#else  // Assembly

// Redefine stdint.h macros for assembler.
// parasoft-begin-suppress MISRA2012-RULE-20_7   "Cannot parenthesize assembly macro args."
// parasoft-begin-suppress MISRA2012-RULE-21_1_c "Necessary to redefine these to enable assembly code to compile."
#define INT8_C(x)       x
#define UINT8_C(x)      x
#define INT16_C(x)      x
#define UINT16_C(x)     x
#define INT32_C(x)      x
#define UINT32_C(x)     x
#define INT64_C(x)      x
#define UINT64_C(x)     x
// parasoft-end-suppress MISRA2012-RULE-20_7   "Cannot parenthesize assembly macro args."
// parasoft-end-suppress MISRA2012-RULE-21_1_c "Necessary to redefine these to enable assembly code to compile."

#endif // !defined(_ASMLANGUAGE) && !defined(__ASSEMBLER__)

#endif // XOS_TYPES_H

