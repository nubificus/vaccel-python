# SPDX-License-Identifier: Apache-2.0

import numpy as np
import pytest

from vaccel import Resource, ResourceType, Session
from vaccel.ops.tf import Buffer, Node, Tensor, TensorType


@pytest.fixture(scope="module")
def test_model(vaccel_paths) -> bytes:
    return vaccel_paths["models"] / "tf" / "lstm2"


@pytest.fixture(scope="module")
def test_nodes() -> dict:
    return {
        "in": {
            "name": "serving_default_input_1",
            "id": 0,
        },
        "out": {
            "name": "StatefulPartitionedCall",
            "id": 0,
        },
    }


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


def test_tf(test_nodes, test_tensor, test_model):
    session = Session()

    model = Resource(test_model, ResourceType.MODEL)
    model.register(session)

    session.tf_model_load(model)

    in_nodes = [Node(test_nodes["in"]["name"], test_nodes["in"]["id"])]
    out_nodes = [Node(test_nodes["out"]["name"], test_nodes["out"]["id"])]

    in_tensors = [
        Tensor(test_tensor["dims"], test_tensor["type"], test_tensor["data"])
    ]

    (out_tensors, status) = session.tf_model_run(
        model, in_nodes, in_tensors, out_nodes
    )
    assert status.message == "Operation handled by noop plugin"
    assert out_tensors[0].dims == in_tensors[0].dims
    assert out_tensors[0].data_type == in_tensors[0].data_type
    assert out_tensors[0].data == in_tensors[0].data
    assert out_tensors[0].as_bytelike() == in_tensors[0].as_bytelike()


def test_tf_from_buffer(test_nodes, test_tensor, test_model):
    session = Session()

    model = Resource(test_model, ResourceType.MODEL)
    model.register(session)

    session.tf_model_load(model)

    in_nodes = [Node(test_nodes["in"]["name"], test_nodes["in"]["id"])]
    out_nodes = [Node(test_nodes["out"]["name"], test_nodes["out"]["id"])]

    in_tensors = [
        Tensor.from_buffer(
            test_tensor["dims"], test_tensor["type"], test_tensor["data_bytes"]
        )
    ]

    (out_tensors, status) = session.tf_model_run(
        model, in_nodes, in_tensors, out_nodes
    )
    assert status.message == "Operation handled by noop plugin"
    assert out_tensors[0].dims == in_tensors[0].dims
    assert out_tensors[0].data_type == in_tensors[0].data_type
    assert out_tensors[0].data == in_tensors[0].data
    assert out_tensors[0].as_bytelike() == in_tensors[0].as_bytelike()


def test_tf_with_run_options(test_nodes, test_tensor, test_model):
    session = Session()

    model = Resource(test_model, ResourceType.MODEL)
    model.register(session)

    session.tf_model_load(model)

    in_nodes = [Node(test_nodes["in"]["name"], test_nodes["in"]["id"])]
    out_nodes = [Node(test_nodes["out"]["name"], test_nodes["out"]["id"])]

    in_tensors = [
        Tensor(test_tensor["dims"], test_tensor["type"], test_tensor["data"])
    ]

    run_options = Buffer(b"none")

    (out_tensors, status) = session.tf_model_run(
        model, in_nodes, in_tensors, out_nodes, run_options
    )
    assert status.message == "Operation handled by noop plugin"
    assert out_tensors[0].dims == in_tensors[0].dims
    assert out_tensors[0].data_type == in_tensors[0].data_type
    assert out_tensors[0].data == in_tensors[0].data
    assert out_tensors[0].as_bytelike() == in_tensors[0].as_bytelike()
