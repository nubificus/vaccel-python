# SPDX-License-Identifier: Apache-2.0

"""Common error types."""

import errno

from ._libvaccel import ffi


class FFIError(RuntimeError):
    """Exception raised when a vAccel runtime error occurs.

    Attributes:
        code (int): The error code associated with the runtime error.
        message (str): A message describing the error.
    """

    def __init__(self, error_code: int, message: str):
        """Initializes a new `FFIError` object.

        Args:
            error_code: The code associated with the runtime error.
            message: A message describing the error.
        """
        self.code = error_code
        self.message = message

    def __str__(self):
        return (
            f"[errno {self.code}] {errno.errorcode[self.code]}: {self.message}"
        )


class NullPointerError(RuntimeError):
    """Exception raised when a C pointer is unexpectedly NULL."""

    def __init__(self, context: str):
        """Initializes a new `NullPointerError` object.

        Args:
            context: Name or description of the variable that was NULL.
        """
        super().__init__(f"Unexpected NULL pointer encountered in {context}")


def ptr_or_raise(ptr: ffi.CData, context: str = "pointer") -> ffi.CData:
    """Validates a C pointer and raises an error if it is NULL.

    Args:
        ptr: A CFFI pointer to validate.
        context: A description of the pointer or its role for debugging
            purposes.

    Returns:
        The original `ptr` if it is not NULL.

    Raises:
        NullPointerError: If `ptr` is NULL.
    """
    if ptr == ffi.NULL:
        raise NullPointerError(context)
    return ptr
