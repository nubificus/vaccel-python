# SPDX-License-Identifier: Apache-2.0

"""Tensorflow operations."""

from vaccel._c_types import CList
from vaccel._libvaccel import ffi, lib
from vaccel.error import FFIError
from vaccel.resource import Resource

from .buffer import Buffer
from .node import Node
from .status import Status
from .tensor import Tensor


class TFMixin:
    """Mixin providing Tensorflow operations for a `Session`.

    This mixin is intended to be used in combination with `BaseSession` and
    should not be instantiated on its own.

    Intended usage:
        class Session(BaseSession, TensorflowMixin):
            ...
    """

    def tf_model_load(self, resource: Resource) -> Status:
        """Performs the Tensorflow model load operation.

        Wraps the `vaccel_tf_model_load()` C operation.

        Args:
            resource: A resource with the model to load.

        Returns:
            The status of the operation execution.

        Raises:
            FFIError: If the C operation fails.
        """
        status = Status()
        ret = lib.vaccel_tf_model_load(
            self._c_ptr_or_raise, resource._c_ptr, status._c_ptr
        )
        if ret != 0:
            raise FFIError(ret, "Tensorflow model load failed")
        return status

    def tf_model_unload(self, resource: Resource) -> Status:
        """Performs the Tensorflow model unload operation.

        Wraps the `vaccel_tf_model_unload()` C operation.

        Args:
            resource: A resource with the model to unload.

        Returns:
            The status of the operation execution.

        Raises:
            FFIError: If the C operation fails.
        """
        status = Status()
        ret = lib.vaccel_tf_model_unload(
            self._c_ptr_or_raise, resource._c_ptr, status._c_ptr
        )
        if ret != 0:
            raise FFIError(ret, "Tensorflow model unload failed")
        return status

    def tf_model_run(
        self,
        resource: Resource,
        in_nodes: list[Node],
        in_tensors: list[Tensor],
        out_nodes: list[Node],
        run_options: Buffer | None = None,
    ) -> (list[Tensor], Status):
        """Performs the Tensorflow model run operation.

        Wraps the `vaccel_tf_model_run()` C operation.

        Args:
            resource: A resource with the model to run.
            in_nodes: The input nodes for the inference.
            in_tensors: The input tensors for the inference.
            out_nodes: The output nodes for the inference.
            run_options: The inference options.

        Returns:
            A tuple containing:
                - The output tensors
                - The status of the operation execution.

        Raises:
            FFIError: If the C operation fails.
        """
        run_options_ptr = (
            ffi.NULL if run_options is None else run_options._c_ptr
        )
        c_in_nodes = CList(in_nodes)
        c_in_tensors = CList.from_ptrs(in_tensors)
        c_out_nodes = CList(out_nodes)
        c_out_tensors = CList.from_ptrs([Tensor.empty()] * len(c_out_nodes))
        status = Status()

        ret = lib.vaccel_tf_model_run(
            self._c_ptr_or_raise,
            resource._c_ptr,
            run_options_ptr,
            c_in_nodes._c_ptr,
            c_in_tensors._c_ptr,
            len(c_in_nodes),
            c_out_nodes._c_ptr,
            c_out_tensors._c_ptr,
            len(c_out_nodes),
            status._c_ptr,
        )
        if ret != 0:
            raise FFIError(ret, "Tensorflow model run failed")

        out_tensors = [Tensor.from_c_obj(t) for t in c_out_tensors.value]
        return (out_tensors, status)
