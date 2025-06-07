# SPDX-License-Identifier: Apache-2.0

import numpy as np
import pytest

from vaccel import Resource, ResourceType, Session
from vaccel.ops.torch import Buffer, Tensor, TensorType


@pytest.fixture(scope="module")
def test_model(vaccel_paths) -> bytes:
    return vaccel_paths["models"] / "torch" / "cnn_trace.pt"


@pytest.fixture(scope="module")
def test_tensor() -> dict:
    data = [1.0] * 30
    return {
        "dims": [1, 30],
        "data": data,
        "type": TensorType.FLOAT,
        "data_bytes": np.array(data, dtype=np.float32).tobytes(),
    }


def test_tensor_plain(test_tensor):
    tensor = Tensor(
        test_tensor["dims"], test_tensor["type"], test_tensor["data"]
    )
    assert tensor.dims == test_tensor["dims"]
    assert tensor.data_type == test_tensor["type"]
    assert tensor.data == test_tensor["data"]
    assert tensor.as_bytelike() == test_tensor["data_bytes"]
    assert tensor.as_memoryview() == test_tensor["data_bytes"]
    assert tensor.to_bytes() == test_tensor["data_bytes"]


def test_tensor_from_buffer(test_tensor):
    tensor = Tensor.from_buffer(
        test_tensor["dims"], test_tensor["type"], test_tensor["data_bytes"]
    )
    assert tensor.dims == test_tensor["dims"]
    assert tensor.data_type == test_tensor["type"]
    assert tensor.data == test_tensor["data"]
    assert tensor.as_bytelike() == test_tensor["data_bytes"]
    assert tensor.as_memoryview() == test_tensor["data_bytes"]
    assert tensor.to_bytes() == test_tensor["data_bytes"]


def test_torch(test_tensor, test_model):
    session = Session()

    model = Resource(test_model, ResourceType.MODEL)
    model.register(session)

    in_tensors = [
        Tensor(test_tensor["dims"], test_tensor["type"], test_tensor["data"])
    ]

    out_tensors = session.torch_jitload_forward(model, in_tensors)
    assert out_tensors[0].dims == in_tensors[0].dims
    assert out_tensors[0].data_type == in_tensors[0].data_type
    assert out_tensors[0].data == in_tensors[0].data
    assert out_tensors[0].as_bytelike() == in_tensors[0].as_bytelike()


def test_torch_from_buffer(test_tensor, test_model):
    session = Session()

    model = Resource(test_model, ResourceType.MODEL)
    model.register(session)

    in_tensors = [
        Tensor.from_buffer(
            test_tensor["dims"], test_tensor["type"], test_tensor["data_bytes"]
        )
    ]

    out_tensors = session.torch_jitload_forward(model, in_tensors)
    assert out_tensors[0].dims == in_tensors[0].dims
    assert out_tensors[0].data_type == in_tensors[0].data_type
    assert out_tensors[0].data == in_tensors[0].data
    assert out_tensors[0].as_bytelike() == in_tensors[0].as_bytelike()


def test_torch_with_run_options(test_tensor, test_model):
    session = Session()

    model = Resource(test_model, ResourceType.MODEL)
    model.register(session)

    in_tensors = [
        Tensor(test_tensor["dims"], test_tensor["type"], test_tensor["data"])
    ]

    run_options = Buffer(b"none")

    out_tensors = session.torch_jitload_forward(
        model, in_tensors, run_options=run_options
    )
    assert out_tensors[0].dims == in_tensors[0].dims
    assert out_tensors[0].data_type == in_tensors[0].data_type
    assert out_tensors[0].data == in_tensors[0].data
    assert out_tensors[0].as_bytelike() == in_tensors[0].as_bytelike()
