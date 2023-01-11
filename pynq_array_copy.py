from vaccel.session import Session
from typing import List
from vaccel.genop import Genop, VaccelArg, VaccelOpType
import struct

class Pynq_array_copy:

    __op__ = VaccelOpType.VACCEL_PYNQ_ARR_COPY
    
    def_arg_write: bytes = bytes(100 * " ", encoding="utf-8")

    @staticmethod
    def __genop__(arg_read: List[VaccelArg], arg_write: List[VaccelArg], index: int) -> int:
        """
        Performs the genop operation provided in arg_read.

        Returns the content of the arg_write indicated by index.
        """
        ses = Session(flags=0)
        Genop.genop(ses, arg_read, arg_write)
        return struct.unpack('d', arg_write[index].raw_content[:8])[0]

    @classmethod
    def pynq_arr_copy(self, a:int):
        
        """
        Pynq array copy using vAccel over genop.

        Parameters
        ----------
        a : `int`

        Returns
        ----------
        b : `int`
        c : `int`
        """

        arg_read = [VaccelArg(data=int(self.__op__)),
                    VaccelArg(data=a)]
        arg_write = [VaccelArg(data=self.def_arg_write)]
        return self.__genop__(arg_read=arg_read, arg_write=arg_write, index=0)