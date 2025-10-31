# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

import pytest

from vaccel import PluginType, Resource, ResourceType, Session


@pytest.fixture
def test_lib(vaccel_paths) -> Path:
    return vaccel_paths["lib"] / "libmytestlib.so"


def test_session():
    ses_a = Session()
    assert ses_a.id > 0
    assert ses_a.flags == 0
    assert ses_a.is_remote == 0

    ses_b = Session(flags=1)
    assert ses_b.id == ses_a.id + 1
    assert ses_b.flags == 1
    assert ses_b.is_remote == 0

    ses_c = Session(flags=PluginType.GENERIC | PluginType.DEBUG)
    assert ses_c.id == ses_b.id + 1
    assert ses_c.flags == PluginType.GENERIC | PluginType.DEBUG
    assert ses_c.is_remote == 0


def test_resource(test_lib):
    res_a = Resource(test_lib, ResourceType.LIB)
    res_b = Resource([test_lib, test_lib], ResourceType.LIB)
    assert res_b.id == res_a.id + 1


def test_noop():
    session = Session(flags=0)
    session.noop()
