# Makefile for vaccel python helper lib
#
CC=gcc
LD=gcc 
CFLAGS=-Wall -Ilibs/install/include

all: libvaccel-python.so install

libvaccel-python.so: helper.c
	$(CC) $< -o $@ ${CFLAGS} -fPIC -shared

install: libvaccel-python.so
	cp $< libs/install/lib

clean:
	-rm -f libvaccel-python.so libs/install/lib/libvaccel-python.so

test:
	PYTHON_VACCEL_PLUGIN=./libs/vaccelrt/build/plugins/noop/libvaccel-noop.so VACCEL_DEBUG_LEVEL=4 LD_LIBRARY_PATH=./libs/install/lib PYTHONPATH=$(which python3):. python3 vaccel/test.py
