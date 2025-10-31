# SPDX-License-Identifier: Apache-2.0

"""C type interface for NumPy array objects."""

from vaccel._c_types.types import CType, to_ctype
from vaccel._libvaccel import ffi

try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


class CNumpyArray(CType):
    """Wrapper for NumPy array objects.

    Provides an interface to interact with the C representation of NumPy array
    objects.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _data (np.array): The input NumPy array.
    """

    def __init__(self, data: "np.ndarray"):
        """Initializes a new `CNumpyArray` object.

        Args:
            data: The NumPy array to be wrapped.

        Raises:
            NotImplementedError: If NumPy is not installed.
        """
        if not HAS_NUMPY:
            msg = "NumPy is not available"
            raise NotImplementedError(msg)

        self._data = np.ascontiguousarray(data)
        super().__init__()

    def _init_c_obj(self):
        self._c_obj = ffi.from_buffer(self._data)
        self._c_size = self._data.nbytes

    @property
    def value(self) -> "np.ndarray":
        """Returns the python representation of the data."""
        return self._data

    @classmethod
    def from_c_obj(
        cls,
        c_obj: ffi.CData,
        c_size: int,
        shape: tuple[int, ...],
        dtype: "np.dtype",
    ) -> "CNumpyArray":
        """Initializes a new `CNumpyArray` object from a C pointer.

        Args:
            c_obj: A pointer to a C object or array.
            c_size: The size of the C object or array.
            shape: The shape of the resulting NumPy array.
            dtype: The NumPy data type.

        Returns:
            A new `CNumpyArray` object

        Raises:
            NotImplementedError: If NumPy is not installed.
            TypeError: If the `c_obj` is not a C pointer or array.
            ValueError: If `c_size` does not match with the array properties.
        """
        if not HAS_NUMPY:
            msg = "NumPy is not available"
            raise NotImplementedError(msg)

        type_str = ffi.getctype(ffi.typeof(c_obj))
        if not type_str.endswith((" *", "[]")):
            msg = f"Expected a pointer or array type, got '{type_str}'"
            raise TypeError(msg)

        computed_c_size = int(np.prod(shape)) * dtype.itemsize
        if c_size != computed_c_size:
            msg = f"Expected size {computed_c_size}, got {c_size}"
            raise ValueError(msg)

        inst = cls.__new__(cls)
        inst._c_obj = c_obj
        inst._c_size = c_size

        buf = ffi.buffer(inst._c_obj, inst._c_size)
        inst._data = np.frombuffer(buf, dtype=dtype).reshape(shape)

        return inst

    def _as_c_array(self, c_type: str = "char") -> ffi.CData:
        """Returns a typed C array pointer (e.g., int*, uint8_t*, etc)."""
        return ffi.cast(f"{c_type} *", self._c_ptr_or_raise)

    def as_memoryview(self) -> memoryview:
        """Returns a memoryview of the wrapped array.

        Returns:
            The array data as a memoryview object.
        """
        return memoryview(self._data)

    def to_bytes(self) -> bytes:
        """Returns the array's raw data as bytes.

        Returns:
            The raw data of the array as bytes.
        """
        return self._data.tobytes()

    @property
    def shape(self) -> tuple[int, ...]:
        """Returns the shape of the array."""
        return self._data.shape

    @property
    def dtype(self) -> "np.dtype":
        """Returns the data type of the array."""
        return self._data.dtype

    @property
    def ndim(self) -> int:
        """Returns the number of the array dimensions."""
        return self._data.ndim

    @property
    def itemsize(self) -> int:
        """Returns the size in bytes of a single array element."""
        return self._data.itemsize

    @property
    def size(self) -> int:
        """Returns the total number of elements in the array."""
        return self._data.size

    @property
    def is_contiguous(self) -> bool:
        """Returns True if the array is C-contiguous in memory."""
        return self._data.flags["C_CONTIGUOUS"]


if HAS_NUMPY:

    @to_ctype.register
    def _(value: np.ndarray, *, precision: str | None = None):
        _ = precision
        return CNumpyArray(value)
