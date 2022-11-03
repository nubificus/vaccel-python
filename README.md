# python bindings for vaccel

This repo defines and builds the vaccel bindings for python. It is WiP and only
defines a subset of the vAccel API.


### building

To build, first clone the repo and its submodules:

```bash
git clone https://github.com/nubificus/python-vaccel --recursive
```

#### vAccelRT

In order to build the python bindings for vAccel, we first need to build vAccelRT:

```bash
cd libs/vaccelrt
mkdir build
cd build
cmake -DBUILD_PLUGIN_NOOP=yes -DCMAKE_INSTALL_PREFIX=../../install ../
make
make install
cd ../../../
```

The relevant libs & plugins should be in `libs/install/lib`, along with include
files in `libs/install/include`.

#### helper lib

Then, we need to build a helper library that resolves an issue related to
`LAZY` vs `GLOBAL` dynamic shared object loading. So, at the top level
directory of this repo, run:

```bash
make
```

to build `libvaccel-python.so` and place it in `libs/install/lib`.

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
PYTHON_VACCEL_PLUGIN=./libs/vaccelrt/build/plugins/noop/libvaccel-noop.so LD_LIBRARY_PATH=./libs/install/lib PYTHONPATH=$PYTHONPATH:. python3 vaccel/test.py
```


## Test

To run the tests:

```bash
# Run tests
PYTHON_VACCEL_PLUGIN=./libs/vaccelrt/build/plugins/noop/libvaccel-noop.so LD_LIBRARY_PATH=./libs/install/lib PYTHONPATH=$PYTHONPATH:. pytest

# Test coverage
PYTHON_VACCEL_PLUGIN=./libs/vaccelrt/build/plugins/noop/libvaccel-noop.so LD_LIBRARY_PATH=./libs/install/lib PYTHONPATH=$PYTHONPATH:. pytest --cov=vaccel tests/
```
