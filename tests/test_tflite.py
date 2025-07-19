# SPDX-License-Identifier: Apache-2.0

import numpy as np
import pytest

from vaccel import Resource, ResourceType, Session
from vaccel.ops.tf.lite import Tensor, TensorType


@pytest.fixture(scope="module")
def test_model(vaccel_paths) -> bytes:
    return vaccel_paths["models"] / "tf" / "lstm2.tflite"


@pytest.fixture(scope="module")
def test_tensor() -> dict:
    data = [1.0] * 30
    data_np = np.array(data, dtype=np.float32)
    return {
        "dims": [30],
        "data": data,
        "type": TensorType.FLOAT32,
        "data_np": data_np,
        "data_bytes": np.ascontiguousarray(data_np).tobytes(),
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
    assert tensor.as_numpy().all() == test_tensor["data_np"].all()


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


def test_tensor_from_numpy(test_tensor):
    tensor = Tensor.from_numpy(test_tensor["data_np"])
    assert tensor.dims == test_tensor["dims"]
    assert tensor.data_type == test_tensor["type"]
    assert tensor.data == test_tensor["data"]
    assert tensor.as_bytelike() == test_tensor["data_np"]
    assert tensor.as_memoryview() == memoryview(test_tensor["data_np"])
    assert tensor.to_bytes() == test_tensor["data_bytes"]
    assert tensor.as_numpy().all() == test_tensor["data_np"].all()


def test_tflite(test_tensor, test_model):
    session = Session()

    model = Resource(test_model, ResourceType.MODEL)
    model.register(session)

    session.tflite_model_load(model)

    in_tensors = [
        Tensor(test_tensor["dims"], test_tensor["type"], test_tensor["data"])
    ]

    (out_tensors, status) = session.tflite_model_run(model, in_tensors)
    assert status == 0
    assert out_tensors[0].dims == in_tensors[0].dims
    assert out_tensors[0].data_type == in_tensors[0].data_type
    assert out_tensors[0].data == in_tensors[0].data
    assert out_tensors[0].to_bytes() == in_tensors[0].to_bytes()

    session.tflite_model_unload(model)


def test_tflite_from_buffer(test_tensor, test_model):
    session = Session()

    model = Resource(test_model, ResourceType.MODEL)
    model.register(session)

    session.tflite_model_load(model)

    in_tensors = [
        Tensor.from_buffer(
            test_tensor["dims"], test_tensor["type"], test_tensor["data_bytes"]
        )
    ]

    (out_tensors, status) = session.tflite_model_run(model, in_tensors)
    assert status == 0
    assert out_tensors[0].dims == in_tensors[0].dims
    assert out_tensors[0].data_type == in_tensors[0].data_type
    assert out_tensors[0].data == in_tensors[0].data
    assert out_tensors[0].to_bytes() == in_tensors[0].to_bytes()

    session.tflite_model_unload(model)


def test_tflite_from_numpy(test_tensor, test_model):
    session = Session()

    model = Resource(test_model, ResourceType.MODEL)
    model.register(session)

    session.tflite_model_load(model)

    in_tensors = [Tensor.from_numpy(test_tensor["data_np"])]

    (out_tensors, status) = session.tflite_model_run(model, in_tensors)
    assert status == 0
    assert out_tensors[0].dims == in_tensors[0].dims
    assert out_tensors[0].data_type == in_tensors[0].data_type
    assert out_tensors[0].data == in_tensors[0].data
    assert out_tensors[0].to_bytes() == in_tensors[0].to_bytes()

    session.tflite_model_unload(model)
