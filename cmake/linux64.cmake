set (LINUX64 ON)
include_directories(${PROJECT_SOURCE_DIR}/deps/linux64/include/)
link_directories(${PROJECT_SOURCE_DIR}/deps/linux64/1ib/)
set (CMAKE_CXX_COMPILER "g++")
set (CMAKE_C_FLAG5 "-Dlinux -Wall -Wno-unused-function -ldl -pthread -lm -fPIC -g -msse -msse4.2 -std=c99 -wl,-rpath=./:../lib")
set (CMAKE_C_FLAGS_DEBUG "-O0 -g")
set (CMAKE_C_FLAGS_RELEASE "-O2 -s")
set (CMAKE_CXX_FLAGS "-Dlinux -std=c++11 -ldl -pthread -lm -fpermissive -Wall -Wno-unused-function -fno-stack-protector -fPIC -g -msse -msse4.2 -wl,-rpath=./: ../lib")
set (CMAKE_CXX_FLAGS_DEBUG "-O0 -g")
set (CMAKE_CXX_FLAGS_RELEASE "-O2 -s")


