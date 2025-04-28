# SPDX-License-Identifier: Apache-2.0

"""Common error types."""

import errno


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
