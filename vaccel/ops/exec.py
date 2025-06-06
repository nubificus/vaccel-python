# SPDX-License-Identifier: Apache-2.0

"""Exec operations."""

from pathlib import Path
from typing import Any

from vaccel._c_types import CList
from vaccel._libvaccel import lib
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
        arg_read: list[Any],
        arg_write: list[Any],
    ) -> list[Any]:
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
        c_arg_read = CList([Arg(arg) for arg in arg_read])
        c_arg_write = CList([Arg(arg) for arg in arg_write])

        ret = lib.vaccel_exec(
            self._c_ptr_or_raise,
            str(library).encode(),
            symbol.encode(),
            c_arg_read._c_ptr,
            len(c_arg_read),
            c_arg_write._c_ptr,
            len(c_arg_write),
        )
        if ret != 0:
            raise FFIError(ret, "Exec operation failed")

        return [c_arg_write[i].buf for i in range(len(c_arg_write))]

    def exec_with_resource(
        self,
        resource: Resource,
        symbol: str,
        arg_read: list[Any],
        arg_write: list[Any],
    ) -> list[Any]:
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
        c_arg_read = CList([Arg(arg) for arg in arg_read])
        c_arg_write = CList([Arg(arg) for arg in arg_write])

        ret = lib.vaccel_exec_with_resource(
            self._c_ptr_or_raise,
            resource._c_ptr,
            symbol.encode(),
            c_arg_read._c_ptr,
            len(c_arg_read),
            c_arg_write._c_ptr,
            len(c_arg_write),
        )
        if ret != 0:
            raise FFIError(ret, "Exec with resource operation failed")

        return [c_arg_write[i].buf for i in range(len(c_arg_write))]
