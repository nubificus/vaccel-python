"""Blas operations."""

from vaccel._c_types import CList
from vaccel._libvaccel import lib
from vaccel.error import FFIError


class BlasMixin:
    """Mixin providing Blas operations for a `Session`.

    This mixin is intended to be used in combination with `BaseSession` and
    should not be instantiated on its own.

    Intended usage:
        class Session(BaseSession, BlasMixin):
            ...
    """

    def sgemm(
        self,
        m: int,
        n: int,
        k: int,
        alpha: float,
        a: list[float],
        lda: int,
        b: list[float],
        ldb: int,
        beta: float,
        ldc: int,
    ) -> list[float]:
        """Performs the SGEMM operation.

        Wraps the `vaccel_sgemm()` C operation.

        Args:
            m: The number of rows in matrix A and matrix C.
            n: The number of columns in matrix B and matrix C.
            k: The number of columns in matrix A and rows in matrix B.
            alpha: Scalar multiplier for the matrix product A * B.
            a: The matrix A in row-major order with shape (m, k).
            lda: The leading dimension of matrix A (usually m).
            b: The matrix B in row-major order with shape (k, n).
            ldb: The leading dimension of matrix B (usually k).
            beta: Scalar multiplier for matrix C.
            ldc: The leading dimension of matrix C (usually m).

        Returns:
            The resulting matrix C in row-major order with shape (m, n).

        Raises:
            RuntimeError: If the `Session` is uninitialized.
            FFIError: If the C operation fails.
        """
        if not self._c_ptr:
            msg = "Uninitialized session"
            raise RuntimeError(msg)

        c_a = CList(a)
        c_b = CList(b)
        c_c = CList([float(0)] * m * n)

        ret = lib.vaccel_sgemm(
            self._c_ptr,
            m,
            n,
            k,
            alpha,
            c_a._c_ptr,
            lda,
            c_b._c_ptr,
            ldb,
            beta,
            c_c._c_ptr,
            ldc,
        )
        if ret != 0:
            raise FFIError(ret, "SGEMM failed")

        return c_c.value
