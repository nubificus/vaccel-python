# SPDX-License-Identifier: Apache-2.0

"""Interface to the `struct vaccel_torch_tensor` C object."""

import logging
from typing import Any, Final

from vaccel._c_types import CBytes, CNumpyArray, CType
from vaccel._c_types.utils import CEnumBuilder
from vaccel._libvaccel import ffi, lib
from vaccel.error import FFIError, NullPointerError

try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import torch

    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

logger = logging.getLogger(__name__)

enum_builder = CEnumBuilder(lib)
TensorType = enum_builder.from_prefix("TensorType", "VACCEL_TORCH_")


class TensorTypeMapper:
    """Utility for mapping between `TensorType` and other common types."""

    _TENSOR_TYPE_TO_C: Final[dict[TensorType, (str, int)]] = {
        TensorType.BYTE: ("uint8_t", ffi.sizeof("uint8_t")),
        TensorType.CHAR: ("int8_t", ffi.sizeof("int8_t")),
        TensorType.SHORT: ("int16_t", ffi.sizeof("int16_t")),
        TensorType.INT: ("int32_t", ffi.sizeof("int32_t")),
        TensorType.LONG: ("int64_t", ffi.sizeof("int64_t")),
        TensorType.FLOAT: ("float", ffi.sizeof("float")),
    }

    @classmethod
    def type_to_c_type(cls, tensor_type: TensorType) -> str:
        """Converts a `TensorType` to a C type string.

        Args:
            tensor_type: The tensor type value.

        Returns:
            A corresponding C type as a string (e.g., "float", "int64_t").

        Raises:
            ValueError: If the `tensor_type` value is not supported.
        """
        if tensor_type not in cls._TENSOR_TYPE_TO_C:
            supported = ", ".join(str(d) for d in cls._TENSOR_TYPE_TO_C)
            msg = (
                f"Unsupported TensorType: {tensor_type}. Supported: {supported}"
            )
            raise ValueError(msg)
        return cls._TENSOR_TYPE_TO_C[tensor_type][0]

    @classmethod
    def type_to_c_size(cls, tensor_type: TensorType) -> int:
        """Converts a `TensorType` to a C type size (in bytes).

        Args:
            tensor_type: The tensor type value.

        Returns:
            A corresponding C type size in bytes.

        Raises:
            ValueError: If the `tensor_type` value is not supported.
        """
        if tensor_type not in cls._TENSOR_TYPE_TO_C:
            supported = ", ".join(str(d) for d in cls._TENSOR_TYPE_TO_C)
            msg = (
                f"Unsupported TensorType: {tensor_type}. Supported: {supported}"
            )
            raise ValueError(msg)
        return cls._TENSOR_TYPE_TO_C[tensor_type][1]

    if HAS_NUMPY:
        _NUMPY_TO_TENSOR_TYPE = {
            np.dtype("uint8"): TensorType.BYTE,
            np.dtype("int8"): TensorType.CHAR,
            np.dtype("int16"): TensorType.SHORT,
            np.dtype("int32"): TensorType.INT,
            np.dtype("int64"): TensorType.LONG,
            np.dtype("float32"): TensorType.FLOAT,
        }
        _TENSOR_TYPE_TO_NUMPY = {v: k for k, v in _NUMPY_TO_TENSOR_TYPE.items()}

    @classmethod
    def type_from_numpy(cls, dtype: "np.dtype") -> TensorType:
        """Converts a NumPy `dtype` to `TensorType`.

        Args:
            dtype: A NumPy `dtype` object or something convertible to
                `np.dtype`.

        Returns:
            A corresponding tensor type value.

        Raises:
            NotImplementedError: If NumPy is not installed.
            ValueError: If the `dtype` value is not supported.
        """
        if not HAS_NUMPY:
            msg = "NumPy is not available"
            raise NotImplementedError(msg)

        dtype = np.dtype(dtype)
        if dtype not in cls._NUMPY_TO_TENSOR_TYPE:
            supported = ", ".join(str(d) for d in cls._NUMPY_TO_TENSOR_TYPE)
            msg = f"Unsupported NumPy dtype: {dtype}. Supported: {supported}"
            raise ValueError(msg)

        return cls._NUMPY_TO_TENSOR_TYPE[dtype]

    @classmethod
    def type_to_numpy(cls, ttype: TensorType) -> "np.dtype":
        """Converts a `TensorType` to a NumPy `dtype`.

        Args:
            ttype: A `TensorType` enum value.

        Returns:
            A corresponding NumPy `dtype` object.

        Raises:
            NotImplementedError: If NumPy is not installed.
            ValueError: If the `TensorType` value is not supported.
        """
        if not HAS_NUMPY:
            msg = "NumPy is not available"
            raise NotImplementedError(msg)

        if ttype not in cls._TENSOR_TYPE_TO_NUMPY:
            supported = ", ".join(str(t) for t in cls._TENSOR_TYPE_TO_NUMPY)
            msg = f"Unsupported TensorType: {ttype}. Supported: {supported}"
            raise ValueError(msg)

        return cls._TENSOR_TYPE_TO_NUMPY[ttype]

    if HAS_TORCH:
        _TORCH_TO_TENSOR_TYPE = {
            torch.uint8: TensorType.BYTE,
            torch.int8: TensorType.CHAR,
            torch.int16: TensorType.SHORT,
            torch.int32: TensorType.INT,
            torch.int64: TensorType.LONG,
            torch.float32: TensorType.FLOAT,
        }
        _TENSOR_TYPE_TO_TORCH = {v: k for k, v in _TORCH_TO_TENSOR_TYPE.items()}

    @classmethod
    def type_from_torch(cls, dtype: "torch.dtype") -> TensorType:
        """Converts a PyTorch `dtype` to `TensorType`.

        Args:
            dtype: A PyTorch `dtype` object.

        Returns:
            A corresponding tensor type value.

        Raises:
            NotImplementedError: If PyTorch is not installed.
            ValueError: If the `dtype` value is not supported.
        """
        if not HAS_TORCH:
            msg = "PyTorch is not available"
            raise NotImplementedError(msg)

        if dtype not in cls._TORCH_TO_TENSOR_TYPE:
            supported = ", ".join(str(d) for d in cls._TORCH_TO_TENSOR_TYPE)
            msg = f"Unsupported PyTorch dtype: {dtype}. Supported: {supported}"
            raise ValueError(msg)

        return cls._TORCH_TO_TENSOR_TYPE[dtype]

    @classmethod
    def type_to_torch(cls, ttype: TensorType) -> "torch.dtype":
        """Converts a `TensorType` to a PyTorch `dtype`.

        Args:
            ttype: A `TensorType` enum value.

        Returns:
            A corresponding PyTorch `dtype` object.

        Raises:
            NotImplementedError: If PyTorch is not installed.
            ValueError: If the `TensorType` value is not supported.
        """
        if not HAS_TORCH:
            msg = "PyTorch is not available"
            raise NotImplementedError(msg)

        if ttype not in cls._TENSOR_TYPE_TO_TORCH:
            supported = ", ".join(str(t) for t in cls._TENSOR_TYPE_TO_TORCH)
            msg = f"Unsupported TensorType: {ttype}. Supported: {supported}"
            raise ValueError(msg)

        return cls._TENSOR_TYPE_TO_TORCH[ttype]


