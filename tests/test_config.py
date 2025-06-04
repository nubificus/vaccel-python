# SPDX-License-Identifier: Apache-2.0

import pytest

from vaccel import Config


@pytest.fixture
def test_data():
    return {
        "plugins": "libvaccel-exec.so",
        "log_level": 4,
        "log_file": "vaccel.log",
        "profiling_enabled": True,
        "version_ignore": True,
    }


def test_config_default():
    config = Config()
    assert config.plugins == "libvaccel-noop.so"
    assert config.log_level == 1
    assert config.log_file is None
    assert not config.profiling_enabled
    assert not config.version_ignore


def test_config_with_data(test_data):
    config = Config(
        plugins=test_data["plugins"],
        log_level=test_data["log_level"],
        log_file=test_data["log_file"],
        profiling_enabled=test_data["profiling_enabled"],
        version_ignore=test_data["version_ignore"],
    )
    assert config.plugins == test_data["plugins"]
    assert config.log_level == test_data["log_level"]
    assert config.log_file == test_data["log_file"]
    assert config.profiling_enabled == test_data["profiling_enabled"]
    assert config.version_ignore == test_data["version_ignore"]
