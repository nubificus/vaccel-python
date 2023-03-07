from vaccel.session import Session
from typing import List
from vaccel.genop import Genop, VaccelArg, VaccelOpType
from vaccel._vaccel import lib, ffi

class Exec_Operation:
    """An Image Operation model vAccel resource
    
    Attributes:
        def_arg_write (bytes): The result of the operation
    """

    def_arg_write: bytes = bytes(100 * " ", encoding="utf-8")

    @staticmethod
    def __genop__(arg_read: List[VaccelArg], arg_write: List[VaccelArg], index: int) -> str:
        """Performs the genop operation provided in arg_read.
        
        Args:
            arg_read : A list of inputs
            arg_write : A list of outputs
            index : An integer

        Returns:
            The content of the `arg_write` indicated by `index`.
        """
        ses = Session(flags=0)
        Genop.genop(ses, arg_read, arg_write)
        return arg_write[index].content

class Exec(Exec_Operation):
    """An Exec model vAccel resource.

    Attributes:
        __op__: The genop operation type
    """

    __op__ = VaccelOpType.VACCEL_EXEC

    @classmethod
    def exec(self, library: str, symbol: str, arg_read: List[VaccelArg], arg_write: List[VaccelArg]) -> str:
        """Performs the Exec using vAccel over genop.

        Args:
            library: Path to the shared object containing the function that the user wants to call
            symbol: Name of the function contained in the above shared object
            arg_read: A list of inputs

        Returns:
            arg_write: A list of outputs
        """

        arg_read_local = [VaccelArg(data=int(self.__op__)),
                    VaccelArg(data=library),VaccelArg(data=symbol)] + arg_read
        arg_write = [VaccelArg(data=bytes(100 * " ", encoding="utf-8"))]
        return self.__genop__(arg_read=arg_read_local, arg_write=arg_write, index=0)


class Exec_with_resource(Exec_Operation):
    """An Exec with resource model vAccel resource.

    Attributes:
        __op__: The genop operation type
    """

    __op__ = VaccelOpType.VACCEL_EXEC_WITH_RESOURCE

    @classmethod
    def exec_with_resource(self, object: str, symbol: str, arg_read: List[VaccelArg], arg_write: List[VaccelArg]) -> str:
        """Performs the Exec using vAccel over genop.

        Args:
            object: pointer to a `shared object`-type vaccel resource
            symbol: Name of the function contained in the above shared object
            arg_read: A list of inputs

        Returns:
            arg_write: A list of outputs
        """ 

        #my_object = ffi.cast("struct vaccel_shared_object *",object)

        arg_read_local = [VaccelArg(data=int(self.__op__)),
                    VaccelArg(data=object),VaccelArg(data=symbol)] + arg_read
        arg_write = [VaccelArg(data=bytes(100 * " ", encoding="utf-8"))]
        return self.__genop__(arg_read=arg_read_local, arg_write=arg_write, index=0)


"""
int vaccel_exec(struct vaccel_session *sess, const char *library,
                const char *fn_symbol, struct vaccel_arg *read,
                size_t nr_read, struct vaccel_arg *write, size_t nr_write);
"""

"""
int vaccel_exec_with_resource(struct vaccel_session *sess, struct vaccel_shared_object *object,
		     const char *fn_symbol, struct vaccel_arg *read,
		     size_t nr_read, struct vaccel_arg *write, size_t nr_write);
"""