# SPDX-License-Identifier: Apache-2.0

"""Interface to the `struct vaccel_tf_status` C object."""

import logging

from vaccel._c_types import CStr, CType
from vaccel._libvaccel import ffi, lib
from vaccel.error import FFIError, NullPointerError

logger = logging.getLogger(__name__)


class Status(CType):
    """Wrapper for the `struct vaccel_tf_status` C object.

    Manages the creation and initialization of a C `struct vaccel_tf_status` and
    provides access to it through Python properties.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _error_code (int): The status's error code.
        _message (str): The status' message.
        _c_obj_ptr (ffi.CData): A double pointer to the underlying
            `struct vaccel_tf_status` C object.
    """

    def __init__(self, error_code: int = 0, message: str = ""):
        """Initializes a new `Status` object.

        Args:
            error_code: The error code to be passed to the C struct. Defaults
                to 0.
            message: The message to be passed to the C struct. Defaults to "".
        """
        self._error_code = error_code
        self._message = message
        self._c_obj_ptr = ffi.NULL
        super().__init__()

    def _init_c_obj(self):
        """Initializes the underlying C `struct vaccel_tf_status` object.

        Raises:
            FFIError: If status initialization fails.
        """
        self._c_obj_ptr = ffi.new("struct vaccel_tf_status **")
        ret = lib.vaccel_tf_status_new(
            self._c_obj_ptr, self._error_code, self._message.encode()
        )
        if ret != 0:
            raise FFIError(ret, "Could not initialize status")

        self._c_obj = self._c_obj_ptr[0]
        self._c_size = ffi.sizeof("struct vaccel_tf_status")

    @property
    def value(self) -> ffi.CData:
        """Returns the value of the underlying C struct.

        Returns:
            The dereferenced 'struct vaccel_tf_status`
        """
        return self._c_ptr_or_raise[0]

    def _del_c_obj(self):
        """Deletes the underlying `struct vaccel_tf_status` C object.

        Raises:
            FFIError: If status deletion fails.
        """
        ret = lib.vaccel_tf_status_delete(self._c_ptr_or_raise)
        if ret != 0:
            raise FFIError(ret, "Could not delete status")

    def __del__(self):
        try:
            self._del_c_obj()
        except NullPointerError:
            pass
        except FFIError:
            logger.exception("Failed to clean up Status")

    @property
    def code(self) -> int:
        """The status error code.

        Returns:
            The code of the status.
        """
        return int(self._c_ptr_or_raise.error_code)

    @property
    def message(self) -> str:
        """The status message.

        Returns:
            The message of the status.
        """
        return CStr.from_c_obj(self._c_ptr_or_raise.message).value

    def __repr__(self):
        try:
            c_ptr = (
                f"0x{int(ffi.cast('uintptr_t', self._c_obj)):x}"
                if self._c_obj != ffi.NULL
                else "NULL"
            )
            code = self.code
            message = self.message
        except (AttributeError, TypeError, NullPointerError):
            return f"<{self.__class__.__name__} (uninitialized or invalid)>"
        return (
            f"<{self.__class__.__name__} code={code} "
            f"message={message!r} "
            f"at {c_ptr}>"
        )
