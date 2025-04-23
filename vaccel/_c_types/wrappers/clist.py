"""C type interface for `list` objects."""

from collections.abc import Iterator, Sequence
from typing import Any

from vaccel._c_types.types import CType, to_ctype
from vaccel._libvaccel import ffi


class CList(CType):
    """Wrapper for `list` objects.

    Provides an interface to interact with the C representation of `list`
    objects.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _items (Sequence[Any])): An input sequence of items.
        _item_type (type): The type of the input items.
        _ctype_str (str): The type string of the C representation of the items.
    """

    def __init__(self, items: Sequence[Any]):
        """Initializes a new `CList` object.

        Args:
            items: The input sequence of items to be wrapped.
        """
        if not items:
            msg = "CList cannot be empty"
            raise ValueError(msg)

        # Wrap items
        # TODO: Optimize this. Not all types need wrappers for  # noqa: FIX002
        # values
        self._items = [to_ctype(item) for item in items]
        self._item_type = type(self._items[0])

        # Validate all are same type
        if not all(isinstance(i, self._item_type) for i in self._items):
            msg = "All elements must be of the same type"
            raise TypeError(msg)

        # Infer C type string (e.g., "int", "double") based on first element
        self._ctype_str = self._infer_ctype_str(self._items[0])
        super().__init__()

    def _infer_ctype_str(self, item: CType) -> str:
        ptr = item._c_ptr
        ctype = ffi.getctype(ffi.typeof(ptr))
        return ctype.replace(" *", "")

    def _init_c_obj(self):
        if any(
            (item._c_ptr is None or item._c_ptr == ffi.NULL)
            for item in self._items
        ):
            self._c_obj = ffi.new(f"{self._ctype_str}[{len(self._items)}]")
        else:
            values = [item.value for item in self._items]
            self._c_obj = ffi.new(f"{self._ctype_str}[{len(values)}]", values)
        self._c_size = ffi.sizeof(self._c_obj)
        self._is_ptr_array = False

    @property
    def value(self) -> list[ffi.CData]:
        """Returns the python representation of the list."""
        return [self._c_obj[i] for i in range(len(self._items))]

    @classmethod
    def from_ptrs(cls, items: Sequence[Any]) -> "CList":
        """Initializes a new `CList` object of pointers to items.

        Creates a C array of pointers to the C representations of the provided
        items.

        Args:
            items: An input sequence of items.

        Returns:
            A new `CList` object
        """
        if not items:
            msg = "CList.from_ptrs() cannot be called with empty items"
            raise ValueError(msg)

        inst = cls.__new__(cls)

        # Wrap items
        inst._items = [to_ctype(item) for item in items]
        inst._item_type = type(inst._items[0])

        # Validate all are same type
        if not all(isinstance(i, inst._item_type) for i in inst._items):
            msg = "All elements must be of the same type"
            raise TypeError(msg)

        # Build array of pointers
        c_ptrs = [item._c_ptr for item in items]
        ptr_type = ffi.typeof(c_ptrs[0])
        inst._c_obj = ffi.new(
            f"{ffi.getctype(ptr_type)}[{len(c_ptrs)}]", c_ptrs
        )
        inst._c_size = ffi.sizeof(inst._c_obj)
        inst._is_ptr_array = True
        return inst

    # Mutators
    def append(self, value: Any):
        """Appends the value to the `CList` and updates the C representation."""
        # Warning: this will allocate a new C array
        c_value = to_ctype(value)
        if not isinstance(c_value, self._item_type):
            msg = f"Expected {self._item_type}, got {type(c_value)}"
            raise TypeError(msg)
        self._items.append(c_value)
        self._init_c_obj()

    def extend(self, values: Sequence[Any]):
        """Extends `CList` with the values and updates the C representation."""
        # Warning: this will allocate a new C array
        new_items = [to_ctype(val) for val in values]
        for item in new_items:
            if not isinstance(item, self._item_type):
                msg = (
                    f"Expected all items to be {self._item_type}, "
                    f"got {type(item)}"
                )
                raise TypeError(msg)
        self._items.extend(new_items)
        self._init_c_obj()

    def __setitem__(self, idx: int, value: Any):
        c_value = to_ctype(value)
        if not isinstance(c_value, self._item_type):
            msg = f"Expected {self._item_type}, got {type(c_value)}"
            raise TypeError(msg)
        self._items[idx] = c_value
        self._c_obj[idx] = c_value.value

    def __getitem__(self, idx: int):
        return self._items[idx]

    def __len__(self):
        return len(self._items)

    def __iter__(self) -> Iterator[CType]:
        return iter(self._items)

    def __contains__(self, val: Any):
        return any(val == item.value for item in self._items)

    def as_list(self):
        return self.value

    def __eq__(self, other: "CList | list"):
        if isinstance(other, CList):
            return self.value == other.value
        if isinstance(other, list):
            return self.value == other
        return False

    def __bool__(self):
        return bool(self._items)

    def __reversed__(self):
        return reversed(self._items)

    def __add__(self, other: "CList | list"):
        if isinstance(other, (list, CList)):
            return CList(self._items + list(other))
        msg = "Can only add list or CList"
        raise TypeError(msg)

    def __iadd__(self, other: "CList | list"):
        if isinstance(other, (list, CList)):
            for item in other:
                self.append(item)
            return self
        msg = "Can only add list or CList"
        raise TypeError(msg)

    def __hash__(self):
        return hash(tuple(self.value))

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"<CList[{len(self)}] {self.value}>"


@to_ctype.register(tuple)
@to_ctype.register(list)
def _(value: list):
    return CList(value)
