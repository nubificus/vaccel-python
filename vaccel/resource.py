"""Interface to the `struct vaccel_resource` C object."""

from pathlib import Path
from typing import TYPE_CHECKING

from ._c_types import CType
from ._c_types.utils import CEnumBuilder
from ._libvaccel import ffi, lib
from .error import FFIError

if TYPE_CHECKING:
    from vaccel.session import (
        BaseSession as Session,  # Type hint only, not imported at runtime
    )


enum_builder = CEnumBuilder(lib)
ResourceType = enum_builder.from_prefix("ResourceType", "VACCEL_RESOURCE_")


class Resource(CType):
    """Wrapper for the `struct vaccel_resource` C object.

    Manages the creation and initialization of a C `struct vaccel_resource` and
    provides access to it through Python properties.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _path (str): The path to the contained file.
        _type (ResourceType): The type of the resource.
    """

    def __init__(self, path: str | Path, type_: ResourceType):
        """Initializes a new `Resource` object.

        Args:
            path: The path to the file that will be represented by the resource.
            type_: The type of the resource.
        """
        # TODO: Allow the use of lists for path  # noqa: FIX002
        self._path = str(path)
        self._type = type_
        self.__sessions = []
        super().__init__()

    def _init_c_obj(self):
        """Initializes the underlying C `struct vaccel_resource` object.

        Raises:
            FFIError: If resource initialization fails.
        """
        self._c_obj_ptr = ffi.new("struct vaccel_resource **")
        ret = lib.vaccel_resource_new(
            self._c_obj_ptr, self._path.encode(), self._type
        )
        if ret != 0:
            raise FFIError(ret, "Could not initialize resource")

        self._c_obj = self._c_obj_ptr[0]
        self._c_size = ffi.sizeof("struct vaccel_resource")

    @property
    def value(self) -> ffi.CData:
        """Returns the value of the underlying C struct.

        Returns:
            The dereferenced 'struct vaccel_resource`
        """
        return self._c_obj[0]

    def _del_c_obj(self):
        """Deletes the underlying `struct vaccel_resource` C object.

        Raises:
            FFIError: If resource deletion fails.
        """
        if self._c_obj:
            ret = lib.vaccel_resource_delete(self._c_obj)
            if ret != 0:
                raise FFIError(ret, "Could not delete resource")
            self._c_obj = None

    def __del__(self):
        for session in self.__sessions:
            self.unregister(session)
        self._del_c_obj()

    @property
    def id(self) -> int:
        """The resource identifier.

        Returns:
            The resource's unique ID.
        """
        return int(self._c_obj.id)

    @property
    def remote_id(self) -> int:
        """The remote resource identifier.

        Returns:
            The resource's remote ID.
        """
        return int(self._c_obj.remote_id)

    def is_registered(self, session: "Session") -> bool:
        """Checks if the resource is registered with the session.

        Args:
            session: The session to check for registration.

        Returns:
            True if the resource is registered with the session.
        """
        return session in self.__sessions

    def register(self, session: "Session") -> None:
        """Register the resource with a session.

        Args:
            session: The session to register the resource with.
        """
        ret = lib.vaccel_resource_register(
            self._c_obj,
            session._c_ptr,
        )
        if ret != 0:
            raise FFIError(
                ret,
                f"Could not register resource {self.id()} "
                f"with session {session.id()}",
            )
        self.__sessions.append(session)

    def unregister(self, session: "Session") -> None:
        """Unregister the resource from a session.

        Args:
            session: The session to unregister the resource from.
        """
        ret = lib.vaccel_resource_unregister(
            self._c_obj,
            session._c_ptr,
        )
        if ret != 0:
            raise FFIError(
                ret,
                f"Could not unregister resource {self.id()} "
                f"from session {session.id()}",
            )
        self.__sessions.remove(session)
