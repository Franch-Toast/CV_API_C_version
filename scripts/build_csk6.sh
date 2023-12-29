# # export XT_DEVTOOLS=/yrfs4/acousticpro/yswang11/opt/xtensa/XtDevTools/
# export XT_DEVTOOLS=/home3/dlp/leifang3/test/RI-2021.7-linux/XtensaTools/
# export LM_LICENSE FILE=10016@172.20.64.89
# #make clean
# make al1 IC_BOARD=1 TAG=CSK6001 a11
# #make all IC _OARD=1 TAG=CSK6001 all j8

rm -rf build_venus
mkdir build_venus

build type=Release
if [ "$1" == "debug"];then
    build type=Debug
fi

cd build_venus
echo "BUILD TYPE=" $build type
cmake -DCMAKE_BULD_TYPE-$build_type -DPLATFORM_NAME=venus -DSHARED_LIB=OFF..
#make -j8
make
cd ..