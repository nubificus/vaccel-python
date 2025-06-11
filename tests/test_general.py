# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

import pytest

from vaccel import Resource, ResourceType, Session


@pytest.fixture
def test_lib(vaccel_paths) -> Path:
    return vaccel_paths["lib"] / "libmytestlib.so"


def test_session():
    ses_a = Session(flags=0)
    ses_b = Session(flags=1)
    assert ses_b.id == ses_a.id + 1


def test_resource(test_lib):
    res_a = Resource(test_lib, ResourceType.LIB)
    res_b = Resource([test_lib, test_lib], ResourceType.LIB)
    assert res_b.id == res_a.id + 1


def test_noop():
    session = Session(flags=0)
    session.noop()
