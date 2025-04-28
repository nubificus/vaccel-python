# SPDX-License-Identifier: Apache-2.0

"""FPGA operations."""

from vaccel._c_types import CList
from vaccel._libvaccel import lib
from vaccel.error import FFIError


class FpgaMixin:
    """Mixin providing the FPGA operations for a `Session`.

    This mixin is intended to be used in combination with `BaseSession` and
    should not be instantiated on its own.

    Intended usage:
        class Session(BaseSession, FPGAMixin):
            ...
    """

    def fpga_arraycopy(self, a: list[int]) -> list[int]:
        """Performs the matrix copying operation.

        Wraps the `vaccel_fpga_arraycopy()` C operation.

        Args:
            a: The matrix A to be copied.

        Returns:
            A copy of the matrix A.

        Raises:
            RuntimeError: If the `Session` is uninitialized.
            FFIError: If the C operation fails.
        """
        c_a = CList(a)
        c_out_a = CList([0] * len(a))

        ret = lib.vaccel_fpga_arraycopy(
            self._c_ptr, c_a._c_ptr, c_out_a._c_ptr, len(c_a)
        )
        if ret != 0:
            raise FFIError(ret, "FPGA array copy failed")

        return [int(item) for item in c_out_a.value]

    def fpga_mmult(self, a: list[float], b: list[float]) -> list[float]:
        """Performs the matrix multiplication operation.

        Wraps the `vaccel_fpga_mmult()` C operation.

        Args:
            a: A matrix A.
            b: A matrix B.

        Returns:
            The multiplication result of matrices A and B.

        Raises:
            RuntimeError: If the `Session` is uninitialized.
            FFIError: If the C operation fails.
        """
        c_a = CList(a)
        c_b = CList(b)
        c_c = CList([float(0)] * len(a))

        ret = lib.vaccel_fpga_mmult(
            self._c_ptr, c_a._c_ptr, c_b._c_ptr, c_c._c_ptr, len(c_a)
        )
        if ret != 0:
            raise FFIError(ret, "FPGA matrix multiplication failed")

        return [float(item) for item in c_c.value]

    def fpga_parallel(
        self, a: list[float], b: list[float]
    ) -> (list[float], list[float]):
        """Performs the parallel matrix addition and multiplication operation.

        Wraps the `vaccel_fpga_parallel()` C operation.

        Args:
            a: A matrix A.
            b: A matrix B.

        Returns:
            A tuple containing:
                - The result of the addition of matrices A and B.
                - The result of the multiplication of matrices A and B.

        Raises:
            RuntimeError: If the `Session` is uninitialized.
            FFIError: If the C operation fails.
        """
        c_a = CList(a)
        c_b = CList(b)
        c_add_output = CList([float(0)] * len(a))
        c_mult_output = CList([float(0)] * len(a))

        ret = lib.vaccel_fpga_parallel(
            self._c_ptr,
            c_a._c_ptr,
            c_b._c_ptr,
            c_add_output._c_ptr,
            c_mult_output._c_ptr,
            len(c_a),
        )
        if ret != 0:
            raise FFIError(
                ret, "FPGA parallel matrix addition and multiplication failed"
            )

        return (
            [float(item) for item in c_add_output.value],
            [float(item) for item in c_mult_output.value],
        )

    def fpga_vadd(self, a: list[float], b: list[float]) -> list[float]:
        """Performs the matrix addition operation.

        Wraps the `vaccel_fpga_vadd()` C operation.

        Args:
            a: A matrix A.
            b: A matrix B.

        Returns:
            The addition result of matrices A and B.

        Raises:
            RuntimeError: If the `Session` is uninitialized.
            FFIError: If the C operation fails.
        """
        c_a = CList(a)
        c_b = CList(b)
        c_c = CList([float(0)] * len(a))

        ret = lib.vaccel_fpga_vadd(
            self._c_ptr, c_a._c_ptr, c_b._c_ptr, c_c._c_ptr, len(c_a), len(c_b)
        )
        if ret != 0:
            raise FFIError(ret, "FPGA vector addition failed")

        return [float(item) for item in c_c.value]
