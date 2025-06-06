# SPDX-License-Identifier: Apache-2.0

"""Interface to the `struct vaccel_torch_buffer` C object."""

import logging

from vaccel._c_types import CBytes, CType
from vaccel._libvaccel import ffi, lib
from vaccel.error import FFIError, NullPointerError

logger = logging.getLogger(__name__)


class Buffer(CType):
    """Wrapper for the `struct vaccel_torch_buffer` C object.

    Manages the creation and initialization of a C `struct vaccel_torch_buffer`
    and provides access to it through Python properties.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _data (bytes | bytearray): The data of the buffer.
        _c_data (CBytes): The encapsulated buffer data passed to the C struct.
        _c_obj_ptr (ffi.CData): A double pointer to the underlying
            `struct vaccel_torch_buffer` C object.
    """

    def __init__(self, data: bytes | bytearray):
        """Initializes a new `Buffer` object.

        Args:
            data: The buffer data to be passed to the C struct.
        """
        self._data = data
        self._c_data = None
        self._c_obj_ptr = ffi.NULL
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
        return self._c_ptr_or_raise[0]

    def _del_c_obj(self):
        """Deletes the underlying `struct vaccel_torch_buffer` C object.

        Raises:
            FFIError: If buffer deletion fails.
        """
        c_data = ffi.new("void **")
        c_size = ffi.new("size_t *")
        ret = lib.vaccel_torch_buffer_take_data(
            self._c_ptr_or_raise, c_data, c_size
        )
        if ret != 0:
            raise FFIError(ret, "Failed to take ownership of buffer data")

        ret = lib.vaccel_torch_buffer_delete(self._c_ptr_or_raise)
        if ret != 0:
            raise FFIError(ret, "Could not delete buffer")

    def __del__(self):
        try:
            self._del_c_obj()
        except NullPointerError:
            pass
        except FFIError:
            logger.exception("Failed to clean up Buffer")

    @property
    def size(self) -> int:
        """The buffer size.

        Returns:
            The size of the buffer.
        """
        return int(self._c_ptr_or_raise.size)

    @property
    def data(self) -> bytes:
        """The buffer data.

        Returns:
            The data of the buffer.
        """
        if not self._obj.data or self.size == 0:
            return b""
        return ffi.buffer(self._c_ptr_or_raise.data, self.size)[:]

    def __repr__(self):
        try:
            c_ptr = (
                f"0x{int(ffi.cast('uintptr_t', self._c_obj)):x}"
                if self._c_obj != ffi.NULL
                else "NULL"
            )
            size = self.size
        except (AttributeError, TypeError, NullPointerError):
            return f"<{self.__class__.__name__} (uninitialized or invalid)>"
        return f"<{self.__class__.__name__} size={size} at {c_ptr}>"
