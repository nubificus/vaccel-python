# SPDX-License-Identifier: Apache-2.0

"""Interface to the `struct vaccel_tf_node` C object."""

import logging

from vaccel._c_types import CStr, CType
from vaccel._libvaccel import ffi, lib
from vaccel.error import FFIError, NullPointerError

logger = logging.getLogger(__name__)


class Node(CType):
    """Wrapper for the `struct vaccel_tf_node` C object.

    Manages the creation and initialization of a C `struct vaccel_tf_node` and
    provides access to it through Python properties.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _name (str): The name of the node.
        _id (int): The ID of the node.
        _c_obj_ptr (ffi.CData): A double pointer to the underlying
            `struct vaccel_tf_node` C object.
    """

    def __init__(self, name: str, id_: int):
        """Initializes a new `Node` object.

        Args:
            name: The name to be passed to the C struct.
            id_: The ID to be passed to the C struct.
        """
        self._name = name
        self._id = id_
        self._c_obj_ptr = ffi.NULL
        super().__init__()

    def _init_c_obj(self):
        """Initializes the underlying C `struct vaccel_tf_node` object.

        Raises:
            FFIError: If node initialization fails.
        """
        self._c_obj_ptr = ffi.new("struct vaccel_tf_node **")

        ret = lib.vaccel_tf_node_new(
            self._c_obj_ptr, self._name.encode(), self._id
        )
        if ret != 0:
            raise FFIError(ret, "Could not initialize node")

        self._c_obj = self._c_obj_ptr[0]
        self._c_size = ffi.sizeof("struct vaccel_tf_node")

    @property
    def value(self) -> ffi.CData:
        """Returns the value of the underlying C struct.

        Returns:
            The dereferenced 'struct vaccel_tf_node`
        """
        return self._c_ptr_or_raise[0]

    def _del_c_obj(self):
        """Deletes the underlying `struct vaccel_tf_node` C object.

        Raises:
            FFIError: If node deletion fails.
        """
        ret = lib.vaccel_tf_node_delete(self._c_ptr_or_raise)
        if ret != 0:
            raise FFIError(ret, "Could not delete node")

    def __del__(self):
        try:
            self._del_c_obj()
        except NullPointerError:
            pass
        except FFIError:
            logger.exception("Failed to clean up Node")

    @property
    def name(self) -> str:
        """The node name.

        Returns:
            The node's name.
        """
        return CStr.from_c_obj(self._c_ptr_or_raise.name).value

    @property
    def id(self) -> int:
        """The node identifier.

        Returns:
            The node's ID.
        """
        return int(self._c_ptr_or_raise.id[0])

    def __repr__(self):
        try:
            c_ptr = (
                f"0x{int(ffi.cast('uintptr_t', self._c_obj)):x}"
                if self._c_obj != ffi.NULL
                else "NULL"
            )
            node_name = self.name
            node_id = self.id
        except (AttributeError, TypeError, NullPointerError):
            return f"<{self.__class__.__name__} (uninitialized or invalid)>"
        return (
            f"<{self.__class__.__name__} name={node_name!r} "
            f"id={node_id} "
            f"at {c_ptr}>"
        )
