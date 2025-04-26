import pytest

from vaccel import Resource, ResourceType, Session
from vaccel.torch import Tensor, TensorType


@pytest.fixture
def test_model(vaccel_paths) -> bytes:
    return vaccel_paths["models"] / "torch" / "cnn_trace.pt"


def test_torch(test_model):
    session = Session()

    model = Resource(test_model, ResourceType.MODEL)
    model.register(session)

    in_tensors = [Tensor([1, 30], TensorType.FLOAT, [1.0] * 30)]

    out_tensors = session.torch_jitload_forward(model, in_tensors)
    assert out_tensors[0].dims == in_tensors[0].dims
    assert out_tensors[0].data_type == in_tensors[0].data_type
    assert out_tensors[0].data == in_tensors[0].data
