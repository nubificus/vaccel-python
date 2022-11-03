from vaccel._vaccel import lib


class Noop:
    def __init__(self):
        """exec vAccel Noop"""
        print("test init")

    def __del__(self):
        print("test del")

    @classmethod
    def noop(self, session):
        """exec the operation"""
        csession = session._to_inner()
        return lib.vaccel_noop(csession)
