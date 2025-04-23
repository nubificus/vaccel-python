import random

import pytest

from vaccel import Resource, ResourceType, Session


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


def test_exec_genop(test_lib, test_args):
    session = Session()
    res = session.exec(
        test_lib["path"],
        test_lib["symbol"],
        test_args["read"],
        test_args["write"],
    )
    assert res == test_args["read"]


def test_exec_with_res(test_lib, test_args):
    session = Session()
    lib = Resource(test_lib["path"], ResourceType.LIB)
    lib.register(session)
    res = session.exec_with_resource(
        lib, test_lib["symbol"], test_args["read"], test_args["write"]
    )
    assert res == test_args["read"]
