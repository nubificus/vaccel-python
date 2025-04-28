# SPDX-License-Identifier: Apache-2.0

"""Common interfaces for C types."""

from abc import ABC, abstractmethod
from functools import singledispatch
from typing import Any


class CType(ABC):
    """Abstract base class for defining C data types.

    Attributes:
        _c_obj (ffi.CData): A pointer to the underlying C object.
        _c_size (int): The size of the underlying C object.
    """

    def __init__(self):
        self._c_obj = None
        self._c_size = None
        self._init_c_obj()

    @abstractmethod
    def _init_c_obj(self):
        """Initializes the C object."""

    @property
    def _c_ptr(self):
        """Returns the C pointer representation of the object."""
        return self._c_obj

    @property
    def c_size(self) -> int:
        """Returns the size of the object in bytes."""
        return self._c_size

    @property
    @abstractmethod
    def value(self):
        """Returns the Python value representing the C object."""

    # TODO: Add from_c_obj  # noqa: FIX002

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} "
            f"value={self.value!r} size={self.c_size}>"
        )


class CAny(CType):
    """Generic adapter for wrapping C objects.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _wrapped (CType): The wrapped C object.
    """

    def __init__(self, obj: Any):
        """Initializes a new `CAny` object.

        Args:
            obj: The python object to be wrapped as a C type.
        """
        self._wrapped = to_ctype(obj)

    def _init_c_obj(self):
        msg = "CAny is a generic adapter, not meant for initialization."
        raise NotImplementedError(msg)

    @property
    def _c_ptr(self):
        """Return the C pointer of the wrapped object."""
        return self._wrapped._c_ptr

    @property
    def c_size(self) -> int:
        """Return the size of the wrapped object in bytes."""
        return self._wrapped.c_size

    @property
    def value(self):
        """Return the Python value of the wrapped C object."""
        return self._wrapped.value

    def __repr__(self):
        return f"<CAny wrapping {self._wrapped!r}>"


@singledispatch
def to_ctype(value: Any):
    msg = f"No CType wrapper registered for {type(value)}"
    raise TypeError(msg)


@to_ctype.register
def _(value: CType):
    return value
