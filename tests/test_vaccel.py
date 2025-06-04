# SPDX-License-Identifier: Apache-2.0

import vaccel
from vaccel import Config


def test_bootstrap_default():
    vaccel.bootstrap()


def test_bootstrap_with_config():
    config = Config()
    vaccel.bootstrap(config)


def test_cleanup():
    vaccel.cleanup()


def test_bootstrap_default_and_cleanup():
    vaccel.bootstrap()
    vaccel.cleanup()


def test_bootstrap_with_config_and_cleanup():
    config = Config()
    vaccel.bootstrap(config)
    vaccel.cleanup()
