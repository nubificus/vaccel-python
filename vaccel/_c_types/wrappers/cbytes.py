# SPDX-License-Identifier: Apache-2.0

"""C type interface for byte-like objects."""

from vaccel._c_types.types import CType, to_ctype
from vaccel._libvaccel import ffi


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
    def value(self) -> ffi.CData:
        """Returns the python representation of the data."""
        return self._data

    def _as_c_array(self, c_type: str = "char") -> ffi.CData:
        """Returns a typed C array pointer (e.g., int*, uint8_t*, etc)."""
        return ffi.cast(f"{c_type} *", self._c_obj)

    def to_str(self) -> str:
        """Converts the current C array to a Python string."""
        return ffi.string(self._c_obj).decode()

    def __len__(self):
        return len(self._data)

    def __eq__(self, other: "CBytes | bytes | bytearray | memoryview"):
        if isinstance(other, CBytes):
            return self._data == other._data
        if isinstance(other, (bytes, bytearray, memoryview)):
            return self._data == other
        return NotImplemented

    def __bytes__(self):
        return bytes(self._data)


@to_ctype.register
def _(value: bytes):
    return CBytes(value)


@to_ctype.register
def _(value: bytearray):
    return CBytes(value)
