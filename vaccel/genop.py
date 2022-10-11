from enum import Enum
from vaccel._vaccel import lib, ffi

from vaccel.session import Session
from typing import List


class VaccelOpType(Enum):
    VACCEL_NO_OP = 0
    VACCEL_BLAS_SGEMM = 1
    VACCEL_IMG_CLASS = 2
    VACCEL_IMG_DETEC = 3
    VACCEL_IMG_SEGME = 4
    VACCEL_IMG_POSE = 5
    VACCEL_IMG_DEPTH = 6
    VACCEL_EXEC = 7
    VACCEL_TF_MODEL_NEW = 8
    VACCEL_TF_MODEL_DESTROY = 9
    VACCEL_TF_MODEL_REGISTER = 10
    VACCEL_TF_MODEL_UNREGISTER = 11
    VACCEL_TF_SESSION_LOAD = 12
    VACCEL_TF_SESSION_RUN = 13
    VACCEL_TF_SESSION_DELETE = 14
    VACCEL_FUNCTIONS_NR = 15
    VACCEL_MINMAX = 16

    def __int__(self):
        return self.value


class VaccelArg:
    def __init__(self, data) -> None:
        self.buf = data
        self.info = VaccelArgInfo.from_vaccel_arg(self)
        self.size = self.info.datasize
        self.__hidden__ = []

    def to_cffi(self):
        arg1buf = None
        if self.info.datatype == "int":
            arg1buf = ffi.new("int *", self.buf)

        if self.info.datatype == "char []":
            arg1buf = ffi.new(f"char[{len(self.buf)}]",
                              bytes(self.buf, encoding='utf-8'))

        if self.info.datatype == "bytes":
            arg1buf = ffi.from_buffer(self.buf)

        if self.info.datatype == "float":
            arg1buf = ffi.new("float *", self.buf)

        # TODO Handle double data type
        if self.info.datatype == "double":
            arg1buf = ffi.new("double *", self.buf)      

        self.__hidden__.append(arg1buf)
        buf = ffi.cast("void *", arg1buf)
        arg = ffi.new("struct vaccel_arg []", 1)

        # hack to keep memory alive
        self.__hidden__.append(arg)
        arg[0].size = self.size
        arg[0].buf = buf

        return arg[0]

    @property
    def content(self):
        return str(self.buf, encoding='utf-8').strip().rstrip('\x00')


class VaccelArgInfo:
    def __init__(self, datatype="", datasize="") -> None:
        self.datatype = datatype
        self.datasize = datasize

    @staticmethod
    def detect_datatype(arg: VaccelArg) -> str:
        datatype = "void"
        if isinstance(arg.buf, int):
            datatype = "int"
        if isinstance(arg.buf, str):
            datatype = "char []"
        if isinstance(arg.buf, float):
            datatype = "float"
        if isinstance(arg.buf, bytes):
            datatype = "bytes"
        #if isinstance(arg.buf, double):
        #   datatype = "double"
        if "cdata" in str(arg.buf).lower():
            datatype = "cdata"
        return datatype

    @classmethod
    def from_vaccel_arg(cls, arg: VaccelArg):
        datatype = VaccelArgInfo.detect_datatype(arg)

        if datatype == "int":
            temp = ffi.new("int *", arg.buf)
        if datatype == "char []":
            temp = ffi.new("char []", bytes(arg.buf, encoding="utf-8"))
        if datatype == "float":
            temp = ffi.new("float *", arg.buf)
            temp = ffi.new(f"float *", arg.buf)
        if datatype == "double":
            temp = ffi.cast("double *", arg.buf)
        if datatype == "cdata":
            temp = arg.buf
        if datatype == "bytes":
            temp = ffi.from_buffer(arg.buf)
        if datatype == "void":
            temp1 = ffi.new("char []", bytes(arg.buf, encoding="utf-8"))
            temp = ffi.cast(temp1)
        datasize = ffi.sizeof(temp)
        return cls(datatype=datatype, datasize=datasize)

class VaccelArgList:
    def __init__(self, args: List[VaccelArg]) -> None:
        self.args = args
        self.__hidden__ = []

    def to_cffi(self):
        temp = []
        for arg in self.args:
            this = arg.to_cffi()
            temp.append(this)
        final = ffi.new("struct vaccel_arg[]", temp)

        # hack to keep memory alive
        self.__hidden__.append(final)

        return final


class Genop:
    def __init__(self):
        """exec vAccel Genop"""
        print("test init")

    def __del__(self):
        print("test del")

    @classmethod
    def genop(self, session: Session, arg_read: List[VaccelArg], arg_write: List[VaccelArg]) -> List[str]:
        """exec the operation"""
        csession = session._to_inner()

        nr_read = len(arg_read)
        nr_write = len(arg_write)

        vaccel_args_read = VaccelArgList(arg_read).to_cffi()
        vaccel_args_write = VaccelArgList(arg_write).to_cffi()

        ret = lib.vaccel_genop(csession, vaccel_args_read, nr_read,
                               vaccel_args_write, nr_write)
        # if ret != 0:
        #    raise VaccelError(ret, "Could not execute generic operation")

        return ret
