from vaccel.session import Session
from vaccel.shared_object import Object
from typing import List, Any
from vaccel.genop import Genop, VaccelArg, VaccelOpType, VaccelArgList
from vaccel._vaccel import lib, ffi
import os

#__hidden__ = list()

# class Object:
#     def __init__(self, obj):
#         """Create a new vAccel object"""
#         self.object = obj
        
#     def __parse_object__(self) -> bytes:
#         """Parses a shared object file and returns its content and size

#         Args:
#             obj: The path to the shared object file

#         Returns:
#             A tuple containing the content of the shared object file as bytes
#             and its size as an integer

#         Raises:
#             TypeError: If object is not a string
#         """
#         filename = self
#         obj = self
#         if not isinstance(obj, str):
#             raise TypeError(
#                 f"Invalid image type. Expected str or bytes, got {type(obj)}.")

#         if isinstance(obj, str):
#             with open(obj, "rb") as objfile:
#                 obj = objfile.read()

#         size = os.stat(filename).st_size
#         return obj, size

#     def create_shared_object(self):
#         """Creates a shared object from a file and returns a pointer to it

#         Args:
#             obj: The file path to the object file

#         Returns:
#             A pointer to the shared object
#         """
#         sharedobj, size = Object.__parse_object__(self)
#         shared = ffi.new("struct vaccel_shared_object *")
#         sharedobject = ffi.new("char[%d]" % size, sharedobj)
#         __hidden__.append(sharedobject)
#         sharedobject = ffi.cast("const void *", sharedobject)
#         lib.vaccel_shared_object_new_from_buffer(shared, sharedobject, size)
#         return shared
        
    
#     def register_object(self,session):
#         ret= lib.vaccel_sess_register(session._to_inner(), self.resource)
#         return ret


#     def object_symbol(self,symbol):
#         symbolcdata = ffi.new(f"char[{len(symbol)}]",
#                               bytes(symbol, encoding='utf-8'))
#         return symbolcdata


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


class Exec_with_resource(Exec_Operation, Object):
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
        shared = self.create_shared_object(obj)
        Object.register_object(shared,session)

        #shared = self.create_shared_object(obj)

        vaccel_args_read = Vaccel_Args.vaccel_args(arg_read)
        vaccel_args_write = Vaccel_Args.vaccel_args(arg_write)
        nr_read = len(vaccel_args_read)
        nr_write = len(vaccel_args_write)

        symbolcdata = Object.object_symbol(obj,symbol)


        ret = lib.vaccel_exec_with_resource(session._to_inner(), shared, symbolcdata, vaccel_args_read, nr_read, vaccel_args_write, nr_write)


        #return arg_write[0].content
