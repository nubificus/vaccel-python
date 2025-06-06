# SPDX-License-Identifier: Apache-2.0

"""Interface to the `struct vaccel_arg` C object."""

from typing import Any

from ._c_types import CAny, CType
from ._libvaccel import ffi
from .error import NullPointerError, ptr_or_raise


class Arg(CType):
    """Wrapper for the `vaccel_arg` C struct.

    Manages the creation and initialization of a C `struct vaccel_arg` object
    and provides access to it through Python properties.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _c_data (CAny): The encapsulated C data that is passed to the C struct.
    """

    def __init__(self, data: Any):
        """Initializes a new `Arg` object.

        Args:
            data: The input data to be passed to the C struct.
        """
        self._c_data = CAny(data)
        super().__init__()

    def _init_c_obj(self):
        """Initializes the underlying `struct vaccel_arg` C object."""
        c_data = self._c_data
        self._c_obj = ffi.new("struct vaccel_arg *")
        self._c_obj.size = c_data.c_size
        self._c_obj.buf = c_data._c_ptr

    @property
    def value(self) -> ffi.CData:
        """Returns the value of the underlying C struct.

        Returns:
            The dereferenced 'struct vaccel_arg`
        """
        return self._c_ptr_or_raise[0]

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

    def __repr__(self):
        try:
            _c_ptr = (
                f"0x{int(ffi.cast('uintptr_t', self._c_obj)):x}"
                if self._c_obj != ffi.NULL
                else "NULL"
            )
            size = self._c_obj.size if self._c_obj != ffi.NULL else 0
        except (AttributeError, TypeError, NullPointerError):
            return f"<{self.__class__.__name__} (uninitialized or invalid)>"
        return f"<{self.__class__.__name__} size={size} at {_c_ptr}>"
