# SPDX-License-Identifier: Apache-2.0

"""C type interface for `str` objects."""

from pathlib import Path

from vaccel._c_types.types import CType, to_ctype
from vaccel._libvaccel import ffi
from vaccel.error import NullPointerError


class CStr(CType):
    """Wrapper for `str` objects.

    Provides an interface to interact with the C representation of `str`
    objects.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _value (str): The input str.
    """

    def __init__(self, value: str):
        """Initializes a new `CStr` object.

        Args:
            value: The str to be wrapped.
        """
        self._value = str(value)
        super().__init__()

    def _init_c_obj(self):
        self._c_obj = ffi.new("char[]", self._value.encode())
        self._c_size = ffi.sizeof(self._c_obj)

    @property
    def value(self) -> str:
        """Returns the python representation of the data."""
        return self.as_str()

    @classmethod
    def from_c_obj(cls, c_obj: ffi.CData) -> "CStr":
        """Initializes a new `CStr` object from a C string pointer.

        Args:
            c_obj: A pointer to `char` or a `char` array.

        Returns:
            A new `CStr` object
        """
        type_str = ffi.getctype(ffi.typeof(c_obj))
        if type_str not in ("char *", "char[]"):
            msg = f"Expected 'char *' or 'char[]', got '{type_str}'"
            raise TypeError(msg)

        inst = cls.__new__(cls)
        inst._c_obj = c_obj
        inst._c_size = ffi.sizeof(inst._c_obj)
        return inst

    def as_bytes(self) -> bytes:
        """Returns the string as a Python bytes object (same as C string)."""
        return ffi.string(self._c_ptr_or_raise)

    def as_str(self) -> str:
        """Returns the Python string, ensuring it matches the C string."""
        return ffi.string(self._c_ptr_or_raise).decode()

    def update(self, new_str: str | bytes):
        """Modifies the string and updates the C representation."""
        if isinstance(new_str, bytes):
            new_str = new_str.decode("utf-8")
        elif not isinstance(new_str, str):
            msg = "CStr update only accepts str or bytes objects"
            raise TypeError(msg)

        if new_str != self._value:
            self._value = new_str
            self._init_c_obj()

    def __len__(self):
        return len(self._value)

    def __eq__(self, other: "CStr | str"):
        if isinstance(other, CStr):
            return self._value == other._value
        if isinstance(other, str):
            return self._value == other
        return NotImplemented

    __hash__ = None

    def __repr__(self):
        try:
            c_ptr = (
                f"0x{int(ffi.cast('uintptr_t', self._c_obj)):x}"
                if self._c_obj != ffi.NULL
                else "NULL"
            )
            value = self.value
        except (AttributeError, TypeError, NullPointerError):
            return f"<{self.__class__.__name__} (uninitialized or invalid)>"
        return f"<{self.__class__.__name__} value={value!r} at {c_ptr}>"


@to_ctype.register
def _(value: str, *, precision: str | None = None):
    _ = precision
    return CStr(value)


@to_ctype.register
def _(value: Path, *, precision: str | None = None):
    _ = precision
    return CStr(value)
