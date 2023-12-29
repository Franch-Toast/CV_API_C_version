SET (VENUS ON)

SET (XTENSA_CORE "venus hifi4")
SET (XTENSA_RI "RI-2021.7")
SET (XT_DEVTOOLS "/yrfs4/acousticpro/yswang11/opt/xtensa/RI-2021.7-linux/XtensaTools/")
SET (XTEN5A_T0OL5 "/yrfs4/acousticpro/yswang11/opt/xtensa/RI-2021.7-1inux/XtensaTools/bin/")
SET (XTEN5A_SYSTEM "/yrfs4/acousticpro/yswang11/opt/xtensa/RI-2021.7-linux/venus_hifi4/config")



SET (CROSS_COMPILE "${XTENSA_TOOLS}/xt-")
SET (CMAKE_C_COMPILER "${CROSS_COMPILE}clang")
#SET (CMAKE_CXX COMPILER "$(CROSS COMPILEJXC++")
SET (CMAKE_AR "${CROSS_COMPILE}ar")
set (CMAKE_C_COMPILER_WORKS TRUE)


SET (VENUS_ROOT "${PROJECT_SOURCE_DIR}/deps/venus")
SET (LDSCRIPT "$(VENUS_ROOT}/1d/min-rt")
SET (INCLUDE_FLAGS "-I$VENUS ROOT/include \
-I${VENUS ROOT}/include/drive \
-I$fVENUS ROOT}/include/bsp \
-I${VENUS ROOT}/include/debug\
-I$(VENUS ROOT}/include/luna \
-I${VENUS ROOT}/include/opi_cpy")
SET (LIB_FLAGS "-I${VENUS_ROOT}/lib")

SET (CMAKE_C_FLAGS "--xtensa-system=${XTENSA_SYSTEM} --xtensa-core-${XTENSA_CORE} -I${VENUS_ROOT}/include DCSK6001 -DXOS USED -DIC BOARD=1 -DPLATFORM CP -Wa1 -Wno-format -Wno-unused -Wno-comment -MMD -ffunction-sections -fdata-sections -mcoproc -mlongcalls -mno-132r-flix -std=c11")

set (CMAKE_C_FLAGS_DEBUG "-O g")
set (CMAKE_C_FLAGS_RELEASE "-O2 -s")
set (CMAKE_C_FLAGS_RELEASE "-O2")

SET (CMAKE_EXE_LINKER_FLAGS "--xtensa-system=${XTENSA_SYSTEM} --xtensa-core=${XTENSA_CORE} -mlsp=$(VENUS_ROOT}/1d/min-rt -L${VENUS_ROOT}/lib/ -static -wl,-gc-sections")






