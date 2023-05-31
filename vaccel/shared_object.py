from vaccel.session import Session
from typing import List, Any
from vaccel.genop import Genop, VaccelArg, VaccelOpType, VaccelArgList
from vaccel._vaccel import lib, ffi
import os

__hidden__ = list()

class Object:
    def __init__(self, obj):
        """Create a new vAccel object"""
        self.object = obj
        
    def __parse_object__(self) -> bytes:
        """Parses a shared object file and returns its content and size

        Args:
            obj: The path to the shared object file

        Returns:
            A tuple containing the content of the shared object file as bytes
            and its size as an integer

        Raises:
            TypeError: If object is not a string
        """
        filename = self
        obj = self
        if not isinstance(obj, str):
            raise TypeError(
                f"Invalid image type. Expected str or bytes, got {type(obj)}.")

        if isinstance(obj, str):
            with open(obj, "rb") as objfile:
                obj = objfile.read()

        size = os.stat(filename).st_size
        return obj, size

    def create_shared_object(self):
        """Creates a shared object from a file and returns a pointer to it

        Args:
            obj: The file path to the object file

        Returns:
            A pointer to the shared object
        """
        sharedobj, size = Object.__parse_object__(self)
        shared = ffi.new("struct vaccel_shared_object *")
        sharedobject = ffi.new("char[%d]" % size, sharedobj)
        __hidden__.append(sharedobject)
        sharedobject = ffi.cast("const void *", sharedobject)
        lib.vaccel_shared_object_new_from_buffer(shared, sharedobject, size)
        return shared


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
            __hidden__.append(sharedobject)
            sharedobject = ffi.cast("const void *", sharedobject)
            lib.vaccel_shared_object_new_from_buffer(shared, sharedobject, size)
            shared_objects.append(shared)
        return shared_objects
        
    
    def register_object(self,session):
        ret= lib.vaccel_sess_register(session._to_inner(), self.resource)
        return ret


    def object_symbol(self,symbol):
        symbolcdata = ffi.new(f"char[{len(symbol)}]",
                              bytes(symbol, encoding='utf-8'))
        return symbolcdata
