# SPDX-License-Identifier: Apache-2.0

"""Tensorflow Lite operations."""

from vaccel._c_types import CInt, CList
from vaccel._libvaccel import lib
from vaccel.error import FFIError
from vaccel.resource import Resource

from .tensor import Tensor


class TFLiteMixin:
    """Mixin providing Tensorflow Lite operations for a `Session`.

    This mixin is intended to be used in combination with `BaseSession` and
    should not be instantiated on its own.

    Intended usage:
        class Session(BaseSession, TensorflowLiteMixin):
            ...
    """

    def tflite_model_load(self, resource: Resource) -> None:
        """Performs the Tensorflow Lite model load operation.

        Wraps the `vaccel_tflite_model_load()` C operation.

        Args:
            resource: A resource with the model to load.

        Raises:
            FFIError: If the C operation fails.
        """
        ret = lib.vaccel_tflite_model_load(
            self._c_ptr_or_raise, resource._c_ptr
        )
        if ret != 0:
            raise FFIError(ret, "Tensorflow Lite model load failed")

    def tflite_model_unload(self, resource: Resource) -> None:
        """Performs the Tensorflow Lite model unload operation.

        Wraps the `vaccel_tflite_model_unload()` C operation.

        Args:
            resource: A resource with the model to unload.

        Returns:
            The status of the operation execution.

        Raises:
            FFIError: If the C operation fails.
        """
        ret = lib.vaccel_tflite_model_unload(
            self._c_ptr_or_raise, resource._c_ptr
        )
        if ret != 0:
            raise FFIError(ret, "Tensorflow Lite model unload failed")

    def tflite_model_run(
        self,
        resource: Resource,
        in_tensors: list[Tensor],
        nr_out_tensors: int = 1,
    ) -> (list[Tensor], int):
        """Performs the Tensorflow Lite model run operation.

        Wraps the `vaccel_tflite_model_run()` C operation.

        Args:
            resource: A resource with the model to run.
            in_tensors: The input tensors for the inference.
            nr_out_tensors: The number of output tensors. Defaults to 1.

        Returns:
            A tuple containing:
                - The output tensors
                - The status of the operation execution.

        Raises:
            FFIError: If the C operation fails.
        """
        c_in_tensors = CList.from_ptrs(in_tensors)
        c_out_tensors = CList.from_ptrs([Tensor.empty()] * nr_out_tensors)
        status = CInt(0, "uint8_t")

        ret = lib.vaccel_tflite_model_run(
            self._c_ptr_or_raise,
            resource._c_ptr,
            c_in_tensors._c_ptr,
            len(c_in_tensors),
            c_out_tensors._c_ptr,
            len(c_out_tensors),
            status._c_ptr,
        )
        if ret != 0:
            raise FFIError(ret, "Tensorflow Lite model run failed")

        out_tensors = [Tensor.from_c_obj(t) for t in c_out_tensors.value]
        return (out_tensors, status.value)
