# SPDX-License-Identifier: Apache-2.0

import random

import pytest

from vaccel import Arg, ArgType, OpType, Session


@pytest.fixture
def test_lib(vaccel_paths) -> bytes:
    return {
        "path": vaccel_paths["lib"] / "libmytestlib.so",
        "symbol": "mytestfunc",
    }


@pytest.fixture
def test_args() -> bytes:
    return {
        "read": [[random.randint(1, 100) for _ in range(10)]],
        "write": [[0] * 10],
    }


@pytest.fixture
def test_data():
    m = n = k = 12
    return {
        "m": m,
        "n": n,
        "k": k,
        "alpha": 32412.000000,
        "a": [float(1)] * m * k,
        "lda": k,
        "b": [float(2)] * m * k,
        "ldb": n,
        "beta": 2123.000000,
        "ldc": n,
    }


def test_exec(test_lib, test_args):
    g_arg_read = [
        Arg(OpType.EXEC, ArgType.UINT8),
        Arg(test_lib["path"], ArgType.STRING),
        Arg(test_lib["symbol"], ArgType.STRING),
    ]
    g_arg_read += [Arg(arg) for arg in test_args["read"]]
    g_arg_write = [Arg(arg) for arg in test_args["write"]]

    session = Session()
    session.genop(g_arg_read, g_arg_write)

    arg_write = [g_arg_write[i].buf for i in range(len(g_arg_write))]
    assert arg_write == test_args["read"]


def test_sgemm(test_data):
    arg_read = [
        Arg(OpType.BLAS_SGEMM, ArgType.UINT8),
        Arg(test_data["m"], ArgType.INT64),
        Arg(test_data["n"], ArgType.INT64),
        Arg(test_data["k"], ArgType.INT64),
        Arg(test_data["alpha"], ArgType.FLOAT32),
        Arg(test_data["a"], ArgType.FLOAT32_ARRAY),
        Arg(test_data["lda"], ArgType.INT64),
        Arg(test_data["b"], ArgType.FLOAT32_ARRAY),
        Arg(test_data["ldb"], ArgType.INT64),
        Arg(test_data["beta"], ArgType.FLOAT32),
        Arg(test_data["ldc"], ArgType.INT64),
    ]
    c = [float(0)] * test_data["m"] * test_data["n"]
    arg_write = [Arg(c, ArgType.FLOAT32_ARRAY)]

    session = Session()
    session.genop(arg_read, arg_write)
