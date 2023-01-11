from vaccel._vaccel import lib


class Noop:
    def __init__(self):
        print("test init")

    def __del__(self):
        print("test del")

    @classmethod
    def noop(self, session):
        """Execute noop"""
        csession = session._to_inner()
        return lib.vaccel_noop(csession)
