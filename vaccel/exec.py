from vaccel.session import Session
from vaccel.shared_object import Object
from typing import List, Any
from vaccel.genop import Genop, VaccelArg, VaccelOpType, VaccelArgList
from vaccel._vaccel import lib, ffi
import os
import pdb

__hidden__ = list()

class Vaccel_Args:
    """
    A helper class for converting argument lists to the appropriate vAccel format
    """

    @staticmethod
    def vaccel_args(args: List[Any]) -> List[VaccelArg]:
        """Convert a list of arguments to a list of VaccelArg objects

        Args:
            args : A list of integers

       Returns:
            A list of VaccelArg objects
        """
        iterable = list(args)

        new_list = []
        for item in iterable:
            new_item=VaccelArg(data=item)
            new_list.append(new_item)
            __hidden__.append(new_item)

        return VaccelArgList(new_list).to_cffi()


class Exec_Operation:
    """An Exec Operation model vAccel resource

    Attributes:
        def_arg_write (bytes): The result of the operation
    """

    def_arg_write: bytes = bytes(100 * " ", encoding="utf-8")

    @staticmethod
    def __genop__(session, arg_read: List[VaccelArg], arg_write: List[VaccelArg], index: int) -> str:
        """Performs the genop operation provided in arg_read.

        Args:
            arg_read : A list of inputs
            arg_write : A list of outputs
            index : An integer

        Returns:
            The content of the `arg_write` indicated by `index`.
        """
        Genop.genop(session, arg_read, arg_write)
        #return arg_write[index].content
        return arg_write


class Exec(Exec_Operation):
    """An Exec operation model vAccel resource

    Attributes:
        __op__: The genop operation type
    """

    __op__ = VaccelOpType.VACCEL_EXEC

    @classmethod
    def exec(self, library: str, symbol: str, arg_read: List[Any], arg_write: List[Any]):
        """Performs the Exec using vAccel over genop.

        Args:
            library: Path to the shared object containing the function that the user wants to call
            symbol: Name of the function contained in the above shared object
            arg_read: A list of inputs

        Returns:
            arg_write: A list of outputs
        """

        session = Session(flags=0)
        arg_read_local = [VaccelArg(data=int(self.__op__)),
                          VaccelArg(data=library), VaccelArg(data=symbol)] + arg_read
        arg_write = [VaccelArg(data=bytes(100 * " ", encoding="utf-8"))]
        ret = self.__genop__(session, arg_read=arg_read_local, arg_write=arg_write, index=0)
        return ret


class Exec_with_resource(Exec_Operation):
    """An Exec with resource model vAccel resource.

    Attributes:
        __op__: The genop operation type
    """


    __op__ = VaccelOpType.VACCEL_EXEC_WITH_RESOURCE

    @classmethod
    def exec_with_resource(self, obj: str, symbol: str, arg_read: List[Any], arg_write: List[Any]):
        """Performs the Exec with resource operation

        Args:
            object: Filename of a shared object to be used with vaccel exec
            symbol: Name of the function contained in the above shared object
            arg_read: A list of inputs

        Returns:
            arg_write: A list of outputs
        """
        session = Session(flags=0)

        myobject = Object(session,obj,symbol)
        shared_obj = myobject.shared
        symbolcdata = myobject.symbol
        #myobject.register


        vaccel_args_read = Vaccel_Args.vaccel_args(arg_read)
        vaccel_args_write = Vaccel_Args.vaccel_args(arg_write)
        nr_read = len(vaccel_args_read)
        nr_write = len(vaccel_args_write)


        ret = lib.vaccel_exec_with_resource(session._to_inner(), shared_obj, symbolcdata, vaccel_args_read, nr_read, vaccel_args_write, nr_write)
        print(arg_write)
        #import pdb;pdb.set_trace()
        print(vaccel_args_write[0].buf)

        #myobject.unregister
        
        return arg_write 
