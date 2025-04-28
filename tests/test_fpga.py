# SPDX-License-Identifier: Apache-2.0

import pytest

from vaccel import Session


@pytest.fixture
def test_data():
    length = 10
    return {
        "len": length,
        "int": {"a": [1] * length},
        "float": {
            "a": [float(1)] * length,
            "b": [float(2)] * length,
        },
    }


def test_fpga_arraycopy(test_data):
    session = Session()
    out_a = session.fpga_arraycopy(test_data["int"]["a"])
    assert out_a == test_data["int"]["a"]


def test_fpga_mmult(test_data):
    session = Session()
    c = session.fpga_mmult(test_data["float"]["a"], test_data["float"]["b"])
    assert [round(item, 1) for item in c] == [9.1] * 10


def test_fpga_parallel(test_data):
    session = Session()
    (add_output, mult_output) = session.fpga_parallel(
        test_data["float"]["a"], test_data["float"]["b"]
    )
    assert add_output == [
        x + y
        for x, y in zip(
            test_data["float"]["a"], test_data["float"]["b"], strict=True
        )
    ]
    assert mult_output == [float(1)] * test_data["len"]


def test_fpga_vadd(test_data):
    session = Session()
    c = session.fpga_vadd(test_data["float"]["a"], test_data["float"]["b"])
    assert c == [
        x + y
        for x, y in zip(
            test_data["float"]["a"], test_data["float"]["b"], strict=True
        )
    ]
