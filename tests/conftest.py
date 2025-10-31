# SPDX-License-Identifier: Apache-2.0

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pkgconfig
import pytest

from build_ffi import compile_ffi

_REEXEC_MARKER = "_VACCEL_PYTEST_REEXEC_DONE"


def pytest_configure():
    # Build ffi lib if package is not installed
    if importlib.util.find_spec("vaccel") is None:
        ffi_lib = Path("vaccel/_libvaccel.abi3.so")
        if not ffi_lib.is_file():
            compile_ffi()

    # Set environment variables for all tests
    os.environ["VACCEL_PLUGINS"] = "libvaccel-noop.so"
    os.environ["VACCEL_LOG_LEVEL"] = "4"


def pytest_cmdline_main(config):
    _ = config

    # Set library path from pkgconfig
    if _REEXEC_MARKER not in os.environ:
        lib_path = os.environ.get("LD_LIBRARY_PATH", "")
        vaccel_lib_path = pkgconfig.variables("vaccel")["libdir"]

        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = (
            f"{vaccel_lib_path}:{lib_path}" if lib_path else vaccel_lib_path
        )
        env[_REEXEC_MARKER] = "1"

        sys.exit(subprocess.call([sys.executable, *sys.argv], env=env))


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
