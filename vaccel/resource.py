# SPDX-License-Identifier: Apache-2.0

"""Interface to the `struct vaccel_resource` C object."""

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from ._c_types import CBytes, CList, CNumpyArray, CType
from ._c_types.utils import CEnumBuilder
from ._libvaccel import ffi, lib
from .error import FFIError, NullPointerError

if TYPE_CHECKING:
    from vaccel.session import (
        BaseSession as Session,  # Type hint only, not imported at runtime
    )

try:
    import numpy as np  # noqa: TC002

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

logger = logging.getLogger(__name__)

enum_builder = CEnumBuilder(lib)
ResourceType = enum_builder.from_prefix("ResourceType", "VACCEL_RESOURCE_")


class Resource(CType):
    """Wrapper for the `struct vaccel_resource` C object.

    Manages the creation and initialization of a C `struct vaccel_resource` and
    provides access to it through Python properties.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _paths (list[Path] | list[str] | Path | str): The path(s) to the
            contained file(s).
        _type (ResourceType): The type of the resource.
        _c_data (CBytes | CNumpyArray | None): The encapsulated buffer data
            passed to the C struct.
        _c_obj_ptr (ffi.CData): A double pointer to the underlying
            `struct vaccel_resource` C object.
    """

    def __init__(
        self, paths: list[Path] | list[str] | Path | str, type_: ResourceType
    ):
        """Initializes a new `Resource` object.

        Args:
            paths: The path(s) to the file(s) that will be represented by the
                resource.
            type_: The type of the resource.
        """
        if isinstance(paths, list):
            self._paths = [str(path) for path in paths]
        else:
            self._paths = [str(paths)]
        self._c_paths = CList(self._paths)
        self._type = type_
        self._c_data = None
        self._c_obj_ptr = ffi.NULL
        self.__sessions = []
        super().__init__()

    def _init_c_obj(self):
        """Initializes the underlying C `struct vaccel_resource` object.

        Raises:
            FFIError: If resource initialization fails.
        """
        self._c_obj_ptr = ffi.new("struct vaccel_resource **")
        if self._c_paths is not None:
            ret = lib.vaccel_resource_multi_new(
                self._c_obj_ptr,
                self._c_paths._c_ptr,
                len(self._c_paths),
                self._type,
            )
        else:
            ret = lib.vaccel_resource_from_buf(
                self._c_obj_ptr,
                self._c_data._c_ptr,
                self._c_data._c_size,
                self._type,
                ffi.NULL,
                True,  # noqa: FBT003
            )
        if ret != 0:
            raise FFIError(ret, "Could not initialize resource")

        self._c_obj = self._c_obj_ptr[0]
        self._c_size = ffi.sizeof("struct vaccel_resource")

    @classmethod
    def from_buffer(
        cls,
        data: bytes | bytearray | memoryview,
        type_: ResourceType,
    ) -> "Resource":
        """Initializes a new `Resource` object from byte-like data.

        Args:
            data: The data to be passed to the C struct.
            type_: The type of the resource.

        Returns:
            A new `Resource` object
        """
        inst = cls.__new__(cls)
        inst._data = data
        inst._type = type_
        inst._c_data = CBytes(inst._data)
        inst._c_paths = None
        inst._c_obj_ptr = ffi.NULL
        inst.__sessions = []
        super().__init__(inst)
        return inst

    @classmethod
    def from_numpy(cls, data: "np.ndarray") -> "Resource":
        """Initializes a new `Resource` object from a NumPy array.

        Args:
            data: The NumPy array containing the resource data.

        Returns:
            A new `Resource` object

        Raises:
            NotImplementedError: If NumPy is not installed.
        """
        if not HAS_NUMPY:
            msg = "NumPy is not available"
            raise NotImplementedError(msg)

        inst = cls.__new__(cls)
        inst._data = data
        inst._type = ResourceType.DATA
        inst._c_data = CNumpyArray(inst._data)
        inst._c_paths = None
        inst._c_obj_ptr = ffi.NULL
        inst.__sessions = []
        super().__init__(inst)
        return inst

    @property
    def value(self) -> ffi.CData:
        """Returns the value of the underlying C struct.

        Returns:
            The dereferenced 'struct vaccel_resource`
        """
        return self._c_ptr_or_raise[0]

    def _del_c_obj(self):
        """Deletes the underlying `struct vaccel_resource` C object.

        Raises:
            FFIError: If resource deletion fails.
        """
        ret = lib.vaccel_resource_delete(self._c_ptr_or_raise)
        if ret != 0:
            raise FFIError(ret, "Could not delete resource")
        self._c_obj = ffi.NULL

    def __del__(self):
        try:
            if self.id < 0:
                return

            for session in self.__sessions:
                if not session:
                    continue
                self.unregister(session)
            self._del_c_obj()
        except NullPointerError:
            pass
        except FFIError:
            logger.exception("Failed to clean up Resource")

    @property
    def id(self) -> int:
        """The resource identifier.

        Returns:
            The resource's unique ID.
        """
        return int(self._c_ptr_or_raise.id)

    @property
    def remote_id(self) -> int:
        """The remote resource identifier.

        Returns:
            The resource's remote ID.
        """
        return int(self._c_ptr_or_raise.remote_id)

    def is_registered(self, session: "Session") -> bool:
        """Checks if the resource is registered with the session.

        Args:
            session: The session to check for registration.

        Returns:
            True if the resource is registered with the session.
        """
        return session in self.__sessions

    def register(self, session: "Session") -> None:
        """Registers the resource with a session.

        Args:
            session: The session to register the resource with.

        Raises:
            FFIError: If resource registration fails.
        """
        ret = lib.vaccel_resource_register(
            self._c_ptr_or_raise,
            session._c_ptr_or_raise,
        )
        if ret != 0:
            raise FFIError(
                ret,
                f"Could not register resource {self.id} "
                f"with session {session.id}",
            )
        self.__sessions.append(session)

    def unregister(self, session: "Session") -> None:
        """Unregisters the resource from a session.

        Args:
            session: The session to unregister the resource from.

        Raises:
            FFIError: If resource unregistration fails.
        """
        ret = lib.vaccel_resource_unregister(
            self._c_ptr_or_raise,
            session._c_ptr_or_raise,
        )
        if ret != 0:
            raise FFIError(
                ret,
                f"Could not unregister resource {self.id} "
                f"from session {session.id}",
            )
        self.__sessions.remove(session)

    def sync(self, session: "Session") -> None:
        """Synchronizes the resource data to reflect any remote changes.

        Args:
            session: The session the resource is registered with.

        Raises:
            FFIError: If resource synchronization fails.
        """
        ret = lib.vaccel_resource_sync(
            self._c_ptr_or_raise,
            session._c_ptr_or_raise,
        )
        if ret != 0:
            raise FFIError(
                ret,
                f"Could not synchronize resource {self.id} "
                f"in session {session.id}",
            )

    def __repr__(self):
        try:
            c_ptr = (
                f"0x{int(ffi.cast('uintptr_t', self._c_obj)):x}"
                if self._c_obj != ffi.NULL
                else "NULL"
            )
            resource_id = self.id
            remote_id = self.remote_id
            paths = self._paths
            type_name = getattr(self._type, "name", repr(self._type))
        except (AttributeError, TypeError, NullPointerError):
            return f"<{self.__class__.__name__} (uninitialized or invalid)>"
        return (
            f"<{self.__class__.__name__} id={resource_id} "
            f"remote_id={remote_id} "
            f"paths={paths!r} "
            f"type={type_name} "
            f"at {c_ptr}>"
        )
