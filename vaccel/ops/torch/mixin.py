# SPDX-License-Identifier: Apache-2.0

"""Torch operations."""

from vaccel._c_types import CList
from vaccel._libvaccel import ffi, lib
from vaccel.error import FFIError
from vaccel.resource import Resource

from .buffer import Buffer
from .tensor import Tensor


class TorchMixin:
    """Mixin providing Torch operations for a `Session`.

    This mixin is intended to be used in combination with `BaseSession` and
    should not be instantiated on its own.

    Intended usage:
        class Session(BaseSession, TorchMixin):
            ...
    """

    def torch_model_load(self, resource: Resource) -> None:
        """Performs the Torch model load operation.

        Wraps the `vaccel_torch_model_load()` C operation.

        Args:
            resource: A resource with the model to load.

        Raises:
            FFIError: If the C operation fails.
        """
        ret = lib.vaccel_torch_model_load(self._c_ptr_or_raise, resource._c_ptr)
        if ret != 0:
            raise FFIError(ret, "Torch model load failed")

    def torch_model_run(
        self,
        resource: Resource,
        in_tensors: list[Tensor],
        nr_out_tensors: int = 1,
        run_options: Buffer | None = None,
    ) -> list[Tensor]:
        """Performs the Torch model run operation.

        Wraps the `vaccel_torch_model_run()` C operation.

        Args:
            resource: A resource with the model to run.
            in_tensors: The input tensors for the inference.
            nr_out_tensors: The number of output tensors. Defaults to 1.
            run_options: The inference options.

        Returns:
            The output tensors

        Raises:
            FFIError: If the C operation fails.
        """
        run_options_ptr = (
            ffi.NULL if run_options is None else run_options._c_ptr
        )
        c_in_tensors = CList.from_ptrs(in_tensors)
        c_out_tensors = CList.from_ptrs([Tensor.empty()] * nr_out_tensors)

        ret = lib.vaccel_torch_model_run(
            self._c_ptr_or_raise,
            resource._c_ptr,
            run_options_ptr,
            c_in_tensors._c_ptr,
            len(c_in_tensors),
            c_out_tensors._c_ptr,
            len(c_out_tensors),
        )
        if ret != 0:
            raise FFIError(ret, "Torch jitload forward operation failed")

        return [Tensor.from_c_obj(t) for t in c_out_tensors.value]
