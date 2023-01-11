from array import array
from vaccel.session import Session
from typing import List
from vaccel.genop import Genop, VaccelArg, VaccelOpType

class Sgemm:

    __op__ = VaccelOpType.VACCEL_BLAS_SGEMM
    
    def_arg_write: bytes = bytes(100 * " ", encoding="utf-8")

    @staticmethod
    def __genop__(arg_read: List[VaccelArg], arg_write: List[VaccelArg], index: int) -> str:
        """
        Performs the genop operation provided in arg_read.

        Returns the content of the arg_write indicated by index.
        """
        ses = Session(flags=0)
        Genop.genop(ses, arg_read, arg_write)
        return arg_write[index].content

    @classmethod
    def sgemm(self, m:int, n:int, k:int, alpha:float, lda:int, ldb:int, beta:float):
        """
        Sgemm using vAccel over genop.

        Parameters
        ----------
        m : `int`,
        n : `int`,
        k : `int`,
        alpha : `float`,
        lda : `int`,
        ldb : `int`,
        beta : `float`

        Returns
        ----------
        ldc : `int`
        """
        arg_read = [VaccelArg(data=int(self.__op__)),
                    VaccelArg(data=m),VaccelArg(data=n),VaccelArg(data=k),
                    VaccelArg(data=alpha),VaccelArg(data=lda),
                    VaccelArg(data=ldb),VaccelArg(data=beta)]
        arg_write = [VaccelArg(data=self.def_arg_write)]
        return self.__genop__(arg_read=arg_read, arg_write=arg_write, index=0)
