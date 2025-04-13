#!/bin/bash

source /venv/.env/bin/activate

python builder.py
export VACCEL_PLUGINS=libvaccel-noop.so 
export PYTHONPATH=$PYTHONPATH:.
python setup.py install
rm -fr ./dist ./build ./.eggs ./vaccel_python.egg*

lazydocs vaccel --overview-file index --src-base-url https://github.com/nubificus/python-vaccel --output-path ./_docs/docs
