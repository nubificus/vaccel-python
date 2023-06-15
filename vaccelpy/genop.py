from vaccelpy.session import VaccelSession
from vaccelpy.vaccelarg import VaccelArg, create_vaccel_arg_array
from vaccelpy.common import VaccelOperationResult
from typing import List, Any
from vaccel._vaccel import lib


class __Genop__:
    """A geveric vaccel operation.
    """
    @staticmethod
    def __run__(session: VaccelSession, arg_read: List[Any], arg_write: List[Any]) -> VaccelOperationResult:
        """Performs a generic vaccel operation

        Args:
            session : A vaccel.Session instance
            arg_read: A list of inputs
            arg_write: A list of outputs

        Returns:
            result: An object containing the ret code and the values of arg_write arguments
        """
        vaccel_arg_read = [VaccelArg(arg) for arg in arg_read]
        c_vaccel_arg_read = create_vaccel_arg_array(vaccel_arg_read)
        vaccel_arg_write = [VaccelArg(arg) for arg in arg_write]
        c_vaccel_arg_write = create_vaccel_arg_array(vaccel_arg_write)

        nr_read = len(vaccel_arg_read)
        nr_write = len(vaccel_arg_write)
        ret = lib.vaccel_genop(
            session.__csession__, c_vaccel_arg_read, nr_read, c_vaccel_arg_write, nr_write)
        return VaccelOperationResult(
            ret=ret,
            arg_write=[arg.value for arg in vaccel_arg_write]
        )
