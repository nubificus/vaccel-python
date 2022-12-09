from vaccel.session import Session
from typing import List
from vaccel.genop import Genop, VaccelArg, VaccelOpType
import struct
import copy

class MinMax:

    def_arg_write: float = bytes(100 * " ", encoding="utf-8")

    __op__ = VaccelOpType.VACCEL_MINMAX

    @staticmethod
    def __genop__(arg_read: List[VaccelArg], arg_write: List[VaccelArg], index: int) -> str:
        """
        Performs the genop operation provided in arg_read.

        Returns the content of the arg_write indicated by index.
        """
        ses = Session(flags=0)
        Genop.genop(ses, arg_read, arg_write)
        return struct.unpack('d', arg_write[index].raw_content[:8])[0]

    @staticmethod
    def __parse_ndata__(ndata: "str | bytes") -> bytes:
        if not isinstance(ndata, str) and not isinstance(ndata, bytes):
            raise TypeError(
                f"Invalid ndata type. Expected str or bytes, got {type(ndata)}.")

        if isinstance(ndata, str):
            with open(ndata, "rb") as ndatafile:
                ndata = ndatafile.read()

        return ndata

    @classmethod
    def minmax(self, indata: int, ndata: "str | bytes", low_threshold: "int", high_threshold: "int"):
        """
        MinMax using vAccel over genop

        Parameters:
            indata: float
            ndata (str | bytes): str or bytes object of the ndata
            low_theshold: int 
            high_threshold: int

        Returns:
            outdata, min, max: float 
        """
        #indata = double(indata)
        ndata = self.__parse_ndata__(ndata=ndata)
        arg_read = [VaccelArg(data=int(self.__op__)),
                    VaccelArg(data=ndata),
                    VaccelArg(data=indata),
                    VaccelArg(data=low_threshold),
                    VaccelArg(data=high_threshold)]
        
        arg_write = [VaccelArg(data=self.def_arg_write), VaccelArg(data=copy.deepcopy(self.def_arg_write)), VaccelArg(data=copy.deepcopy(self.def_arg_write))]
        return self.__genop__(arg_read=arg_read, arg_write=arg_write, index=1)


"""int vaccel_minmax(struct vaccel_session *sess,
        const double *indata, int ndata,
        int low_threshold, int high_threshold,
        double *outdata,
        double *min, double *max);
"""
