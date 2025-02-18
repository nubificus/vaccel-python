# python bindings for vaccel

This repo defines and builds the vaccel bindings for python. It is WiP and only
defines a subset of the vAccel API.


### building

To build, first clone the repo:

```bash
git clone https://github.com/nubificus/python-vaccel
```

#### vAccel

In order to build the python bindings for vAccel, we first need a vAccel
installation. We can either build it from source, or get the latest binary
release:

##### Build from source

```bash
git clone https://github.com/nubificus/vaccel --recursive
cd vaccel
meson setup -Dplugin-noop=enabled build
meson compile -C build
meson install -C build

```

The relevant libs & plugins should be in `/usr/local/lib/x86_64-linux-gnu`, along with include
files in `/usr/local/include`.

##### Get the binary release:

Get the latest vAccel binaries:

```
wget https://s3.nbfc.io/nbfc-assets/github/vaccel/rev/main/x86_64/release/vaccel-latest-bin.tar.gz
```

and install it:

```
sudo tar xfv vaccel-latest-bin.tar.gz --strip-components=2 -C /usr/local
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
export VACCEL_PLUGINS=/usr/local/lib/x86_64-linux-gnu/libvaccel-noop.so 
export LD_LIBRARY_PATH=/usr/local/lib/x86_64-linux-gnu
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
export VACCEL_PLUGINS=/usr/local/lib/x86_64-linux-gnu/libvaccel-noop.so 
export LD_LIBRARY_PATH=/usr/local/lib/x86_64-linux-gnu
export PYTHONPATH=$PYTHONPATH:. 
pytest


# Test coverage
export VACCEL_PLUGINS=/usr/local/lib/x86_64-linux-gnu/libvaccel-noop.so 
export LD_LIBRARY_PATH=/usr/local/lib/x86_64-linux-gnu
export PYTHONPATH=$PYTHONPATH:. 
pytest --cov=vaccel tests/
```
