from vaccel.session import Session
from typing import List
from vaccel.genop import Genop, VaccelArg, VaccelOpType
import struct

class Pynq_array_copy:
    """A Pynq array copy model vAccel resource.
    
    Attributes:
        __op__: The genop operation type
        def_arg_write (bytes): The result of the operation
    """

    __op__ = VaccelOpType.VACCEL_PYNQ_ARR_COPY
    
    def_arg_write: bytes = bytes(100 * " ", encoding="utf-8")

    @staticmethod
    def __genop__(arg_read: List[VaccelArg], arg_write: List[VaccelArg], index: int) -> int:
        """Performs the genop operation provided in arg_read.

        Args:
            arg_read : A list of inputs
            arg_write : A list of outputs
            index : An integer

        Returns:
            The content of the `arg_write` indicated by `index`.
        """
        ses = Session(flags=0)
        Genop.genop(ses, arg_read, arg_write)
        return struct.unpack('d', arg_write[index].raw_content[:8])[0]

    @classmethod
    def pynq_arr_copy(cls, a:int):
        """Executes Pynq array copy operation using vAccel over genop.

        Args:
            a: An integer for the initial array

        Returns:
            b: An integer for the copy of the array
            c: An integer giving the length of the array
        """

        arg_read = [VaccelArg(data=int(cls.__op__)),
                    VaccelArg(data=a)]
        arg_write = [VaccelArg(data=cls.def_arg_write)]
        return cls.__genop__(arg_read=arg_read, arg_write=arg_write, index=0)