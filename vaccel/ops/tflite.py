# SPDX-License-Identifier: Apache-2.0

"""Tensorflow Lite operations."""

import logging
from typing import Any, ClassVar

from vaccel._c_types import CInt, CList, CType
from vaccel._c_types.utils import CEnumBuilder
from vaccel._libvaccel import ffi, lib
from vaccel.error import FFIError, NullPointerError
from vaccel.resource import Resource

logger = logging.getLogger(__name__)

enum_builder = CEnumBuilder(lib)
TensorType = enum_builder.from_prefix("TensorType", "VACCEL_TFLITE_")


class Tensor(CType):
    """Wrapper for the `struct vaccel_tflite_tensor` C object.

    Manages the creation and initialization of a C `struct vaccel_tflite_tensor`
    and provides access to it through Python properties.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _dims (list[int]): The dims of the tensor.
        _data (list[Any]): The data of the tensor.
        _data_type (TensorType): The type of the tensor.
        _c_obj_ptr (ffi.CData): A double pointer to the underlying
            `struct vaccel_tflite_tensor` C object.
        _c_obj_data (ffi.CData): A pointer to the data of the underlying
            `struct vaccel_tflite_tensor` C object.

    """

    _size_dict: ClassVar[dict[TensorType, (int, str)]] = {
        TensorType.FLOAT32: (ffi.sizeof("float"), "float"),
        TensorType.INT32: (ffi.sizeof("int32_t"), "int32_t"),
        TensorType.UINT8: (ffi.sizeof("uint8_t"), "uint8_t"),
        TensorType.INT64: (ffi.sizeof("int64_t"), "int64_t"),
        TensorType.BOOL: (ffi.sizeof("bool"), "bool"),
        TensorType.INT16: (ffi.sizeof("int16_t"), "int16_t"),
        TensorType.INT8: (ffi.sizeof("int8_t"), "int8_t"),
        TensorType.FLOAT64: (ffi.sizeof("double"), "double"),
        TensorType.UINT64: (ffi.sizeof("uint64_t"), "uint64_t"),
        TensorType.UINT32: (ffi.sizeof("uint32_t"), "uint32_t"),
        TensorType.UINT16: (ffi.sizeof("uint16_t"), "uint16_t"),
    }

    def __init__(self, dims: list[int], data_type: TensorType, data: list[Any]):
        """Initializes a new `Tensor` object.

        Args:
            dims: The dims to be passed to the C struct.
            data_type: The data_type to be passed to the C struct.
            data: The data to be passed to the C struct.
        """
        self._dims = dims
        self._data = data
        self._data_type = data_type
        self._c_obj_ptr = ffi.NULL
        self._c_obj_data = ffi.NULL
        super().__init__()

    def _init_c_obj(self):
        """Initializes the underlying C `struct vaccel_tflite_tensor` object.

        Raises:
            FFIError: If tensor initialization fails.
        """
        nr_dims = len(self._dims)
        c_dims = ffi.new(f"int32_t[{nr_dims}]", self._dims)

        self._c_obj_ptr = ffi.new("struct vaccel_tflite_tensor **")
        ret = lib.vaccel_tflite_tensor_new(
            self._c_obj_ptr, nr_dims, c_dims, self._data_type
        )
        if ret != 0:
            FFIError(ret, "Could not initialize tensor")

        self._c_obj = self._c_obj_ptr[0]
        self._c_size = ffi.sizeof("struct vaccel_tflite_tensor")

        self._c_obj_data = ffi.new(
            f"{self._c_data_type}[{len(self._data)}]", self._data
        )

        ret = lib.vaccel_tflite_tensor_set_data(
            self._c_obj, self._c_obj_data, self._c_data_size * len(self._data)
        )
        if ret != 0:
            raise FFIError(ret, "Could not set tensor data")

    @property
    def value(self) -> ffi.CData:
        """Returns the value of the underlying C struct.

        Returns:
            The dereferenced 'struct vaccel_tflite_tensor`
        """
        return self._c_ptr_or_raise[0]

    def _del_c_obj(self):
        """Deletes the underlying `struct vaccel_tflite_tensor` C object.

        Raises:
            FFIError: If tensor deletion fails.
        """
        ret = lib.vaccel_tflite_tensor_delete(self._c_ptr_or_raise)
        if ret != 0:
            raise FFIError(ret, "Could not delete tensor")

    def __del__(self):
        try:
            self._del_c_obj()
        except NullPointerError:
            pass
        except FFIError:
            logger.exception("Failed to clean up Tensor")

    @property
    def _c_data_size(self):
        return self._size_dict[self.data_type][0]

    @property
    def _c_data_type(self):
        return self._size_dict[self.data_type][1]

    @property
    def dims(self) -> list[int]:
        """The tensor dims.

        Returns:
            The dims of the tensor.
        """
        return [
            int(self._c_ptr_or_raise.dims[i])
            for i in range(self._c_ptr_or_raise.nr_dims)
        ]

    @property
    def data(self) -> list | str:
        """The tensor data.

        Returns:
            The data of the tensor.
        """
        typed_c_data = ffi.cast(
            f"{self._c_data_type} *", self._c_ptr_or_raise.data
        )
        return ffi.unpack(
            typed_c_data, int(self._c_ptr_or_raise.size / self._c_data_size)
        )

    @property
    def data_type(self) -> TensorType:
        """The tensor data type.

        Returns:
            The data type of the tensor.
        """
        return TensorType(self._c_ptr_or_raise.data_type)

    @classmethod
    def from_c_obj(cls, c_obj: ffi.CData) -> "Tensor":
        """Initializes a new `Tensor` object from an existing C struct.

        Args:
            c_obj: A pointer to a `struct vaccel_tflite_tensor` C object.

        Returns:
            A new `Tensor` object
        """
        type_str = ffi.getctype(ffi.typeof(c_obj))
        if type_str != "struct vaccel_tflite_tensor *":
            msg = f"Expected 'struct vaccel_tflite_tensor *', got '{type_str}'"
            raise TypeError(msg)

        inst = cls.__new__(cls)
        inst._c_obj = c_obj
        inst._c_size = ffi.sizeof(inst._c_obj)
        inst._dims = None
        inst._data = None
        inst._data_type = None
        inst._c_obj_ptr = ffi.NULL
        return inst

    @classmethod
    def empty(cls) -> "Tensor":
        """Initializes a new empty `Tensor` object.

        The object a NULL pointer in place of the C struct.

        Returns:
            A new `Tensor` object
        """
        inst = cls.__new__(cls)
        inst._c_obj_ptr = ffi.new("struct vaccel_tflite_tensor **")
        inst._c_obj = inst._c_obj_ptr[0]
        inst._c_obj_ptr[0] = ffi.NULL
        inst._c_size = ffi.sizeof("struct vaccel_tflite_tensor *")
        return inst

    def __repr__(self):
        return f"<Tensor dims={self.dims} data_type={self.data_type}>"


