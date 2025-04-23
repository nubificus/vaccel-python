from pathlib import Path

import pytest

from vaccel import Session


@pytest.fixture
def test_image(vaccel_paths) -> bytes:
    image_path = vaccel_paths["images"] / "example.jpg"
    with Path(image_path).open("rb") as f:
        return f.read()


def test_image_classify(test_image):
    session = Session()
    res = session.classify(test_image)
    assert res == (
        "This is a dummy classification tag!",
        "This is a dummy imgname!",
    )


def test_image_detect(test_image):
    session = Session()
    res = session.detect(test_image)
    assert res == "This is a dummy imgname!"


def test_image_segment(test_image):
    session = Session()
    res = session.segment(test_image)
    assert res == "This is a dummy imgname!"


def test_image_pose(test_image):
    session = Session()
    res = session.pose(test_image)
    assert res == "This is a dummy imgname!"


def test_image_depth(test_image):
    session = Session()
    res = session.depth(test_image)
    assert res == "This is a dummy imgname!"
