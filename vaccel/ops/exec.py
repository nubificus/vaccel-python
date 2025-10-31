# SPDX-License-Identifier: Apache-2.0

"""Exec operations."""

from pathlib import Path
from typing import Any

from vaccel._c_types import CList
from vaccel._libvaccel import ffi, lib
from vaccel.arg import Arg
from vaccel.error import FFIError
from vaccel.resource import Resource


class ExecMixin:
    """Mixin providing the Exec operations for a `Session`.

    This mixin is intended to be used in combination with `BaseSession` and
    should not be instantiated on its own.

    Intended usage:
        class Session(BaseSession, ExecMixin):
            ...
    """

    def exec(
        self,
        library: str | Path,
        symbol: str,
        arg_read: list[Any] | None = None,
        arg_write: list[Any] | None = None,
    ) -> list[Any] | None:
        """Performs the Exec operation.

        Wraps the `vaccel_exec()` C operation.

        Args:
            library: The path to the shared object containing the function that
                will be called.
            symbol: The name of the function contained in the above shared
                object.
            arg_read: The input arguments that will be passed to the
                called function.
            arg_write: The output arguments that will be passed to the
                called function.

        Returns:
            The resulting outputs.

        Raises:
            FFIError: If the C operation fails.
        """
        if arg_read is not None:
            c_arg_read = CList(
                [arg if isinstance(arg, Arg) else Arg(arg) for arg in arg_read]
            )
            c_arg_read_ptr = c_arg_read._c_ptr
            c_arg_read_len = len(c_arg_read)
        else:
            c_arg_read = None
            c_arg_read_ptr = ffi.NULL
            c_arg_read_len = 0

        if arg_write is not None:
            c_arg_write = CList(
                [arg if isinstance(arg, Arg) else Arg(arg) for arg in arg_write]
            )
            c_arg_write_ptr = c_arg_write._c_ptr
            c_arg_write_len = len(c_arg_write)
        else:
            c_arg_write = None
            c_arg_write_ptr = ffi.NULL
            c_arg_write_len = 0

        ret = lib.vaccel_exec(
            self._c_ptr_or_raise,
            str(library).encode(),
            symbol.encode(),
            c_arg_read_ptr,
            c_arg_read_len,
            c_arg_write_ptr,
            c_arg_write_len,
        )
        if ret != 0:
            raise FFIError(ret, "Exec operation failed")

        if c_arg_write is not None:
            return [c_arg_write[i].buf for i in range(len(c_arg_write))]
        return None

    def exec_with_resource(
        self,
        resource: Resource,
        symbol: str,
        arg_read: list[Any] | None = None,
        arg_write: list[Any] | None = None,
    ) -> list[Any] | None:
        """Performs the Exec with resource operation.

        Wraps the `vaccel_exec_with_resource()` C operation.

        Args:
            resource: The resource of the shared object containing the function
                that will be called.
            symbol: The name of the function contained in the above shared
                object.
            arg_read: The input arguments that will be passed to the
                called function.
            arg_write: The output arguments that will be passed to the
                called function.

        Returns:
            The resulting outputs.

        Raises:
            FFIError: If the C operation fails.
        """
        if arg_read is not None:
            c_arg_read = CList(
                [arg if isinstance(arg, Arg) else Arg(arg) for arg in arg_read]
            )
            c_arg_read_ptr = c_arg_read._c_ptr
            c_arg_read_len = len(c_arg_read)
        else:
            c_arg_read = None
            c_arg_read_ptr = ffi.NULL
            c_arg_read_len = 0

        if arg_write is not None:
            c_arg_write = CList(
                [arg if isinstance(arg, Arg) else Arg(arg) for arg in arg_write]
            )
            c_arg_write_ptr = c_arg_write._c_ptr
            c_arg_write_len = len(c_arg_write)
        else:
            c_arg_write = None
            c_arg_write_ptr = ffi.NULL
            c_arg_write_len = 0

        ret = lib.vaccel_exec_with_resource(
            self._c_ptr_or_raise,
            resource._c_ptr,
            symbol.encode(),
            c_arg_read_ptr,
            c_arg_read_len,
            c_arg_write_ptr,
            c_arg_write_len,
        )
        if ret != 0:
            raise FFIError(ret, "Exec with resource operation failed")

        if c_arg_write is not None:
            return [c_arg_write[i].buf for i in range(len(c_arg_write))]
        return None
