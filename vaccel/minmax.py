from vaccel.session import Session
from typing import List
from vaccel.genop import Genop, VaccelArg, VaccelOpType
import struct
import copy

class MinMax:
    """A MinMax model vAccel resource.
    
    Attributes:
        def_arg_write (bytes): The result of the operation
        __op__: The genop operation type
    """

    def_arg_write: float = bytes(100 * " ", encoding="utf-8")

    __op__ = VaccelOpType.VACCEL_MINMAX

    @staticmethod
    def __genop__(arg_read: List[VaccelArg], arg_write: List[VaccelArg], index: int) -> str:
        """Performs the genop operation provided in arg_read.

        Args:
            arg_read : `list`
            arg_write : `list`
            index : `int`

        Returns:
            The content of the `arg_write` indicated by `index`.
        """
        ses = Session(flags=0)
        Genop.genop(ses, arg_read, arg_write)
        return struct.unpack('d', arg_write[index].raw_content[:8])[0]

    @staticmethod
    def __parse_ndata__(ndata: "str | bytes") -> bytes:
        """Reads data from file.

        Args:
            ndata : A string or bytes object 

        Returns:
            Returns image file content.

        Raises:
            TypeError: If ndata object is not a string or bytes object
        """
        if not isinstance(ndata, str) and not isinstance(ndata, bytes):
            raise TypeError(
                f"Invalid ndata type. Expected str or bytes, got {type(ndata)}.")

        if isinstance(ndata, str):
            with open(ndata, "rb") as ndatafile:
                ndata = ndatafile.read()

        return ndata

    @classmethod
    def minmax(self, indata: int, ndata: "str | bytes", low_threshold: "int", high_threshold: "int"):
        """Performs the MinMax operation using vAccel over genop.

        Args:
            indata: An integer giving the number of inputs
            ndata: A string or bytes object containing the ndata file path
            low_theshold: An integer value for low threshold
            high_threshold: An integer value for high threshold

        Returns:
            outdata: A float number containing the outdata
            min: A float number for the min value
            max: A float number for the max value 
        """
        ndata = self.__parse_ndata__(ndata=ndata)
        arg_read = [VaccelArg(data=int(self.__op__)),
                    VaccelArg(data=ndata),
                    VaccelArg(data=indata),
                    VaccelArg(data=low_threshold),
                    VaccelArg(data=high_threshold)]
        
        arg_write = [VaccelArg(data=self.def_arg_write), VaccelArg(data=copy.deepcopy(self.def_arg_write)), VaccelArg(data=copy.deepcopy(self.def_arg_write))]
        return self.__genop__(arg_read=arg_read, arg_write=arg_write, index=1)