class TFLiteMixin:
    """Mixin providing Tensorflow Lite operations for a `Session`.

    This mixin is intended to be used in combination with `BaseSession` and
    should not be instantiated on its own.

    Intended usage:
        class Session(BaseSession, TensorflowLiteMixin):
            ...
    """

    def tflite_model_load(self, resource: Resource) -> None:
        """Performs the Tensorflow Lite model loading operation.

        Wraps the `vaccel_tflite_session_load()` C operation.

        Args:
            resource: A resource with the model to load.

        Raises:
            FFIError: If the C operation fails.
        """
        ret = lib.vaccel_tflite_session_load(
            self._c_ptr_or_raise, resource._c_ptr
        )
        if ret != 0:
            raise FFIError(ret, "Tensorflow Lite model loading failed")

    def tflite_model_run(
        self,
        resource: Resource,
        in_tensors: list[Tensor],
        nr_out_tensors: int = 1,
    ) -> (list[Tensor], int):
        """Performs the Tensorflow Lite model run operation.

        Wraps the `vaccel_tflite_session_run()` C operation.

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

        ret = lib.vaccel_tflite_session_run(
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

    def tflite_model_delete(self, resource: Resource) -> None:
        """Performs the Tensorflow Lite model deletion operation.

        Wraps the `vaccel_tflite_session_delete()` C operation.

        Args:
            resource: A resource with the model to unload.

        Returns:
            The status of the operation execution.

        Raises:
            FFIError: If the C operation fails.
        """
        ret = lib.vaccel_tflite_session_delete(
            self._c_ptr_or_raise, resource._c_ptr
        )
        if ret != 0:
            raise FFIError(ret, "Tensorflow Lite model delete failed")
