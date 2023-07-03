from vaccel._vaccel import lib


class Noop:
    def __init__(self):
        print("test init")

    def __del__(self):
        print("test del")

    @staticmethod
    def noop(session):
        """Execute noop
        
        Args: 
            session: A vaccel.Session instance

        Returns:
            A string containing the noop result
        """
        csession = session._to_inner()
        return lib.vaccel_noop(csession)
