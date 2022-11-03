# python bindings for vaccel

This repo defines and builds the vaccel bindings for python. It is WiP and only
defines a subset of the vAccel API.


### building

To build, first clone the repo:

```bash
git clone https://github.com/nubificus/python-vaccel
```

#### vAccelRT

In order to build the python bindings for vAccel, we first need a vAccelRT
installation. We can either build it from source, or get the latest binary
release:

##### Build from source

```bash
mkdir -p libs
git clone https://github.com/cloudkernels/vaccelrt --recursive
cd vaccelrt
mkdir build
cd build
cmake -DBUILD_PLUGIN_NOOP=yes -DCMAKE_INSTALL_PREFIX=/usr/local ../
make
make install
cd ../../../
```

The relevant libs & plugins should be in `/usr/local/lib`, along with include
files in `/usr/local/include`.

##### Get the binary release:

We currently build vaccelrt as a `deb` package, installable in `/usr/local/`. 
Get the latest deb:

```
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-deb/vaccel-0.5.0-Linux.deb
```

and install it:

```
dpkg -i vaccel-0.5.0-Linux.deb
```

#### python bindings

Finally, call the `builder.py` to build the bindings. The required python
packages to build are: `datestamp cffi wheel setuptools cmake_build_extension`.
To install them use:

```bash
pip3 install datestamp cffi wheel setuptools cmake_build_extension
```

and run the builder:

```bash
python3 builder.py
```

The module should be ready. To test run:

```bash
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so 
export LD_LIBRARY_PATH=/usr/local/lib 
export PYTHONPATH=$PYTHONPATH:. 
python3 vaccel/test.py
```
Alternatively, you could build the pip package:

```
pip3 install build
python3 -m build
```

and install it:

```
pip install dist/vaccel*.tar.gz
```

## Test

To run the tests:

```bash
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so 
export LD_LIBRARY_PATH=/usr/local/lib 
export PYTHONPATH=$PYTHONPATH:. 
pytest


# Test coverage
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so 
export LD_LIBRARY_PATH=/usr/local/lib 
export PYTHONPATH=$PYTHONPATH:. 
pytest --cov=vaccel tests/
```
