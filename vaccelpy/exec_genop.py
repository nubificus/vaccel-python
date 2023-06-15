from vaccel._vaccel import lib, ffi
from vaccelpy.common import VaccelOpType, VaccelOperationResult
from vaccelpy.vaccelarg import VaccelArg, create_vaccel_arg_array

from typing import List, Any
from vaccelpy.session import VaccelSession
from vaccelpy.genop import __Genop__


class Exec:
    """An Exec operation model vAccel resource

    Attributes:
        __op__: The genop operation type
    """

    __op__ = VaccelOpType.VACCEL_EXEC

    @staticmethod
    def __genop__(arg_read: List[VaccelArg], arg_write: List[VaccelArg]) -> VaccelOperationResult:
        """Performs the genop operation provided in arg_read.

        Args:
            session : A vaccel.Session instance
            arg_read : A list of inputs
            arg_write : A list of outputs

        Returns:
            result: An object containing the ret code and the values of arg_write arguments
        """
        session = VaccelSession(flags=0)
        return __Genop__.__run__(session, arg_read=arg_read, arg_write=arg_write)

    @staticmethod
    def run(library: str, symbol: str, arg_read: List[Any], arg_write: List[Any]) -> VaccelOperationResult:
        arg_read_local = [int(Exec.__op__), library, symbol]
        arg_read_local.extend(arg_read)
        if len(arg_write) == 0:
            arg_write = [bytes(100 * " ", encoding="utf-8")]
        return Exec.__genop__(arg_read=arg_read_local, arg_write=arg_write)
