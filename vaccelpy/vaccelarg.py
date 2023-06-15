from vaccel._vaccel import lib, ffi
import sys
import numpy as np


# __hidden__ = list()


class VaccelArg:

    def __init__(self, value):
        self._vaccel_arg = ffi.new("struct vaccel_arg*")
        self.input = value
        self.size, self.buf, self.dtype = self.get_buffer_info(value)

    def get_buffer_info(self, value):
        dtype = None
        if isinstance(value, int):
            print(value, "int")
            buf = ffi.new("int*", value)
            # __hidden__.append(buf)
            size = ffi.sizeof("int")
            dtype = "int"
        elif isinstance(value, float):
            print(value, "float")
            buf = ffi.new("double*", value)
            # __hidden__.append(buf)
            size = ffi.sizeof("double")
            dtype = "float"
        elif isinstance(value, str):
            print(value, "str")
            buf = ffi.new("char[]", value.encode("utf-8"))
            # __hidden__.append(buf)
            size = sys.getsizeof(value) - sys.getsizeof("") + 1
            dtype = "str"
        elif isinstance(value, bytes):
            print(value, "bytes")
            buf = ffi.new("char[]", value)
            # __hidden__.append(buf)
            size = len(value)
            dtype = "bytes"
        elif isinstance(value, bytearray):
            print(value, "bytearry")
            # buf = ffi.new("char[]", bytes(value))
            buf = ffi.from_buffer(value)
            # __hidden__.append(buf)
            size = len(value)
            dtype = "bytearray"
        # elif isinstance(value, list) or isinstance(value, numpy.ndarray):
        elif isinstance(value, list):
            print(value, "list")
            buf = ffi.new("char[]", bytes(value))
            size = len(value)
            dtype = "list"
        elif isinstance(value, np.ndarray):
            print("Numpy type:", value.dtype)
            dtype = "np.ndarray"
            if value.dtype == np.int32:
                buf = ffi.cast("int*", value.ctypes.data)
                size = value.nbytes
                dtype += "_int32"
            elif value.dtype == np.float32:
                # buf = ffi.cast("double*", value.ctypes.data)
                buf = ffi.cast("float*", value.ctypes.data)
                size = value.nbytes
                dtype += "_float32"
            elif value.dtype == np.float64:
                buf = ffi.cast("double*", value.ctypes.data)
                size = value.nbytes
                dtype += "_float64"
            else:
                raise ValueError("Unsupported numpy array data type")
        else:
            print("WTF")
            print(value)
            print("WTF2")
            print(value, "WTF")
            raise ValueError("Unsupported data type")

        print(buf, size)
        return size, buf, dtype

    @property
    def size(self):
        return self._vaccel_arg.size

    @size.setter
    def size(self, value):
        self._vaccel_arg.size = value

    @property
    def buf(self):
        return ffi.cast("char*", self._vaccel_arg.buf)

    @buf.setter
    def buf(self, value):
        self._vaccel_arg.buf = ffi.cast("void*", value)

    @property
    def value(self):
        output_buffer = ffi.buffer(
            self.buf, self.size)
        # import pdb
        # pdb.set_trace()
        output_data = bytes(output_buffer)
        return output_data

    @property
    def native(self):
        if self.dtype == "int":
            return int.from_bytes(self.value, byteorder='little', signed=True)
        if "np.ndarray" in self.dtype:
            return self.input


def create_vaccel_arg_array(args):
    arg_array = ffi.new("struct vaccel_arg[]", len(args))
    for i, arg in enumerate(args):
        arg_array[i].size = arg.size
        arg_array[i].buf = arg.buf

    return arg_array
