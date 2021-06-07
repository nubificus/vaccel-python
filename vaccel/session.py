from vaccel._vaccel import lib, ffi
from vaccel.error import VaccelError

class Session:
    def __init__(self, flags):
        """Create a new vAccel session"""

        self._inner = ffi.new("struct vaccel_session *")
        ret = lib.vaccel_sess_init(self._inner, flags)
        if ret != 0:
            raise VaccelError(ret, "Could not initialize session")

    def __del__(self):
        ret = lib.vaccel_sess_free(self._inner)
        if ret != 0:
            raise VaccelError(ret, "Could not free vAccel session")

    def id(self):
        """Get the session id"""

        return self._inner.session_id

    def register_resource(self, resource):
        """Register a vAccel resource with the session"""

        ret = lib.vaccel_sess_register(self._inner, resource._get_inner_resource())
        if ret != 0:
            raise VaccelError(ret, "Could not register resource to session".format(self.id()))
        
    def unregister_resource(self, resource):
        """Unregister a vAccel resource from the session"""

        ret = lib.vaccel_sess_unregister(self._inner, resource._get_inner_resource())
        if ret != 0:
            raise VaccelError(ret, "Could not unregister resource from session".format(self.id()))

    def has_resource(self, resource):
        """Returns true if the resource is registered with the session"""

        return lib.vaccel_sess_has_resource(self._inner, resource._get_inner_resource()) != 0

    def _to_inner(self):
        return self._inner
