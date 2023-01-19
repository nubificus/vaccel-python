#!/bin/bash
source /venv/.env/bin/activate
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-deb/vaccel-0.5.0-Linux.deb
dpkg -i vaccel-0.5.0-Linux.deb
rm -fr vaccel-0.5.0-Linux.deb
python builder.py
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so 
export LD_LIBRARY_PATH=/usr/local/lib 
export PYTHONPATH=$PYTHONPATH:.
python setup.py install
rm -fr ./dist ./build ./.eggs ./vaccel_python.egg*
lazydocs vaccel --overview-file index --src-base-url https://github.com/nubificus/python-vaccel --output-path ./_docs/docs