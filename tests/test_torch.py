# SPDX-License-Identifier: Apache-2.0

import numpy as np
import pytest

from vaccel import Resource, ResourceType, Session
from vaccel.ops.torch import Buffer, Tensor, TensorType

try:
    import torch

    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


@pytest.fixture(scope="module")
def test_model(vaccel_paths) -> bytes:
    return vaccel_paths["models"] / "torch" / "cnn_trace.pt"


@pytest.fixture(scope="module")
def test_tensor() -> dict:
    data = [1.0] * 30
    data_np = np.array(data, dtype=np.float32)
    tensor_data = {
        "dims": [30],
        "data": data,
        "type": TensorType.FLOAT,
        "data_np": data_np,
        "data_bytes": np.ascontiguousarray(data_np).tobytes(),
    }

    if HAS_TORCH:
        tensor_data["data_torch"] = torch.from_numpy(data_np)

    return tensor_data


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
    assert tensor.as_numpy().all() == test_tensor["data_np"].all()
    if HAS_TORCH:
        assert torch.equal(tensor.as_torch(), test_tensor["data_torch"])


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
    assert tensor.as_numpy().all() == test_tensor["data_np"].all()
    if HAS_TORCH:
        assert torch.equal(tensor.as_torch(), test_tensor["data_torch"])


def test_tensor_from_numpy(test_tensor):
    tensor = Tensor.from_numpy(test_tensor["data_np"])
    assert tensor.dims == test_tensor["dims"]
    assert tensor.data_type == test_tensor["type"]
    assert tensor.data == test_tensor["data"]
    assert tensor.as_bytelike() == test_tensor["data_np"]
    assert tensor.as_memoryview() == memoryview(test_tensor["data_np"])
    assert tensor.to_bytes() == test_tensor["data_bytes"]
    assert tensor.as_numpy().all() == test_tensor["data_np"].all()
    if HAS_TORCH:
        assert torch.equal(tensor.as_torch(), test_tensor["data_torch"])


@pytest.mark.skipif(not HAS_TORCH, reason="Torch not installed")
def test_tensor_from_torch(test_tensor):
    tensor = Tensor.from_torch(test_tensor["data_torch"])
    assert tensor.dims == test_tensor["dims"]
    assert tensor.data_type == test_tensor["type"]
    assert tensor.data == test_tensor["data"]
    assert tensor.as_bytelike() == test_tensor["data_bytes"]
    assert tensor.as_memoryview() == memoryview(test_tensor["data_bytes"])
    assert tensor.to_bytes() == test_tensor["data_bytes"]
    assert tensor.as_numpy().all() == test_tensor["data_np"].all()
    assert torch.equal(tensor.as_torch(), test_tensor["data_torch"])


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
    assert out_tensors[0].to_bytes() == in_tensors[0].to_bytes()
    assert out_tensors[0].as_numpy().all() == in_tensors[0].as_numpy().all()
    if HAS_TORCH:
        assert torch.equal(out_tensors[0].as_torch(), in_tensors[0].as_torch())


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
    assert out_tensors[0].to_bytes() == in_tensors[0].to_bytes()
    assert out_tensors[0].as_numpy().all() == in_tensors[0].as_numpy().all()
    if HAS_TORCH:
        assert torch.equal(out_tensors[0].as_torch(), in_tensors[0].as_torch())


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
    assert out_tensors[0].to_bytes() == in_tensors[0].to_bytes()
    assert out_tensors[0].as_numpy().all() == in_tensors[0].as_numpy().all()
    if HAS_TORCH:
        assert torch.equal(out_tensors[0].as_torch(), in_tensors[0].as_torch())


def test_torch_from_numpy(test_tensor, test_model):
    session = Session()

    model = Resource(test_model, ResourceType.MODEL)
    model.register(session)

    in_tensors = [Tensor.from_numpy(test_tensor["data_np"])]

    out_tensors = session.torch_jitload_forward(model, in_tensors)
    assert out_tensors[0].dims == in_tensors[0].dims
    assert out_tensors[0].data_type == in_tensors[0].data_type
    assert out_tensors[0].data == in_tensors[0].data
    assert out_tensors[0].to_bytes() == in_tensors[0].to_bytes()
    assert out_tensors[0].as_numpy().all() == in_tensors[0].as_numpy().all()
    if HAS_TORCH:
        assert torch.equal(out_tensors[0].as_torch(), in_tensors[0].as_torch())


@pytest.mark.skipif(not HAS_TORCH, reason="Torch not installed")
def test_torch_from_torch(test_tensor, test_model):
    session = Session()

    model = Resource(test_model, ResourceType.MODEL)
    model.register(session)

    in_tensors = [Tensor.from_torch(test_tensor["data_torch"])]

    out_tensors = session.torch_jitload_forward(model, in_tensors)
    assert out_tensors[0].dims == in_tensors[0].dims
    assert out_tensors[0].data_type == in_tensors[0].data_type
    assert out_tensors[0].data == in_tensors[0].data
    assert out_tensors[0].to_bytes() == in_tensors[0].to_bytes()
    assert out_tensors[0].as_numpy().all() == in_tensors[0].as_numpy().all()
    assert torch.equal(out_tensors[0].as_torch(), in_tensors[0].as_torch())
