import errno

class VaccelError(RuntimeError):
    """Exception raised when a vAccel runtime error occurs"""

    def __init__(self, err_val, message):
        self.error = err_val
        self.message = message

    def __str__(self):
        return "[errno {}] {}: {}".format(self.error, errno.errorcode[self.error], self.message)

