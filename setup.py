from setuptools import setup, find_packages
from platform import uname
from datestamp import stamp
from cmake_build_extension import BuildExtension, CMakeExtension

package = 'vaccel'
platform = uname()

if platform.system != 'Linux':
    _ = f'"(package.title())" only supported to run on Linux'
    raise RuntimeError(_)

setup(name = 'vaccel',
        url = 'https://github.com/nubificus/python-vaccel',
        author = 'Nubificus Ltd.',
        version = stamp(package),
        packages = find_packages(),
        description = ('Python bindings with CFFI for libvaccel'),
        install_requires = ["cffi>=1.0.0"],
        cffi_modules = ["builder.py:ffibuilder"],
)
