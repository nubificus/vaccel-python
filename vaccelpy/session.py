from vaccel._vaccel import lib, ffi
from vaccel.error import VaccelError


class VaccelSession:
    def __init__(self, flags: int = 0) -> None:
        self.__csession__ = ffi.new("struct vaccel_session *")
        ret = lib.vaccel_sess_init(self.__csession__, flags)
        if ret != 0:
            raise VaccelError(ret, "Could not initialize session")

    def __del__(self) -> None:
        self.free()
        ffi.release(self.__csession__)

    def free(self) -> None:
        ret = lib.vaccel_sess_free(self.__csession__)
        if ret != 0:
            raise VaccelError(ret, "Could not free session")

    @property
    def id(self) -> int:
        """Get the session id"""
        return self.__csession__.session_id

    def register_resource(self, resource) -> None:
        """Register a vAccel resource with the session"""

        ret = lib.vaccel_sess_register(
            self.__csession__, resource)
        if ret != 0:
            raise VaccelError(
                ret, "Could not register resource to session {}".format(self.id()))

    def unregister_resource(self, resource) -> None:
        """Unregister a vAccel resource from the session"""

        ret = lib.vaccel_sess_unregister(
            self.__csession__, resource)
        if ret != 0:
            raise VaccelError(
                ret, "Could not unregister resource from session {}".format(self.id()))

    def has_resource(self, resource) -> None:
        """Returns true if the resource is registered with the session"""

        return lib.vaccel_sess_has_resource(self.__csession__, resource) != 0
