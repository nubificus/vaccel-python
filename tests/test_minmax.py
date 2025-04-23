from pathlib import Path

import pytest

from vaccel import Session


@pytest.fixture
def test_input(vaccel_paths) -> bytes:
    input_path = vaccel_paths["input"] / "input_2048.csv"
    with Path(input_path).open("rb") as f:
        return f.read()


def test_min_max_genop(test_input):
    session = Session()
    (outdata, min_val, max_val) = session.minmax(test_input, 2048, 5, 100)
    assert outdata == test_input[: len(outdata)]
    assert min_val == -1.0
    assert max_val == 10000.0
