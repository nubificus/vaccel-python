from vaccel._vaccel import lib, ffi
from vaccel.error import VaccelError

from vaccel.session import Session

class Noop:
    def __init__(self):
        """exec vAccel Noop"""
        printf("test init")

    def __del__(self):
        printf("test del")

    @classmethod
    def noop(self, session):
        """exec the operation"""
        csession = session._to_inner()
        return lib.vaccel_noop(csession)

