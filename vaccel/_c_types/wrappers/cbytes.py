# SPDX-License-Identifier: Apache-2.0

"""C type interface for byte-like objects."""

from vaccel._c_types.types import CType, to_ctype
from vaccel._libvaccel import ffi
from vaccel.error import NullPointerError


class CBytes(CType):
    """Wrapper for byte-like objects.

    Provides an interface to interact with the C representation of byte-like
    objects.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _data (bytes | bytearray | memoryview): The input byte-like data.
    """

    def __init__(self, data: bytes | bytearray | memoryview):
        """Initializes a new `CBytes` object.

        Args:
            data: The data to be wrapped.
        """
        if not isinstance(data, (bytes, bytearray, memoryview)):
            msg = "CBytes only accepts Python bytes-like objects"
            raise TypeError(msg)
        self._data = data
        super().__init__()

    def _init_c_obj(self):
        # NOTE: `bytes` is immutable so the buffer must not be modified
        self._c_obj = ffi.from_buffer(self._data)
        self._c_size = len(self._c_obj)

    @property
    def value(self) -> bytes | bytearray | memoryview:
        """Returns the python representation of the data."""
        return self._data

    @classmethod
    def from_c_obj(cls, c_obj: ffi.CData, c_size: int) -> "CBytes":
        """Initializes a new `CBytes` object from a C string pointer.

        Args:
            c_obj: A pointer to a C object or array.
            c_size: The size of the C object or array.

        Returns:
            A new `CBytes` object

        Raises:
            TypeError: If `c_obj` is not a C pointer or array.
        """
        type_str = ffi.getctype(ffi.typeof(c_obj))
        if not type_str.endswith((" *", "[]")):
            msg = f"Expected a pointer or array type, got '{type_str}'"
            raise TypeError(msg)

        inst = cls.__new__(cls)
        inst._c_obj = c_obj
        inst._c_size = c_size
        inst._data = memoryview(ffi.buffer(inst._c_obj, c_size))
        return inst

    def _as_c_array(self, c_type: str = "char") -> ffi.CData:
        """Returns a typed C array pointer (e.g., int*, uint8_t*, etc)."""
        return ffi.cast(f"{c_type} *", self._c_ptr_or_raise)

    def to_str(self) -> str:
        """Converts the current C array to a Python string."""
        return ffi.string(self._c_ptr_or_raise).decode()

    def __len__(self):
        return len(self._data)

    def __eq__(self, other: "CBytes | bytes | bytearray | memoryview"):
        if isinstance(other, CBytes):
            return self._data == other._data
        if isinstance(other, (bytes, bytearray, memoryview)):
            return self._data == other
        return NotImplemented

    __hash__ = None

    def __bytes__(self):
        return bytes(self._data)

    def __repr__(self):
        try:
            c_ptr = (
                f"0x{int(ffi.cast('uintptr_t', self._c_obj)):x}"
                if self._c_obj != ffi.NULL
                else "NULL"
            )
            size = len(self)
        except (AttributeError, TypeError, NullPointerError):
            return f"<{self.__class__.__name__} (uninitialized or invalid)>"
        return f"<{self.__class__.__name__} size={size} at {c_ptr}>"


@to_ctype.register
def _(value: bytes, *, precision: str | None = None):
    _ = precision
    return CBytes(value)


@to_ctype.register
def _(value: bytearray, *, precision: str | None = None):
    _ = precision
    return CBytes(value)
