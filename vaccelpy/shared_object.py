import os
from typing import Union

from vaccel._vaccel import ffi, lib
from vaccel.error import VaccelError


class VaccelObject:
    def __init__(self, object: Union[str, bytes], symbol: str):
        if not isinstance(object, str) and not isinstance(object, bytes):
            raise TypeError(
                f"Invalid object type. Expected 'str' or 'bytes', got '{type(object)}'.")
        if isinstance(object, str):
            with open(object, "rb") as objfile:
                self.contents = objfile.read()
            self.size = os.stat(object).st_size
        if isinstance(object, bytes):
            self.contents = object
            self.size = len(object)

        self.cobject = ffi.new("struct vaccel_shared_object*")
        ret = lib.vaccel_shared_object_new_from_buffer(
            self.cobject, ffi.from_buffer(self.contents), self.size)
        if ret != 0:
            raise VaccelError(
                ret, "Could not create shared object from buffer")

        self.symbol = symbol
        self.csymbol = ffi.new(
            f"char[{len(symbol)}]", bytes(symbol, encoding='utf-8'))

    def __del__(self):
        ffi.release(self.cobject)
        ffi.release(self.csymbol)
        ret = lib.vaccel_shared_object_destroy(self.cobject)
        if ret != 0:
            raise VaccelError(
                ret, "Could not delete shared objects")

    @property
    def resource(self):
        return self.cobject.resource

    def destroy(self):
        ret = lib.vaccel_shared_object_destroy(self.cobject)
        if ret != 0:
            raise VaccelError(ret, "Could not destroy shared object")
