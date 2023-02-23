from vaccel.session import Session
from typing import List
from vaccel.genop import Genop, VaccelArg, VaccelOpType, VaccelArgList
from vaccel._vaccel import lib, ffi
import os


class Object:
    def __parse_object__(obj: "str") -> bytes:
        """Parses a shared object file and returns its content and size

        Args:
            obj: The path to the shared object file

        Returns:
            A tuple containing the content of the shared object file as bytes
            and its size as an integer

        Raises:
            TypeError: If object is not a string
        """
        filename = obj
        if not isinstance(obj, str):
            raise TypeError(
                f"Invalid image type. Expected str or bytes, got {type(obj)}.")

        if isinstance(obj, str):
            with open(obj, "rb") as objfile:
                obj = objfile.read()

        size = os.stat(filename).st_size
        return obj, size

    def create_shared_object(obj: str):
        """Creates a shared object from a file and returns a pointer to it

        Args:
            obj: The file path to the object file

        Returns:
            A pointer to the shared object
        """
        sharedobj, size = Object.__parse_object__(obj)
        shared = ffi.new("struct vaccel_shared_object *")
        sharedobject = ffi.new("char[%d]" % size, sharedobj)
        sharedobject = ffi.cast("const void *", sharedobject)
        lib.vaccel_shared_object_new_from_buffer(shared, sharedobject, size)
        return shared


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
        return arg_write[index].content


class Vaccel_Args:
    """
    A helper class for converting argument lists to the appropriate vAccel format
    """

    @staticmethod
    def vaccel_read_args(args: List[int]) -> List[VaccelArg]:
        """Convert a list of integers to a list of VaccelArg objects

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

    @staticmethod
    def vaccel_write_args(args: List[bytes]) -> List[VaccelArg]:
        """Convert a list of bytes to a list of VaccelArg objects

        Args:
            args : A list of bytes

       Returns:
            A list of VaccelArg objects
        """
        args = [VaccelArg(data=bytes(100 * " ", encoding="utf-8"))]
        return VaccelArgList(args).to_cffi()


class Exec(Exec_Operation):
    """An Exec operation model vAccel resource

    Attributes:
        __op__: The genop operation type
    """

    __op__ = VaccelOpType.VACCEL_EXEC

    @classmethod
    def exec(self, library: str, symbol: str, arg_read: List[int], arg_write: List[str]):
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
    def exec_with_resource(self, obj: str, symbol: str, arg_read: List[int], arg_write: list[bytes]):
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
        vaccel_args_read = Vaccel_Args.vaccel_read_args(arg_read)
        vaccel_args_write = Vaccel_Args.vaccel_write_args(arg_write)
        nr_read = len(arg_read)
        nr_write = len(arg_write)

        symbolcdata = ffi.new(f"char[{len(symbol)}]",
                              bytes(symbol, encoding='utf-8'))

        lib.vaccel_sess_register(session._to_inner(), shared.resource)
        ret = lib.vaccel_exec_with_resource(session._to_inner(), shared, symbolcdata, vaccel_args_read, nr_read, vaccel_args_write, nr_write)
        #return arg_write[0].content

    @classmethod
    def exec_with_resource_genop(self, obj: str, symbol: str, arg_read: List[int], arg_write: list[bytes]) -> str:
        """Performs the Exec using vAccel over genop

        Args:
            object: Filename of a shared object to be used with vaccel exec
            symbol: Name of the function contained in the above shared object
            arg_read: A list of inputs

        Returns:
            arg_write: A list of outputs
        """

        session = Session(flags=0)
        shared = self.create_shared_object(obj)
        rid = lib.vaccel_shared_object_get_id(shared)
        
        #vaccel_args_read = Vaccel_Args.vaccel_read_args(arg_read)
        arg_read_local = [VaccelArg(data=int(self.__op__)),
                          VaccelArg(data=rid), VaccelArg(data=symbol)] + arg_read
        arg_write = [VaccelArg(data=bytes(100 * " ", encoding="utf-8"))]
        return self.__genop__(session, arg_read=arg_read_local, arg_write=arg_write, index=0)
