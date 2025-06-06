# SPDX-License-Identifier: Apache-2.0

"""Debug operation."""

from vaccel._libvaccel import lib
from vaccel.error import FFIError


class NoopMixin:
    """Mixin providing the NoOp operation for a `Session`.

    This mixin is intended to be used in combination with `BaseSession` and
    should not be instantiated on its own.

    Intended usage:
        class Session(BaseSession, NoopMixin):
            ...
    """

    def noop(self) -> None:
        """Performs the NoOp operation.

        Wraps the `vaccel_noop()` C operation.

        Raises:
            FFIError: If the C operation fails.
        """
        ret = lib.vaccel_noop(self._c_ptr_or_raise)
        if ret != 0:
            raise FFIError(ret, "NoOp operation failed")
