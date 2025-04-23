"""Interface to the `struct vaccel_arg` C object."""

from typing import Any

from ._c_types import CAny, CType
from ._libvaccel import ffi


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
        return self._c_obj[0]

    @property
    def buf(self) -> Any:
        """Returns the buffer value from the underlying C struct.

        Retrieves the buffer (`buf`) stored in the `struct vaccel_arg` C object.
        If the original data type is a Python built-in type, the buffer is
        converted back to that type.

        Returns:
            The buffer value from the C `struct vaccel_arg`.
        """
        return self._c_data.value

    def __repr__(self):
        if not hasattr(self, "_c_data") or not hasattr(self, "_c_obj"):
            return "<Arg (incomplete)>"
        try:
            _c_ptr = (
                f"0x{int(ffi.cast('uintptr_t', self._c_obj)):x}"
                if self._c_obj
                else "None"
            )
            c_buf = (
                f"0x{int(ffi.cast('uintptr_t', self._c_obj.buf)):x}"
                if self._c_obj.buf
                else "None"
            )
            c_size = self._c_obj.size if self._c_obj.size else 0
        except (AttributeError, TypeError) as e:
            return f"<Arg (error in __repr__): {e}>"
        else:
            return (
                f"<Arg buf={self.buf!r} "
                f"_c_ptr={_c_ptr} "
                f"c_buf={c_buf} "
                f"c_size={c_size}>"
            )
