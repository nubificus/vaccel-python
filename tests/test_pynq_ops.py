from vaccel.pynq_array_copy import Pynq_array_copy
from vaccel.pynq_parallel import Pynq_parallel
from vaccel.pynq_vector_add import Pynq_vector_add

def test_pynq_array_copy_genop():
    res = Pynq_array_copy.pynq_arr_copy(a=1)
    assert res

def test_pynq_parallel_genop():
    res = Pynq_parallel.pynq_parellel(a=1.0, len_a=1)
    assert res

def test_pynq_vector_add_genop():
    res = Pynq_vector_add.pynq_vector_add(len_a=1, len_b=1)
    assert res
