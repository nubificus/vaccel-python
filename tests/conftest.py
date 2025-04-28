# SPDX-License-Identifier: Apache-2.0

import importlib.util
import os
from pathlib import Path

import pkgconfig
import pytest

from build_ffi import compile_ffi


def pytest_configure():
    # Build ffi lib if package is not installed
    if importlib.util.find_spec("vaccel") is None:
        ffi_lib = Path("vaccel/_libvaccel.abi3.so")
        if not ffi_lib.is_file():
            compile_ffi()

    # Set environment variables for all tests
    os.environ["VACCEL_PLUGINS"] = "libvaccel-noop.so"
    os.environ["VACCEL_LOG_LEVEL"] = "4"


@pytest.fixture(scope="session")
def vaccel_paths():
    variables = pkgconfig.variables("vaccel")
    return {
        "prefix": Path(variables["prefix"]),
        "lib": Path(variables["libdir"]),
        "images": Path(variables["prefix"]) / "share" / "vaccel" / "images",
        "models": Path(variables["prefix"]) / "share" / "vaccel" / "models",
        "input": Path(variables["prefix"]) / "share" / "vaccel" / "input",
    }
