from vaccel._vaccel import lib, ffi
from vaccel.error import VaccelError
from vaccel.tensorflow import Tensor

class Session:
    def __init__(self, flags):
        """Create a new vAccel session"""

        self._inner = ffi.new("struct vaccel_session *")
        ret = lib.vaccel_session_init(self._inner, flags)
        if ret != 0:
            raise VaccelError(ret, "Could not initialize session")

    def __del__(self):
        ret = lib.vaccel_session_release(self._inner)
        if ret != 0:
            raise VaccelError(ret, "Could not free vAccel session")

    def id(self):
        """Get the session id"""

        return self._inner.id

    def has_resource(self, resource):
        """Returns true if the resource is registered with the session"""

        return lib.vaccel_session_has_resource(self._inner, resource._get_inner_resource()) != 0

    def _to_inner(self):
        return self._inner

