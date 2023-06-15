from enum import Enum
from dataclasses import dataclass
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
    VACCEL_MINMAX = 15
    VACCEL_PYNQ_ARR_COPY = 16
    # VACCEL_PYNQ_MMULT = 17
    VACCEL_PYNQ_PARALLEL = 18
    VACCEL_PYNQ_VECTOR_ADD = 19
    VACCEL_EXEC_WITH_RESOURCE = 20
    VACCEL_FUNCTIONS_NR = 21

    def __int__(self):
        return self.value


@dataclass
class VaccelOperationResult:
    """Class for returning the result and output of vAccel operations"""
    ret: int
    arg_write: List[bytes]
