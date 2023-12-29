#/bin/bash
export LM_LICENSE_FILE=27000@172.20.64.45
export XTENSA_TOOLS=/yrfs4/acousticpro/yswang11/opt/xtensa/RI-2021.7-linux/XtensaTools/
export XTENSA_SYSTEM=/yrfs4/acousticpro/yswang11/opt/xtensa/RI-2021.7-linux/venus_hifi4/config
export XTENSA_CORE=venus_hifi4

echo "script:${0}, bin:${1} ..."

SCRIPT_PATH=$0
BIN_PATH=$1

SCRIPT_DIR=$(dirname $(readlink -f "$0"))
GDB_INIT="${SCRIPT_DIR}/gdb_debug.init"

# gdb
${XTENSA_TOOLS}/bin/xt-gdb --xtensa-system=${XTENSA_SYSTEM} --xtensa-core=${XTENSA_CORE} ${BIN_PATH} -x ${GDB_INIT} 