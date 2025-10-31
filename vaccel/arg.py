# SPDX-License-Identifier: Apache-2.0

"""Interface to the `struct vaccel_arg` C object."""

import logging
from typing import Any, Final

from ._c_types import CAny, CType
from ._c_types.utils import CEnumBuilder
from ._libvaccel import ffi, lib
from .error import FFIError, NullPointerError, ptr_or_raise

logger = logging.getLogger(__name__)

enum_builder = CEnumBuilder(lib)
ArgType = enum_builder.from_prefix("ArgType", "VACCEL_ARG_")


class ArgTypeMapper:
    """Utility for mapping between `ArgType` and other common types."""

    _NUMERIC_TYPES: Final[set[ArgType]] = {
        ArgType.INT8,
        ArgType.INT8_ARRAY,
        ArgType.INT16,
        ArgType.INT16_ARRAY,
        ArgType.INT32,
        ArgType.INT32_ARRAY,
        ArgType.INT64,
        ArgType.INT64_ARRAY,
        ArgType.UINT8,
        ArgType.UINT8_ARRAY,
        ArgType.UINT16,
        ArgType.UINT16_ARRAY,
        ArgType.UINT32,
        ArgType.UINT32_ARRAY,
        ArgType.UINT64,
        ArgType.UINT64_ARRAY,
        ArgType.FLOAT32,
        ArgType.FLOAT32_ARRAY,
        ArgType.FLOAT64,
    }

    _ARG_TYPE_TO_C: Final[dict[ArgType, str]] = {
        ArgType.INT8: "int8_t",
        ArgType.INT8_ARRAY: "int8_t *",
        ArgType.INT16: "int16_t",
        ArgType.INT16_ARRAY: "int16_t *",
        ArgType.INT32: "int32_t",
        ArgType.INT32_ARRAY: "int32_t *",
        ArgType.INT64: "int64_t",
        ArgType.INT64_ARRAY: "int64_t *",
        ArgType.UINT8: "uint8_t",
        ArgType.UINT8_ARRAY: "uint8_t *",
        ArgType.UINT16: "uint16_t",
        ArgType.UINT16_ARRAY: "uint16_t *",
        ArgType.UINT32: "uint32_t",
        ArgType.UINT32_ARRAY: "uint32_t *",
        ArgType.UINT64: "uint64_t",
        ArgType.UINT64_ARRAY: "uint64_t *",
        ArgType.FLOAT32: "float",
        ArgType.FLOAT32_ARRAY: "float *",
        ArgType.FLOAT64: "double",
        ArgType.FLOAT64_ARRAY: "double *",
        ArgType.BOOL: "bool",
        ArgType.BOOL_ARRAY: "bool *",
        ArgType.CHAR: "char",
        ArgType.CHAR_ARRAY: "char *",
        ArgType.UCHAR: "unsigned char",
        ArgType.UCHAR_ARRAY: "unsigned char *",
        ArgType.STRING: "char *",
        ArgType.BUFFER: "void *",
    }

    @classmethod
    def is_numeric(cls, arg_type: ArgType) -> bool:
        """Checks if the arg type represents a numeric type.

        Args:
            arg_type: The arg type value.

        Returns:
            True if the arg type represents a numeric type.
        """
        return arg_type in cls._NUMERIC_TYPES

    @classmethod
    def type_to_c_type(cls, arg_type: ArgType) -> str:
        """Converts an `ArgType` to a C type string.

        Args:
            arg_type: The arg type value.

        Returns:
            A corresponding C type as a string (e.g., "float", "int64_t").

        Raises:
            ValueError: If the `arg_type` value is not supported.
        """
        if arg_type not in cls._ARG_TYPE_TO_C:
            supported = ", ".join(str(d) for d in cls._ARG_TYPE_TO_C)
            msg = f"Unsupported ArgType: {arg_type}. Supported: {supported}"
            raise ValueError(msg)
        return cls._ARG_TYPE_TO_C[arg_type]


