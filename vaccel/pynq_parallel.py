from vaccel.session import Session
from typing import List
from vaccel.genop import Genop, VaccelArg, VaccelOpType
import struct


class Pynq_parallel:
    """A Pynq parallel model vAccel resource.

    Attributes:
        __op__: The genop operation type
        def_arg_write (bytes): The result of the operation
    """

    __op__ = VaccelOpType.VACCEL_PYNQ_PARALLEL

    def_arg_write: bytes = bytes(100 * " ", encoding="utf-8")

    @staticmethod
    def __genop__(arg_read: List[VaccelArg], arg_write: List[VaccelArg], index: int) -> int:
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
        return struct.unpack('d', arg_write[index].raw_content[:8])[0]

    @classmethod
    def pynq_parellel(self, a: float, len_a: int):
        """Executes Pynq parallel operation using vAccel over genop.

        Args:
            a: A float for the array a
            len_a: An integer giving the length of the array

        Returns:
            b: A float for the array b
            add_out: A float for the addition
            mult_out: A float for the multiplication
        """

        arg_read = [VaccelArg(data=int(self.__op__)),
                    VaccelArg(data=a), VaccelArg(data=len_a)]
        arg_write = [VaccelArg(data=self.def_arg_write),
                     VaccelArg(data=self.def_arg_write)]
        return self.__genop__(arg_read=arg_read, arg_write=arg_write, index=0)
