from vaccel.session import Session
from typing import List, Any
from vaccel.genop import Genop, VaccelArg, VaccelOpType, VaccelArgList
from vaccel._vaccel import lib, ffi
import os
import pdb

__hidden__ = list()

class Object:
    def __init__(self,session,obj,symbol):
        """Create a new vAccel object"""
        self.filename = obj
        self.path,self.size = self.__parse_object__(obj)
        self.shared = self.create_shared_object()
        self.register = self.register_object(self.shared,session)
        self.unregister = self.unregister_object(self.shared,session)
        self.symbol = self.object_symbol(symbol)
        
    def many_objects(self,obj):
        self.my_list = []
        for i in obj :
            # self.path, self.size = self.__parse_object__(i)
            self.my_list.append(i)
        objects = self.my_list
        return objects

    def __parse_object__(self,obj) -> bytes:
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


    def create_shared_object(self):
        """Creates a shared object from a file and returns a pointer to it

        Args:
            obj: The file path to the object file

        Returns:
            A pointer to the shared object
        """
        sharedobj, size = self.path, self.size
        shared = ffi.new("struct vaccel_shared_object *")
        sharedobject = ffi.new("char[%d]" % size, sharedobj)
        __hidden__.append(sharedobject)
        sharedobject = ffi.cast("const void *", sharedobject)
        lib.vaccel_shared_object_new_from_buffer(shared, sharedobject, size)
        return shared
    
    def register_object(self,shared,session):
        ret= lib.vaccel_sess_register(session._to_inner(), shared.resource)
        return ret


    def unregister_object(self,shared,session):
        ret= lib.vaccel_sess_unregister(session._to_inner(), shared.resource)
        return ret


    def object_symbol(self,symbol):
        symbolcdata = ffi.new(f"char[{len(symbol)}]",
                              bytes(symbol, encoding='utf-8'))
        return symbolcdata