class Tensor(CType):
    """Wrapper for the `struct vaccel_torch_tensor` C object.

    Manages the creation and initialization of a C `struct vaccel_torch_tensor`
    and provides access to it through Python properties.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _dims (list[int] | None): The dims of the tensor; None if empty.
        _data (list[Any] | bytes | bytearray | np.ndarray | None): The data of
            the tensor; None if empty.
        _data_type (TensorType | None): The type of the tensor; None if empty.
        _c_data (CBytes | CNumpyArray | None): The encapsulated buffer data
            passed to the C struct.
        _c_obj_ptr (ffi.CData): A double pointer to the underlying
            `struct vaccel_torch_tensor` C object.
        _c_obj_data (ffi.CData): A pointer to the data of the underlying
            `struct vaccel_torch_tensor` C object.
    """

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
        self._c_data = None
        self._c_obj_ptr = ffi.NULL
        self._c_obj_data = ffi.NULL
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

        if self._c_obj_data != ffi.NULL:
            data_size = (
                self._c_data.c_size if self._c_data else len(self._c_obj_data)
            )
        else:
            c_type_str = TensorTypeMapper.type_to_c_type(self._data_type)
            self._c_obj_data = ffi.new(
                f"{c_type_str}[{len(self._data)}]", self._data
            )
            c_type_size = TensorTypeMapper.type_to_c_size(self._data_type)
            data_size = c_type_size * len(self._data)

        ret = lib.vaccel_torch_tensor_set_data(
            self._c_obj, self._c_obj_data, data_size
        )
        if ret != 0:
            raise FFIError(ret, "Could not set tensor data")

    @property
    def value(self) -> ffi.CData:
        """Returns the value of the underlying C struct.

        Returns:
            The dereferenced 'struct vaccel_torch_tensor`
        """
        return self._c_ptr_or_raise[0]

    def _del_c_obj(self):
        """Deletes the underlying `struct vaccel_torch_tensor` C object.

        Raises:
            FFIError: If tensor deletion fails.
        """
        ret = lib.vaccel_torch_tensor_delete(self._c_ptr_or_raise)
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
    def shape(self) -> list[int]:
        """The tensor shape.

        Alias of `Tensor.dims`.

        Returns:
            The shape of the tensor.
        """
        return self.dims

    @property
    def data(self) -> list:
        """The tensor data.

        Returns:
            The data of the tensor.
        """
        c_type_str = TensorTypeMapper.type_to_c_type(self.data_type)
        if self._c_data:
            typed_c_data = self._c_data._as_c_array(c_type_str)
        else:
            typed_c_data = ffi.cast(
                f"{c_type_str} *", self._c_ptr_or_raise.data
            )
        c_type_size = TensorTypeMapper.type_to_c_size(self.data_type)
        return ffi.unpack(
            typed_c_data, int(self._c_ptr_or_raise.size / c_type_size)
        )

    def as_bytelike(self) -> bytes | bytearray | memoryview:
        """Returns the tensor data buffer as a byte-like object.

        Returns:
            The data of the tensor as a byte-like object.
        """
        if self._c_data is not None:
            if isinstance(self._c_data, CBytes):
                return self._c_data.value
            return self._c_data.as_memoryview()
        return CBytes.from_c_obj(
            self._c_ptr_or_raise.data, self._c_ptr_or_raise.size
        ).value

    def as_memoryview(self) -> memoryview:
        """Returns the tensor data buffer as memoryview.

        Returns:
            The data of the tensor as memoryview.
        """
        data = self.as_bytelike()
        return data if isinstance(data, memoryview) else memoryview(data)

    def to_bytes(self) -> bytes:
        """Returns the tensor data buffer as bytes.

        Returns:
            The data of the tensor as bytes.
        """
        data = self.as_bytelike()
        return data if isinstance(data, bytes) else bytes(data)

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
            c_obj: A pointer to a `struct vaccel_torch_tensor` C object.

        Returns:
            A new `Tensor` object
        """
        type_str = ffi.getctype(ffi.typeof(c_obj))
        if type_str != "struct vaccel_torch_tensor *":
            msg = f"Expected 'struct vaccel_torch_tensor *', got '{type_str}'"
            raise TypeError(msg)

        inst = cls.__new__(cls)
        inst._dims = None
        inst._data = None
        inst._data_type = None
        inst._c_data = None
        inst._c_obj_ptr = ffi.NULL
        inst._c_obj_data = ffi.NULL
        inst._c_obj = c_obj
        inst._c_size = ffi.sizeof(inst._c_obj)
        return inst

    @classmethod
    def from_buffer(
        cls,
        dims: list[int],
        data_type: TensorType,
        data: bytes | bytearray | memoryview,
    ) -> "Tensor":
        """Initializes a new `Tensor` object from byte-like data.

        Args:
            dims: The dims to be passed to the C struct.
            data_type: The data_type to be passed to the C struct.
            data: The data to be passed to the C struct.

        Returns:
            A new `Tensor` object
        """
        inst = cls.__new__(cls)
        inst._dims = dims
        inst._data = data
        inst._data_type = data_type
        inst._c_data = CBytes(inst._data)
        inst._c_obj_ptr = ffi.NULL
        inst._c_obj_data = inst._c_data._c_ptr
        super().__init__(inst)
        return inst

    @classmethod
    def empty(cls) -> "Tensor":
        """Initializes a new empty `Tensor` object.

        The object has a NULL pointer in place of the C struct.

        Returns:
            A new `Tensor` object
        """
        inst = cls.__new__(cls)
        inst._dims = None
        inst._data = None
        inst._data_type = None
        inst._c_data = None
        inst._c_obj_ptr = ffi.new("struct vaccel_torch_tensor **")
        inst._c_obj = inst._c_obj_ptr[0]
        inst._c_obj_ptr[0] = ffi.NULL
        inst._c_size = ffi.sizeof("struct vaccel_torch_tensor *")
        return inst

    def __repr__(self):
        try:
            c_ptr = (
                f"0x{int(ffi.cast('uintptr_t', self._c_obj)):x}"
                if self._c_obj != ffi.NULL
                else "NULL"
            )
            dims = self.dims
            data_type = self.data_type.name
        except (AttributeError, TypeError, NullPointerError):
            return f"<{self.__class__.__name__} (uninitialized or invalid)>"
        return (
            f"<{self.__class__.__name__} dims={dims} "
            f"data_type={data_type} "
            f"at {c_ptr}>"
        )

    @classmethod
    def from_numpy(cls, data: "np.ndarray") -> "Tensor":
        """Initializes a new `Tensor` object from a NumPy array.

        Args:
            data: The NumPy array containing the tensor data.

        Returns:
            A new `Tensor` object

        Raises:
            NotImplementedError: If NumPy is not installed.
        """
        if not HAS_NUMPY:
            msg = "NumPy is not available"
            raise NotImplementedError(msg)

        inst = cls.__new__(cls)
        inst._dims = list(data.shape)
        inst._data = data
        inst._data_type = TensorTypeMapper.type_from_numpy(inst._data.dtype)
        inst._c_data = CNumpyArray(inst._data)
        inst._c_obj_ptr = ffi.NULL
        inst._c_obj_data = inst._c_data._c_ptr
        super().__init__(inst)
        return inst

    def as_numpy(self) -> "np.ndarray":
        """Returns the tensor data buffer as a NumPy array.

        Returns:
            The data of the tensor as a NumPy array.
        """
        if not HAS_NUMPY:
            msg = "NumPy is not available"
            raise NotImplementedError(msg)

        if isinstance(self._c_data, CNumpyArray):
            return self._c_data.value

        dtype = TensorTypeMapper.type_to_numpy(self.data_type)
        return CNumpyArray.from_c_obj(
            self._c_ptr_or_raise.data,
            self._c_ptr_or_raise.size,
            self.shape,
            dtype,
        ).value

    @classmethod
    def from_torch(cls, data: "torch.Tensor") -> "Tensor":
        """Initializes a new `Tensor` object from a PyTorch tensor.

        Args:
            data: The PyTorch tensor containing the tensor data.

        Returns:
            A new `Tensor` object

        Raises:
            NotImplementedError: If PyTorch is not installed.
        """
        if not HAS_TORCH:
            msg = "PyTorch is not available"
            raise NotImplementedError(msg)

        inst = cls.__new__(cls)
        inst._dims = list(data.shape)
        inst._data = data.contiguous().cpu()
        inst._data_type = TensorTypeMapper.type_from_torch(inst._data.dtype)
        inst._c_obj_ptr = ffi.NULL
        data_ptr_int = inst._data.untyped_storage().data_ptr()
        data_ptr = ffi.cast("void *", data_ptr_int)
        data_size = inst._data.untyped_storage().nbytes()
        inst._c_data = CBytes.from_c_obj(data_ptr, data_size)
        inst._c_obj_data = inst._c_data._c_ptr
        super().__init__(inst)
        return inst

    def as_torch(self) -> "torch.Tensor":
        """Returns the tensor as a PyTorch tensor.

        Returns:
            The tensor as a PyTorch tensor.

        Raises:
            NotImplementedError: If PyTorch is not installed.
        """
        if not HAS_TORCH:
            msg = "PyTorch is not available"
            raise NotImplementedError(msg)

        if isinstance(self._data, torch.Tensor):
            return self._data

        dtype = TensorTypeMapper.type_to_torch(self.data_type)
        buf = ffi.buffer(self._c_ptr_or_raise.data, self._c_ptr_or_raise.size)

        return torch.frombuffer(buf, dtype=dtype).reshape(self.shape)
