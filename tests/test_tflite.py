import pytest

from vaccel import Resource, ResourceType, Session
from vaccel.tflite import Tensor, TensorType


@pytest.fixture
def test_model(vaccel_paths) -> bytes:
    return vaccel_paths["models"] / "tf" / "lstm2.tflite"


def test_tflite(test_model):
    session = Session()

    model = Resource(test_model, ResourceType.MODEL)
    model.register(session)

    session.tflite_model_load(model)

    in_tensors = [Tensor([1, 30], TensorType.FLOAT32, [1.0] * 30)]

    (out_tensors, status) = session.tflite_model_run(model, in_tensors)
    assert status == 0
    assert out_tensors[0].dims == in_tensors[0].dims
    assert out_tensors[0].data_type == in_tensors[0].data_type
    assert out_tensors[0].data == in_tensors[0].data
