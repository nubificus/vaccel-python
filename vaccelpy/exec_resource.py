from typing import Any, List

from vaccel._vaccel import lib
from vaccelpy.common import VaccelOperationResult, VaccelOpType
from vaccelpy.session import VaccelSession
from vaccelpy.shared_object import VaccelObject
from vaccelpy.vaccelarg import VaccelArg, create_vaccel_arg_array


class ExecResource:
    """An Exec with resource model vAccel operation.

    Attributes:
        __op__: The exec with resource operation type
    """
    __op__ = VaccelOpType.VACCEL_EXEC_WITH_RESOURCE

    @staticmethod
    def run(obj: str, symbol: str, arg_read: List[Any], arg_write: List[Any]) -> VaccelOperationResult:
        """Performs the Exec with resource operation

        Args:
            object: Filename of a shared object to be used with vaccel exec
            symbol: Name of the function contained in the above shared object
            arg_read: A list of inputs
            arg_write: A list of outputs

        Returns:
            result: An object containing the vAccel return code and the values of arg_write arguments
        """
        session = VaccelSession(flags=0)
        object = VaccelObject(obj, symbol)
        session.register_resource(object.resource)
        vaccel_arg_read = [VaccelArg(arg) for arg in arg_read]
        c_vaccel_arg_read = create_vaccel_arg_array(vaccel_arg_read)
        vaccel_arg_write = [VaccelArg(arg) for arg in arg_write]
        c_vaccel_arg_write = create_vaccel_arg_array(vaccel_arg_write)

        nr_read = len(vaccel_arg_read)
        nr_write = len(vaccel_arg_write)
        ret = lib.vaccel_exec_with_resource(
            session.__csession__, object.cobject, object.csymbol, c_vaccel_arg_read, nr_read, c_vaccel_arg_write, nr_write)
        session.unregister_resource(object.resource)

        return VaccelOperationResult(
            ret=ret,
            arg_write=[arg for arg in vaccel_arg_write]
        )


class ExecManyResource:
    """An Exec with resource model vAccel resource.

    Attributes:
        __op__: The genop operation type
    """

    __op__ = VaccelOpType.VACCEL_EXEC_WITH_RESOURCE

    @staticmethod
    def run(objects: List[str], symbols: List[str], arg_read: List[Any], arg_write: List[Any]) -> List[VaccelOperationResult]:
        """Performs the Exec with resources operation

        Args:
            objects: Filenames of shared objects to be used with vaccel exec
            symbols: Names of the functions contained in the above shared objects
            arg_read: A list of inputs
            arg_write: A list of outputs

        Returns:
            result: An list of objects containing the vAccel return code and the values of arg_write arguments for each exec
        """
        output = []
        session = VaccelSession(flags=0)

        for shared, symbol, read in zip(objects, symbols, arg_read):
            print(shared, symbol, read)
            object = VaccelObject(shared, symbol)
            session.register_resource(object.resource)
            vaccel_arg_read = [VaccelArg(read)]
            c_vaccel_arg_read = create_vaccel_arg_array(vaccel_arg_read)
            vaccel_arg_write = [VaccelArg(arg) for arg in arg_write]
            c_vaccel_arg_write = create_vaccel_arg_array(vaccel_arg_write)
            nr_read = len(vaccel_arg_read)
            nr_write = len(vaccel_arg_write)
            ret = lib.vaccel_exec_with_resource(
                session.__csession__, object.cobject, object.csymbol, c_vaccel_arg_read, nr_read, c_vaccel_arg_write, nr_write)
            session.unregister_resource(object.resource)
            output.append(VaccelOperationResult(
                ret=ret,
                arg_write=[arg.value for arg in vaccel_arg_write]
            ))
        return output
