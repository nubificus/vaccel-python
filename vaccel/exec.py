from array import array
from vaccel.session import Session
from typing import List
from vaccel.genop import Genop, VaccelArg, VaccelOpType

class Exec:
    """An Exec model vAccel resource.
    
    Attributes:
        def_arg_write (bytes): The result of the operation
        __op__: The genop operation type
    """

    __op__ = VaccelOpType.VACCEL_EXEC
    
    @staticmethod
    def __genop__(arg_read: List[VaccelArg], arg_write: List[VaccelArg], index: int) -> str:
        """Performs the genop operation provided in arg_read.

        Args:
            arg_read : `list`
            arg_write : `list`
            index : `int`

        Returns:
            The content of the `arg_write` indicated by `index`.
        """
        ses = Session(flags=0)
        Genop.genop(ses, arg_read, arg_write)
        return arg_write[index].content

    @classmethod
    def exec(self, library: str, symbol: str, arg_read: List[VaccelArg], arg_write: List[VaccelArg]) -> str:
        """Performs the Exec using vAccel over genop.

        Args:

        Returns:
        """
        arg_read_local = [VaccelArg(data=int(self.__op__)),
                    VaccelArg(data=library),VaccelArg(data=symbol)] + arg_read
        print(arg_read_local)
        return self.__genop__(arg_read=arg_read_local, arg_write=arg_write, index=0)
