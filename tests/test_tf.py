# SPDX-License-Identifier: Apache-2.0

import pytest

from vaccel import Resource, ResourceType, Session
from vaccel.ops.tf import Buffer, Node, Tensor, TensorType


@pytest.fixture
def test_model(vaccel_paths) -> bytes:
    return vaccel_paths["models"] / "tf" / "lstm2"


def test_tf(test_model):
    session = Session()

    model = Resource(test_model, ResourceType.MODEL)
    model.register(session)

    session.tf_model_load(model)

    in_nodes = [Node("serving_default_input_1", 0)]
    out_nodes = [Node("StatefulPartitionedCall", 0)]

    in_tensors = [Tensor([1, 30], TensorType.FLOAT, [1.0] * 30)]

    (out_tensors, status) = session.tf_model_run(
        model, in_nodes, in_tensors, out_nodes
    )
    assert status.message == "Operation handled by noop plugin"
    assert out_tensors[0].dims == in_tensors[0].dims
    assert out_tensors[0].data_type == in_tensors[0].data_type
    assert out_tensors[0].data == in_tensors[0].data

    run_options = Buffer(b"none")

    (out_tensors, status) = session.tf_model_run(
        model, in_nodes, in_tensors, out_nodes, run_options
    )
    assert status.message == "Operation handled by noop plugin"
    assert out_tensors[0].dims == in_tensors[0].dims
    assert out_tensors[0].data_type == in_tensors[0].data_type
    assert out_tensors[0].data == in_tensors[0].data
