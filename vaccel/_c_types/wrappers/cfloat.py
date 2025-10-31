# SPDX-License-Identifier: Apache-2.0

"""C type interface for `float` objects."""

from typing import Final

from vaccel._c_types.types import CType, to_ctype
from vaccel._libvaccel import ffi
from vaccel.error import NullPointerError


class CFloat(CType):
    """Wrapper for `float` objects.

    Provides an interface to interact with the C representation of `float`
    objects.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _value (float): The input float.
        _precision (str): The input C type to represent the float.
        _ctype_str (str): The actual string that is used for the C type.
    """

    _SUPPORTED_PRECISIONS: Final[set[str]] = {"float", "double"}

    def __init__(self, value: float, precision: str = "float"):
        """Initializes a new `CFloat` object.

        Args:
            value: The float to be wrapped.
            precision: The C type that will be used to represent the float.
        """
        if precision not in self._SUPPORTED_PRECISIONS:
            supported = ", ".join(str(d) for d in self._SUPPORTED_PRECISIONS)
            msg = f"Unsupported precision: {precision}. Supported: {supported}"
            raise ValueError(msg)
        self._value = float(value)
        self._precision = precision
        self._ctype_str = "float" if precision == "float" else "double"
        super().__init__()

    def _init_c_obj(self):
        # TODO: Correctly determine C type (float/double)  # noqa: FIX002
        self._c_obj = ffi.new(f"{self._ctype_str} *", self._value)
        self._c_size = ffi.sizeof(self._ctype_str)

    @property
    def value(self) -> float:
        """Returns the python representation of the data."""
        return float(self._c_ptr_or_raise[0])

    # Comparison Methods
    def __eq__(self, other: "CFloat | float"):
        if isinstance(other, CFloat):
            return self.value == other.value
        return self.value == other

    def __lt__(self, other: "CFloat | float"):
        if isinstance(other, CFloat):
            return self.value < other.value
        return self.value < other

    def __le__(self, other: "CFloat | float"):
        if isinstance(other, CFloat):
            return self.value <= other.value
        return self.value <= other

    def __gt__(self, other: "CFloat | float"):
        if isinstance(other, CFloat):
            return self.value > other.value
        return self.value > other

    def __ge__(self, other: "CFloat | float"):
        if isinstance(other, CFloat):
            return self.value >= other.value
        return self.value >= other

    def __ne__(self, other: "CFloat | float"):
        if isinstance(other, CFloat):
            return self.value != other.value
        return self.value != other

    # Arithmetic Methods
    def __add__(self, other: "CFloat | float"):
        if isinstance(other, CFloat):
            return CFloat(self.value + other.value)
        return CFloat(self.value + other)

    def __sub__(self, other: "CFloat | float"):
        if isinstance(other, CFloat):
            return CFloat(self.value - other.value)
        return CFloat(self.value - other)

    def __mul__(self, other: "CFloat | float"):
        if isinstance(other, CFloat):
            return CFloat(self.value * other.value)
        return CFloat(self.value * other)

    def __truediv__(self, other: "CFloat | float"):
        if isinstance(other, CFloat):
            return self.value / other.value
        return self.value / other

    def __floordiv__(self, other: "CFloat | float"):
        if isinstance(other, CFloat):
            return self.value // other.value
        return self.value // other

    def __mod__(self, other: "CFloat | float"):
        if isinstance(other, CFloat):
            return self.value % other.value
        return self.value % other

    def __pow__(self, other: "CFloat | float"):
        if isinstance(other, CFloat):
            return self.value**other.value
        return self.value**other

    def __neg__(self):
        return CFloat(-self.value)

    def __abs__(self):
        return CFloat(abs(self.value))

    # Conversion Methods
    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    # String Representation Methods
    def __str__(self):
        return str(self.value)

    # Hashing
    def __hash__(self):
        return hash(self.value)

    # Boolean Context
    def __bool__(self):
        return bool(self.value)

    def __repr__(self):
        try:
            c_ptr = (
                f"0x{int(ffi.cast('uintptr_t', self._c_obj)):x}"
                if self._c_obj != ffi.NULL
                else "NULL"
            )
            value = self.value
            c_type = self._precision
        except (AttributeError, TypeError, NullPointerError):
            return f"<{self.__class__.__name__} (uninitialized or invalid)>"
        return (
            f"<{self.__class__.__name__} value={value!r} "
            f"c_type={c_type} "
            f"at {c_ptr}>"
        )


@to_ctype.register
def _(value: float, *, precision: str | None = "float"):
    return CFloat(value, precision)
