# SPDX-License-Identifier: Apache-2.0

"""C type interface for `int` objects."""

from vaccel._c_types.types import CType, to_ctype
from vaccel._libvaccel import ffi


class CInt(CType):
    """Wrapper for `int` objects.

    Provides an interface to interact with the C representation of `int`
    objects.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _value (int): The input int.
        _precision (str): The input C type to represent the int.
        _ctype_str (str): The actual string that is used for the C type.
    """

    def __init__(self, value: int, precision: str = "int"):
        """Initializes a new `CInt` object.

        Args:
            value: The int to be wrapped.
            precision: The C type that will be used to represent the int.
        """
        self._value = int(value)
        self._precision = precision
        # TODO: validate user input  # noqa: FIX002
        self._ctype_str = self._precision
        super().__init__()

    def _init_c_obj(self):
        # TODO: Correctly determine C type (int/int64_t etc.)  # noqa: FIX002
        self._c_obj = ffi.new(f"{self._ctype_str} *", self._value)
        self._c_size = ffi.sizeof(self._ctype_str)

    @property
    def value(self) -> int:
        """Returns the python representation of the data."""
        return int(self._c_ptr_or_raise[0])

    # Comparison Methods
    def __eq__(self, other: "CInt | int"):
        if isinstance(other, CInt):
            return self.value == other.value
        return self.value == other

    def __lt__(self, other: "CInt | int"):
        if isinstance(other, CInt):
            return self.value < other.value
        return self.value < other

    def __le__(self, other: "CInt | int"):
        if isinstance(other, CInt):
            return self.value <= other.value
        return self.value <= other

    def __gt__(self, other: "CInt | int"):
        if isinstance(other, CInt):
            return self.value > other.value
        return self.value > other

    def __ge__(self, other: "CInt | int"):
        if isinstance(other, CInt):
            return self.value >= other.value
        return self.value >= other

    def __ne__(self, other: "CInt | int"):
        if isinstance(other, CInt):
            return self.value != other.value
        return self.value != other

    # Arithmetic Methods
    def __add__(self, other: "CInt | int"):
        if isinstance(other, CInt):
            return CInt(self.value + other.value)
        return CInt(self.value + other)

    def __sub__(self, other: "CInt | int"):
        if isinstance(other, CInt):
            return CInt(self.value - other.value)
        return CInt(self.value - other)

    def __mul__(self, other: "CInt | int"):
        if isinstance(other, CInt):
            return CInt(self.value * other.value)
        return CInt(self.value * other)

    def __truediv__(self, other: "CInt | int"):
        if isinstance(other, CInt):
            return self.value / other.value
        return self.value / other

    def __floordiv__(self, other: "CInt | int"):
        if isinstance(other, CInt):
            return self.value // other.value
        return self.value // other

    def __mod__(self, other: "CInt | int"):
        if isinstance(other, CInt):
            return self.value % other.value
        return self.value % other

    def __pow__(self, other: "CInt | int"):
        if isinstance(other, CInt):
            return self.value**other.value
        return self.value**other

    def __neg__(self):
        return CInt(-self.value)

    def __abs__(self):
        return CInt(abs(self.value))

    # Conversion Methods
    def __int__(self):
        return self.value

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


@to_ctype.register
def _(value: int):
    return CInt(value)
