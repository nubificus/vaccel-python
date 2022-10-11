from vaccel.session import Session
from typing import List
from vaccel.genop import Genop, VaccelArg, VaccelOpType

class MinMax:

    def_arg_write: bytes = bytes(100 * " ", encoding="utf-8")

    __op__ = VaccelOpType.VACCEL_MINMAX

    @staticmethod
    def __genop__(arg_read: List[VaccelArg], arg_write: List[VaccelArg], index: int) -> str:
        """
        Performs the genop operation provided in arg_read.

        Returns the content of the arg_write indicated by index.
        """
        ses = Session(flags=0)
        Genop.genop(ses, arg_read, arg_write)
        return arg_write[index].content

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
    def minmax(self, indata: "float", ndata: "str | bytes", low_threshold: "int", high_threshold: "int"):
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
        ndata = self.__parse_ndata__(ndata=ndata)
        arg_read = [VaccelArg(data=int(self.__op__)),
                    VaccelArg(data=indata),
                    VaccelArg(data=ndata),
                    VaccelArg(data=low_threshold),
                    VaccelArg(data=high_threshold)]
        arg_write = [VaccelArg(data=self.def_arg_write)]*2
        return self.__genop__(arg_read=arg_read, arg_write=arg_write, index=0)


"""int vaccel_minmax(struct vaccel_session *sess,
        const double *intdata, int ndata,
        int low_threshold, int high_threshold,
        double *outdata,
        double *min, double *max);
"""