#!/bin/bash -xe

g++ -DULAPI -I${HEADERS} -std=c++0x -I${HEADERS} \
    -DSIM -rdynamic -L${LIBDIR} \
    -o test_rtapi_vsnprintf test_rtapi_vsnprintf.c
./test_rtapi_vsnprintf
