from setuptools import setup, find_packages
from platform import uname
from datestamp import stamp

package = 'vaccel-python'
platform = uname()

setup(name=package,
      url='https://github.com/nubificus/python-vaccel',
      author='Nubificus Ltd.',
      packages=find_packages(),
      setuptools_git_versioning={ "enabled": True, },
      setup_requires=["setuptools-git-versioning<2"],
      description=('Python bindings with CFFI for libvaccel'),
      install_requires=["cffi>=1.0.0"],
      cffi_modules=["builder.py:ffibuilder"],
      )
