# SPDX-License-Identifier: Apache-2.0

"""Minmax operation."""

from vaccel._c_types import CBytes, CFloat
from vaccel._libvaccel import ffi, lib
from vaccel.error import FFIError


class MinmaxMixin:
    """Mixin providing the Minmax operation for a `Session`.

    This mixin is intended to be used in combination with `BaseSession` and
    should not be instantiated on its own.

    Intended usage:
        class Session(BaseSession, MinmaxMixin):
            ...
    """

    def minmax(
        self, indata: bytes, ndata: int, low_threshold: int, high_threshold: int
    ) -> (bytes, float, float):
        """Performs the minmax operation.

        Wraps the `vaccel_minmax()` C operation.

        Args:
            indata: The input data as a `bytes` object.
            ndata: The number of data to be read provided data object.
            low_threshold: The threshold for the min value.
            high_threshold: The threshold for the max value.

        Returns:
            A tuple containing:
                - The resulting output data.
                - The detected min value of the data.
                - The detected max value of the data.

        Raises:
            RuntimeError: If the `Session` is uninitialized.
            FFIError: If the C operation fails.
        """
        c_indata = CBytes(indata)
        c_outdata = CBytes(bytearray(ndata * ffi.sizeof("double")))
        c_min = CFloat(float(0), "double")
        c_max = CFloat(float(0), "double")

        ret = lib.vaccel_minmax(
            self._c_ptr,
            c_indata._as_c_array("double"),
            ndata,
            low_threshold,
            high_threshold,
            c_outdata._as_c_array("double"),
            c_min._c_ptr,
            c_max._c_ptr,
        )
        if ret != 0:
            raise FFIError(ret, "Minmax operation failed")

        return (c_outdata.value, c_min.value, c_max.value)
