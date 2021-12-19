# Makefile for vaccel python helper lib
#
CC=gcc
LD=gcc 
CFLAGS=-Wall

all: libvaccel-python.so install

libvaccel-python.so: helper.c
	@$(CC) $< -o $@ ${CFLAGS} -fPIC -shared

install: libvaccel-python.so
	@cp $< libs/install/lib

clean:
	-rm -f libvaccel-python.so libs/install/lib/libvaccel-python.so
