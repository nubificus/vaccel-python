from array import array
from vaccel.session import Session
from typing import List
from vaccel.genop import Genop, VaccelArg, VaccelOpType

class Sgemm:
    """An Sgemm model vAccel resource.
    
    Attributes:
        def_arg_write (bytes): The result of the operation
        __op__: The genop operation type
    """

    __op__ = VaccelOpType.VACCEL_BLAS_SGEMM
    
    def_arg_write: bytes = bytes(100 * " ", encoding="utf-8")

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
    def sgemm(self, m:int, n:int, k:int, alpha:float, lda:int, ldb:int, beta:float):
        """Performs the Sgemm using vAccel over genop.

        Args:
            m: An integer for m dimension
            n: An integer for m dimension
            k: An integer for m dimension
            alpha: A float for scalar constant
            lda: An integer for the dimension
            ldb: An integer for the dimension
            beta: A float for scalar constant

        Returns:
            ldc: An integer
        """
        arg_read = [VaccelArg(data=int(self.__op__)),
                    VaccelArg(data=m),VaccelArg(data=n),VaccelArg(data=k),
                    VaccelArg(data=alpha),VaccelArg(data=lda),
                    VaccelArg(data=ldb),VaccelArg(data=beta)]
        arg_write = [VaccelArg(data=self.def_arg_write)]
        return self.__genop__(arg_read=arg_read, arg_write=arg_write, index=0)
