# SPDX-License-Identifier: Apache-2.0

"""Interface to common vaccel C functions."""

import atexit

from ._libvaccel import lib
from .config import Config
from .error import FFIError


def bootstrap(config: Config | None = None) -> None:
    """Initializes the vAccel library.

    Args:
        config (Config | None): A configuration object for the library. If None,
            defaults are used.

    Raises:
        FFIError: If the C operation fails.
    """
    if config is None:
        ret = lib.vaccel_bootstrap()
    else:
        ret = lib.vaccel_bootstrap_with_config(config._c_ptr)
    if ret != 0:
        raise FFIError(ret, "Could not bootstrap vAccel library")


@atexit.register
def cleanup() -> None:
    """Cleans up the vAccel library resources.

    This function is called automatically at program exit, but can also be
    invoked explicitly if needed.

    Raises:
        FFIError: If the C operation fails.
    """
    ret = lib.vaccel_cleanup()
    if ret != 0:
        raise FFIError(ret, "Could not cleanup vAccel library objects")
