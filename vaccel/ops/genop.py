"""Generic operation."""

from vaccel._c_types import CList
from vaccel._libvaccel import lib
from vaccel.arg import Arg
from vaccel.error import FFIError


class GenopMixin:
    """Mixin providing the Generic operation for a `Session`.

    This mixin is intended to be used in combination with `BaseSession` and
    should not be instantiated on its own.

    Intended usage:
        class Session(BaseSession, GenopMixin):
            ...
    """

    def genop(self, arg_read: list[Arg], arg_write: list[Arg]) -> None:
        """Performs the Generic operation.

        Wraps the `vaccel_genop()` C operation.

        Args:
            arg_read: The input arguments of the operation.
            arg_write: The output arguments of the operation. Modified in place.

        Raises:
            RuntimeError: If the `Session` is uninitialized.
            FFIError: If the C operation fails.
        """
        c_args_read = CList(arg_read)
        c_args_write = CList(arg_write)

        ret = lib.vaccel_genop(
            self._c_ptr,
            c_args_read._c_ptr,
            len(c_args_read),
            c_args_write._c_ptr,
            len(c_args_write),
        )
        if ret:
            raise FFIError(ret, "Generic operation failed")
