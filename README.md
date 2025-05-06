# Python bindings for vAccel

[Python](https://www.python.org/) bindings for vAccel wrap the vAccel C API and
provide a native Python API to vAccel operations. The bindings are currently a
WiP, supporting a subset of the vAccel operations.

You can find more information about these bindings and everything vAccel in the
[Documentation](https://docs.vaccel.org).

## Installation

The bindings are implemented in the `vaccel` Python package. The package is
installable with `pip` by using the provided Wheels or from source.

### Requirements

- To use the `vaccel` Python package you need a valid vAccel installation. You
  can find more information on how to install vAccel in the
  [Installation](https://docs.vaccel.org/latest/getting-started/installation)
  page.

- This package requires Python 3.10 or newer. Verify your Python version with:
  ```sh
  python3 --version
  ```
  and update Python as needed using the
  [official instructions](https://docs.python.org/3/using/index.html)

### Wheel

You can get the latest `vaccel` Wheel package from the
[Releases](https://github.com/nubificus/vaccel-python/releases) page.

```sh
# Replace `x86_64` with `aarch64` or `armv7l` to get packages for the relevant
# architectures
wget https://github.com/nubificus/vaccel-python/releases/download/v0.1.0/vaccel-0.1.0-cp310-abi3-linux_x86_64.whl
pip install vaccel-0.1.0-cp310-abi3-linux_x86_64.whl
```

### Latest artifacts

To install the Wheel artifact of the latest `vaccel` revision:

```sh
# Replace `x86_64` with `aarch64` or `armv7l` to get packages for the relevant
# architectures
wget https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/x86_64/vaccel-latest-cp310-abi3-linux_x86_64.whl
pip install vaccel-latest-cp310-abi3-linux_x86_64.whl
```

### Building from source

You can build the package from source directly and install it using `pip`:

```sh
pip install git+https://github.com/nubificus/vaccel-python
```

## Running the examples

Examples of using the package are provided in the `examples` directory.

After cloning the repo:

```sh
git clone https://github.com/nubificus/vaccel-python
cd vaccel-python
```

you can run all the available examples with sample arguments using:

```sh
python3 run-examples.py
```