class Arg(CType):
    """Wrapper for the `vaccel_arg` C struct.

    Manages the creation and initialization of a C `struct vaccel_arg` object
    and provides access to it through Python properties.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _c_data (CAny): The encapsulated C data that is passed to the C struct.
        _c_obj_ptr (ffi.CData): A double pointer to the underlying
            `struct vaccel_arg` C object.
        type_ (ArgType): The type of the arg.
        custom_type_id (int): The user-specified type ID of the arg if the type
            is `ArgType.CUSTOM`.
    """

    def __init__(
        self, data: Any, type_: ArgType = ArgType.RAW, custom_type_id: int = 0
    ):
        """Initializes a new `Arg` object.

        Args:
            data: The input data to be passed to the C struct.
            type_: The type of the arg.
            custom_type_id: The user-specified type ID of the arg if the type is
                `ArgType.CUSTOM`.
        """
        if ArgType != ArgType.RAW and ArgTypeMapper.is_numeric(type_):
            precision = ArgTypeMapper.type_to_c_type(type_)
            self._c_data = CAny(data, precision=precision)
        else:
            self._c_data = CAny(data)
        self._c_obj_ptr = ffi.NULL
        self._type = type_
        self._custom_type_id = custom_type_id
        super().__init__()

    def _init_c_obj(self):
        """Initializes the underlying `struct vaccel_arg` C object."""
        self._c_obj_ptr = ffi.new("struct vaccel_arg **")
        ret = lib.vaccel_arg_from_buf(
            self._c_obj_ptr,
            self._c_data._c_ptr,
            self._c_data.c_size,
            self._type,
            self._custom_type_id,
        )
        if ret != 0:
            raise FFIError(ret, "Could not initialize arg")

        self._c_obj = self._c_obj_ptr[0]
        self._c_size = ffi.sizeof("struct vaccel_arg")

    @property
    def value(self) -> ffi.CData:
        """Returns the value of the underlying C struct.

        Returns:
            The dereferenced 'struct vaccel_arg`
        """
        return self._c_ptr_or_raise[0]

    def _del_c_obj(self):
        """Deletes the underlying `struct vaccel_arg` C object.

        Raises:
            FFIError: If arg deletion fails.
        """
        ret = lib.vaccel_arg_delete(self._c_ptr_or_raise)
        if ret != 0:
            raise FFIError(ret, "Could not delete arg")

    def __del__(self):
        try:
            self._del_c_obj()
        except NullPointerError:
            pass
        except FFIError:
            logger.exception("Failed to clean up Arg")

    @property
    def buf(self) -> Any:
        """Returns the buffer value from the underlying C struct.

        Retrieves the buffer (`buf`) stored in the `struct vaccel_arg` C object.
        If the original data type is a Python built-in type, the buffer is
        converted back to that type.

        Returns:
            The buffer value from the C `struct vaccel_arg`.
        """
        return ptr_or_raise(
            self._c_data, f"{self.__class__.__name__}._c_data"
        ).value

    @property
    def type(self) -> ArgType:
        """The arg type.

        Returns:
            The type of the arg.
        """
        return ArgType(self._c_ptr_or_raise.type)

    def __repr__(self):
        try:
            _c_ptr = (
                f"0x{int(ffi.cast('uintptr_t', self._c_obj)):x}"
                if self._c_obj != ffi.NULL
                else "NULL"
            )
            size = self._c_obj.size if self._c_obj != ffi.NULL else 0
            type_ = self.type
            type_name = getattr(type_, "name", repr(type_))
        except (AttributeError, TypeError, NullPointerError):
            return f"<{self.__class__.__name__} (uninitialized or invalid)>"
        return (
            f"<{self.__class__.__name__} "
            f"size={size} "
            f"type={type_name} "
            f"at {_c_ptr}>"
        )
