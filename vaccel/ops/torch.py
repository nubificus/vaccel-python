# SPDX-License-Identifier: Apache-2.0

"""Torch operations."""

from typing import Any, ClassVar

from vaccel._c_types import CBytes, CList, CType
from vaccel._c_types.utils import CEnumBuilder
from vaccel._libvaccel import ffi, lib
from vaccel.error import FFIError
from vaccel.resource import Resource

enum_builder = CEnumBuilder(lib)
TensorType = enum_builder.from_prefix("TensorType", "VACCEL_TORCH_")


class Tensor(CType):
    """Wrapper for the `struct vaccel_torch_tensor` C object.

    Manages the creation and initialization of a C `struct vaccel_torch_tensor`
    and provides access to it through Python properties.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _dims (list[int]): The dims of the tensor.
        _data (list[Any]): The data of the tensor.
        _data_type (TensorType): The type of the tensor.
        _c_obj_ptr (ffi.CData or None): A double pointer to the underlying
            `struct vaccel_torch_tensor` C object.
        _c_obj_data (ffi.CData or None): A pointer to the data of the underlying
            `struct vaccel_torch_tensor` C object.

    """

    _size_dict: ClassVar[dict[TensorType, (int, str)]] = {
        TensorType.BYTE: (ffi.sizeof("uint8_t"), "uint8_t"),
        TensorType.CHAR: (ffi.sizeof("int8_t"), "int8_t"),
        TensorType.SHORT: (ffi.sizeof("int16_t"), "int16_t"),
        TensorType.INT: (ffi.sizeof("int32_t"), "int32_t"),
        TensorType.LONG: (ffi.sizeof("int64_t"), "int64_t"),
        TensorType.FLOAT: (ffi.sizeof("float"), "float"),
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
        self._c_obj_ptr = None
        self._c_obj_data = None
        super().__init__()

    def _init_c_obj(self):
        """Initializes the underlying C `struct vaccel_torch_tensor` object.

        Raises:
            FFIError: If tensor initialization fails.
        """
        nr_dims = len(self._dims)
        c_dims = ffi.new(f"int64_t[{nr_dims}]", self._dims)

        self._c_obj_ptr = ffi.new("struct vaccel_torch_tensor **")
        ret = lib.vaccel_torch_tensor_new(
            self._c_obj_ptr, nr_dims, c_dims, self._data_type
        )
        if ret != 0:
            FFIError(ret, "Could not initialize tensor")

        self._c_obj = self._c_obj_ptr[0]
        self._c_size = ffi.sizeof("struct vaccel_torch_tensor")

        self._c_obj_data = ffi.new(
            f"{self._c_data_type}[{len(self._data)}]", self._data
        )

        ret = lib.vaccel_torch_tensor_set_data(
            self._c_obj, self._c_obj_data, self._c_data_size * len(self._data)
        )
        if ret != 0:
            raise FFIError(ret, "Could not set tensor data")

    @property
    def value(self) -> ffi.CData:
        """Returns the value of the underlying C struct.

        Returns:
            The dereferenced 'struct vaccel_torch_tensor`
        """
        return self._c_obj[0]

    def __del__(self):
        """Deletes the underlying `struct vaccel_torch_tensor` C object.

        Raises:
            FFIError: If tensor deletion fails.
        """
        if hasattr(self, "_c_obj") and self._c_obj:
            ret = lib.vaccel_torch_tensor_delete(self._c_obj)
            if ret != 0:
                raise FFIError(ret, "Could not delete tensor")

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
        return [int(self._c_obj.dims[i]) for i in range(self._c_obj.nr_dims)]

    @property
    def data(self) -> list | str:
        """The tensor data.

        Returns:
            The data of the tensor.
        """
        typed_c_data = ffi.cast(f"{self._c_data_type} *", self._c_obj.data)
        return ffi.unpack(
            typed_c_data, int(self._c_obj.size / self._c_data_size)
        )

    @property
    def data_type(self) -> TensorType:
        """The tensor data type.

        Returns:
            The data type of the tensor.
        """
        return TensorType(self._c_obj.data_type)

    @classmethod
    def from_c_obj(cls, c_obj: ffi.CData) -> "Tensor":
        """Initializes a new `Tensor` object from an existing C struct.

        Args:
            c_obj: A pointer to a `struct vaccel_torch_tensor` C object.

        Returns:
            A new `Tensor` object
        """
        type_str = ffi.getctype(ffi.typeof(c_obj))
        if type_str != "struct vaccel_torch_tensor *":
            msg = f"Expected 'struct vaccel_torch_tensor *', got '{type_str}'"
            raise TypeError(msg)

        inst = cls.__new__(cls)
        inst._c_obj = c_obj
        inst._c_size = ffi.sizeof(inst._c_obj)
        inst._dims = None
        inst._data = None
        inst._data_type = None
        inst._c_obj_ptr = None
        return inst

    @classmethod
    def empty(cls) -> "Tensor":
        """Initializes a new empty `Tensor` object.

        The object a NULL pointer in place of the C struct.

        Returns:
            A new `Tensor` object
        """
        inst = cls.__new__(cls)
        inst._c_obj_ptr = ffi.new("struct vaccel_torch_tensor **")
        inst._c_obj = inst._c_obj_ptr[0]
        inst._c_obj_ptr[0] = ffi.NULL
        inst._c_size = ffi.sizeof("struct vaccel_torch_tensor *")
        return inst

    def __repr__(self):
        return f"<Tensor dims={self.dims} data_type={self.data_type}>"


class Buffer(CType):
    """Wrapper for the `struct vaccel_torch_buffer` C object.

    Manages the creation and initialization of a C `struct vaccel_torch_buffer`
    and provides access to it through Python properties.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _data (bytes | bytearray): The data of the buffer.
        _c_data (CBytes): The encapsulated buffer data passed to the C struct.
        _c_obj_ptr (ffi.CData or None): A double pointer to the underlying
            `struct vaccel_torch_buffer` C object.
    """

    def __init__(self, data: bytes | bytearray):
        """Initializes a new `Buffer` object.

        Args:
            data: The buffer data to be passed to the C struct.
        """
        self._data = data
        self._c_data = None
        self._c_obj_ptr = None
        super().__init__()

    def _init_c_obj(self):
        """Initializes the underlying C `struct vaccel_torch_buffer` object.

        Raises:
            FFIError: If buffer initialization fails.
        """
        self._c_data = CBytes(self._data)
        self._c_obj_ptr = ffi.new("struct vaccel_torch_buffer **")

        ret = lib.vaccel_torch_buffer_new(
            self._c_obj_ptr, self._c_data._c_ptr, len(self._c_data)
        )
        if ret != 0:
            raise FFIError(ret, "Could not initialize buffer")

        self._c_obj = self._c_obj_ptr[0]
        self._c_size = ffi.sizeof("struct vaccel_torch_buffer")

    @property
    def value(self) -> ffi.CData:
        """Returns the value of the underlying C struct.

        Returns:
            The dereferenced 'struct vaccel_torch_buffer`
        """
        return self._c_obj[0]

    def __del__(self):
        """Deletes the underlying `struct vaccel_torch_buffer` C object.

        Raises:
            FFIError: If buffer deletion fails.
        """
        if hasattr(self, "_c_obj") and self._c_obj:
            c_data = ffi.new("void **")
            c_size = ffi.new("size_t *")
            ret = lib.vaccel_torch_buffer_take_data(self._c_obj, c_data, c_size)
            if ret != 0:
                raise FFIError(ret, "Failed to take ownership of buffer data")

            ret = lib.vaccel_torch_buffer_delete(self._c_obj)
            if ret != 0:
                raise FFIError(ret, "Could not delete buffer")

    @property
    def size(self) -> int:
        """The buffer size.

        Returns:
            The size of the buffer.
        """
        return int(self._c_obj.size)

    @property
    def data(self) -> bytes:
        """The buffer data.

        Returns:
            The data of the buffer.
        """
        if not self._obj.data or self.size == 0:
            return b""
        return ffi.buffer(self._c_obj.data, self.size)[:]

    def __repr__(self):
        return f"<Buffer size={self.size}>"


class TorchMixin:
    """Mixin providing Torch operations for a `Session`.

    This mixin is intended to be used in combination with `BaseSession` and
    should not be instantiated on its own.

    Intended usage:
        class Session(BaseSession, TorchMixin):
            ...
    """

    def torch_jitload_forward(
        self,
        resource: Resource,
        in_tensors: list[Tensor],
        nr_out_tensors: int = 1,
        run_options: Buffer | None = None,
    ) -> list[Tensor]:
        """Performs the Torch jitload forward operation.

        Wraps the `vaccel_torch_jitload_forward()` C operation.

        Args:
            resource: A resource with the model to run.
            in_tensors: The input tensors for the inference.
            nr_out_tensors: The number of output tensors. Defaults to 1.
            run_options: The inference options.

        Returns:
            The output tensors

        Raises:
            RuntimeError: If the `Session` is uninitialized.
            FFIError: If the C operation fails.
        """
        if not self._c_ptr:
            msg = "Uninitialized session"
            raise RuntimeError(msg)

        run_options_ptr = (
            ffi.NULL if run_options is None else run_options._c_ptr
        )
        c_in_tensors = CList.from_ptrs(in_tensors)
        c_out_tensors = CList.from_ptrs([Tensor.empty()] * nr_out_tensors)

        ret = lib.vaccel_torch_jitload_forward(
            self._c_ptr,
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
