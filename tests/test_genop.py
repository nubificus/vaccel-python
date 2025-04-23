import random

import pytest

from vaccel import Arg, OpType, Session


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
    arg_read = [OpType.EXEC, test_lib["path"], test_lib["symbol"]]
    arg_read.extend(test_args["read"])
    g_arg_read = [Arg(arg) for arg in arg_read]
    g_arg_write = [Arg(arg) for arg in test_args["write"]]

    session = Session()
    session.genop(g_arg_read, g_arg_write)

    arg_write = [g_arg_write[i].buf for i in range(len(g_arg_write))]
    assert arg_write == test_args["read"]


def test_sgemm(test_data):
    arg_read = [
        Arg(OpType.BLAS_SGEMM),
        Arg(test_data["m"]),
        Arg(test_data["n"]),
        Arg(test_data["k"]),
        Arg(test_data["alpha"]),
        Arg(test_data["a"]),
        Arg(test_data["lda"]),
        Arg(test_data["b"]),
        Arg(test_data["ldb"]),
        Arg(test_data["beta"]),
        Arg(test_data["ldc"]),
    ]
    c = [float(0)] * test_data["m"] * test_data["n"]
    arg_write = [Arg(c)]

    session = Session()
    session.genop(arg_read, arg_write)
