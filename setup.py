# SPDX-License-Identifier: Apache-2.0

"""A setuptools based setup module.

This module is only necessary for building the CFFI module library.
"""

from setuptools import setup

setup(
    cffi_modules=["build_ffi.py:compile_ffi"],
)
