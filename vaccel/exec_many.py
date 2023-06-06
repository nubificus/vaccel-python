from vaccel.session import Session
from vaccel.shared_object import Object
from typing import List, Any
from vaccel.genop import VaccelArg, VaccelOpType, VaccelArgList
from vaccel._vaccel import lib, ffi
import os


class Vaccel_Args:
    """
    A helper class for converting argument lists
    to the appropriate vAccel format
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

        return VaccelArgList(new_list).to_cffi()


class Exec_with_many_resources(Object):
    """An Exec with resource model vAccel resource.

    Attributes:
        __op__: The genop operation type
    """

    __op__ = VaccelOpType.VACCEL_EXEC_WITH_RESOURCE

    @classmethod
    def exec_with_many_resources(self, objects: List[str], symbols: List[str], arg_read: List[Any], arg_write: List[Any]):
        """Performs the Exec using vAccel over genop.

        Args:
            object: Filename of a shared object to be used with vaccel exec
            symbol: Name of the function contained in the above shared object
            arg_read: A list of inputs

        Returns:
            arg_write: A list of outputs
        """
        # shared_objects = self.create_shared_objects(self,objects)
        #vaccel_args_read = Vaccel_Args.vaccel_read_args(arg_read)
        #vaccel_args_write = Vaccel_Args.vaccel_write_args(arg_write)
        objects = Object.many_objects(self,objects)
        symbols = Object.many_objects(self,symbols)

        for object, symbol, read in zip(objects, symbols, arg_read):
            session = Session(flags=0)
            print(f"Object: {object}, Symbol: {symbol}, Read: {read}")
            myobject = Object(session,object,symbol)
            shared_obj = myobject.shared
            symbolcdata = myobject.symbol
            myobject.register
            
            vaccel_args_read = Vaccel_Args.vaccel_args(read)
            vaccel_args_write = Vaccel_Args.vaccel_args(arg_write)
            nr_read = len(read)
            nr_write = len(arg_write)
            ret = lib.vaccel_exec_with_resource(session._to_inner(), shared_obj, symbolcdata, vaccel_args_read, nr_read, vaccel_args_write, nr_write)
        #return arg_write[0].content
