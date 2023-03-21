from vaccel.session import Session
from typing import List
from vaccel.genop import Genop, VaccelArg, VaccelOpType, VaccelArgList
from vaccel._vaccel import lib, ffi
from vaccel.error import VaccelError
import os
import sys 
from ctypes import *

class Object:
    def obj(self, flags):
        """Create a new vAccel object"""

        self._inner = ffi.new("struct vaccel_shared_object *")
        ret = lib.vaccel_obj_init(self._inner, flags)
        if ret != 0:
            raise VaccelError(ret, "Could not initialize session")


class Exec_Operation:
    """An Image Operation model vAccel resource
    
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
        return arg_write[index].content

    @staticmethod
    
    def read_file(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    
    def __parse_object__(obj: "str") -> bytes:
        
        filename = obj
        if not isinstance(obj, str):
            raise TypeError(
                f"Invalid image type. Expected str or bytes, got {type(obj)}.")
 
        if isinstance(obj, str):
            with open(obj, "rb") as objfile:
                obj = objfile.read()

        size = os.stat(filename).st_size
        return obj, size

class Exec(Exec_Operation):
    """An Exec model vAccel resource.

    Attributes:
        __op__: The genop operation type
    """

    __op__ = VaccelOpType.VACCEL_EXEC

    @classmethod
    def exec(self, library: str, symbol: str, arg_read: List[VaccelArg], arg_write: List[VaccelArg]) -> str:
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
                    VaccelArg(data=library),VaccelArg(data=symbol)] + arg_read
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
    def exec_with_resource(self, obj: str, symbol: str, arg_read: List[VaccelArg], arg_write: List[VaccelArg]) -> str:
        """Performs the Exec using vAccel over genop.

        Args:
            object: Filename of a shared object to be used with vaccel exec
            symbol: Name of the function contained in the above shared object
            arg_read: A list of inputs

        Returns:
            arg_write: A list of outputs
        """
        session = Session(flags=0)
        sharedobj, size = Exec_Operation.__parse_object__(obj)
        shared = ffi.new("struct vaccel_shared_object *");
        sharedobject = ffi.new("char[%d]" % size, sharedobj);
        sharedobject = ffi.cast("const void *", sharedobject)
        lib.vaccel_shared_object_new_from_buffer(shared, sharedobject, size);
        arg_read_local = [VaccelArg(data=int(self.__op__)),
                          VaccelArg(data=shared),VaccelArg(data=symbol)] + arg_read
        arg_write = [VaccelArg(data=bytes(100 * " ", encoding="utf-8"))]
        vaccel_args_read = VaccelArgList(arg_read).to_cffi()
        vaccel_args_write = VaccelArgList(arg_write).to_cffi()
        nr_read = len(arg_read)
        nr_write = len(arg_write)

        symbolcdata = ffi.new(f"char[{len(symbol)}]",
                              bytes(symbol, encoding='utf-8'))

        lib.vaccel_sess_register(session._to_inner(), shared.resource)
        ret = lib.vaccel_exec_with_resource(session._to_inner(), shared, symbolcdata, vaccel_args_read, nr_read, vaccel_args_write, nr_write)
        return arg_write[0].content

    @classmethod
    def exec_with_resource_genop(self, obj: str, symbol: str, arg_read: List[VaccelArg], arg_write: List[VaccelArg]) -> str:
        """Performs the Exec using vAccel over genop.

        Args:
            object: Filename of a shared object to be used with vaccel exec
            symbol: Name of the function contained in the above shared object
            arg_read: A list of inputs

        Returns:
            arg_write: A list of outputs
        """

        session = Session(flags=0)
        sharedobj, size = Exec_Operation.__parse_object__(obj)
        shared = ffi.new("struct vaccel_shared_object *");
        sharedobject = ffi.new("char[%d]" % size, sharedobj);
        sharedobject = ffi.cast("const void *", sharedobject)
        lib.vaccel_shared_object_new_from_buffer(shared, sharedobject, size);
        lib.vaccel_sess_register(session._to_inner(), shared.resource)
        rid = lib.vaccel_shared_object_get_id(shared)
        arg_read_local = [VaccelArg(data=int(self.__op__)),
                          VaccelArg(data=rid),VaccelArg(data=symbol)] + arg_read
        arg_write = [VaccelArg(data=bytes(100 * " ", encoding="utf-8"))]
        return self.__genop__(session, arg_read=arg_read_local, arg_write=arg_write, index=0)

