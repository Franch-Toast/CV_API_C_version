rm -rf build_linux
mkdir build_linux

# build type=Release
build type=debug
if [ "$1"=="debug"];then
    build type=Debug
cd build_linux
echo "BUILD TYPE=" $build_type
cmake -DCMAKE_BUILD_TYPE-$buid_type -DPLATFORM_NAME=lnux64 -DSHARED_LIB-ON ..
#make-j8
make
cd ..