from vaccel.session import Session
from typing import List
from vaccel.genop import VaccelArg, VaccelOpType, VaccelArgList
from vaccel._vaccel import lib, ffi
import os


class Object:
    def __init__(self):
        self.session = Session(flags=0)

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

    def create_shared_objects(objects: List[str]) -> List[str]:
        """Creates a list of shared objects
           from a list of file paths

        Args:
            objects: A list of file paths to the object files

        Returns:
            A list of pointers to the shared objects
        """
        shared_objects = []
        for obj in objects:
            sharedobj, size = Object.__parse_object__(obj)
            shared = ffi.new("struct vaccel_shared_object *")
            sharedobject = ffi.new("char[%d]" % size, sharedobj)
            sharedobject = ffi.cast("const void *", sharedobject)
            lib.vaccel_shared_object_new_from_buffer(shared, sharedobject, size)
            shared_objects.append(shared)
        return shared_objects


class Vaccel_Args:
    """
    A helper class for converting argument lists
    to the appropriate vAccel format
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


class Exec_with_many_resources(Object):
    """An Exec with resource model vAccel resource.

    Attributes:
        __op__: The genop operation type
    """

    __op__ = VaccelOpType.VACCEL_EXEC_WITH_RESOURCE

    @classmethod
    def exec_with_resources(self, objects: List[str], symbols: List[str], arg_read: List[int], arg_write: List[str]):
        """Performs the Exec using vAccel over genop.

        Args:
            object: Filename of a shared object to be used with vaccel exec
            symbol: Name of the function contained in the above shared object
            arg_read: A list of inputs

        Returns:
            arg_write: A list of outputs
        """
        session = Session(flags=0)
        shared_objects = self.create_shared_objects(objects)
        #vaccel_args_read = Vaccel_Args.vaccel_read_args(arg_read)
        #vaccel_args_write = Vaccel_Args.vaccel_write_args(arg_write)
        

        for shared, symbol, read in zip(shared_objects, symbols, arg_read):
            lib.vaccel_sess_register(session._to_inner(), shared.resource)
            symbolcdata = ffi.new(f"char[{len(symbol)}]",
                                  bytes(symbol, encoding='utf-8'))
            vaccel_args_read = Vaccel_Args.vaccel_read_args(read)
            vaccel_args_write = Vaccel_Args.vaccel_write_args(arg_write)
            nr_read = len(read)
            nr_write = len(arg_write)
            ret = lib.vaccel_exec_with_resource(session._to_inner(), shared, symbolcdata, vaccel_args_read, nr_read, vaccel_args_write, nr_write)
        #return arg_write[0].content
