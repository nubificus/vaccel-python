# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

import numpy as np
import pytest

from vaccel import Resource, ResourceType, Session
from vaccel._c_types import CBytes


@pytest.fixture
def test_lib(vaccel_paths) -> Path:
    return vaccel_paths["lib"] / "libmytestlib.so"


@pytest.fixture
def test_buffer() -> bytes:
    data = [1.0] * 30
    data_np = np.array(data, dtype=np.float32)
    return {
        "data": data,
        "data_np": data_np,
        "data_bytes": np.ascontiguousarray(data_np).tobytes(),
    }


def test_resource(test_lib):
    res_a = Resource(test_lib, ResourceType.LIB)
    assert res_a.id > 0
    assert res_a.remote_id == 0

    res_b = Resource([test_lib, test_lib], ResourceType.LIB)
    assert res_b.id == res_a.id + 1
    assert res_b.remote_id == 0


def test_resource_from_buffer(test_buffer):
    res = Resource.from_buffer(test_buffer["data_bytes"], ResourceType.DATA)
    res_data = res.value.blobs[0].data
    res_size = res.value.blobs[0].size
    assert res.id > 0
    assert res.remote_id == 0
    assert (
        CBytes.from_c_obj(res_data, res_size).value == test_buffer["data_bytes"]
    )


def test_resource_from_numpy(test_buffer):
    res = Resource.from_numpy(test_buffer["data_np"])
    res_data = res.value.blobs[0].data
    res_size = res.value.blobs[0].size
    assert res.id > 0
    assert res.remote_id == 0
    assert (
        CBytes.from_c_obj(res_data, res_size).value == test_buffer["data_bytes"]
    )


def test_resource_register(test_lib):
    res = Resource(test_lib, ResourceType.LIB)
    ses = Session()

    res.register(ses)
    assert ses.has_resource(res)


def test_resource_unregister(test_buffer):
    res = Resource.from_buffer(test_buffer["data_bytes"], ResourceType.DATA)
    ses = Session()

    res.register(ses)
    res.unregister(ses)
    assert not ses.has_resource(res)


def test_resource_register_unregister_multi(test_lib, test_buffer):
    res_a = Resource.from_buffer(test_buffer["data_bytes"], ResourceType.DATA)
    res_b = Resource(test_lib, ResourceType.LIB)
    ses_a = Session()
    ses_b = Session()

    res_a.register(ses_a)
    assert ses_a.has_resource(res_a)
    res_b.register(ses_a)
    assert ses_a.has_resource(res_b)

    res_a.register(ses_b)
    assert ses_b.has_resource(res_a)
    res_b.register(ses_b)
    assert ses_b.has_resource(res_b)

    res_a.sync(ses_a)
    res_a.sync(ses_b)

    res_a.unregister(ses_a)
    assert not ses_a.has_resource(res_a)
    res_b.unregister(ses_a)
    assert not ses_a.has_resource(res_b)
    res_a.unregister(ses_b)
    assert not ses_b.has_resource(res_a)
    res_b.unregister(ses_b)
    assert not ses_b.has_resource(res_b)
