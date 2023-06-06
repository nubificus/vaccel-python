from vaccel.exec import Exec, Exec_with_resource
from vaccel.exec_many import Exec_with_many_resources
from vaccel.genop import VaccelArg

lib = "/usr/local/lib/libmytestlib.so"
object = "/usr/local/lib/libmytestlib.so"
sym = "mytestfunc"
arg_read = [1048576,12323,134366,1212]

arg_write = ['                              ']


# def test_exec_genop():
#     res = Exec.exec(lib, sym, arg_read, arg_write)
# #     assert res == ("")
# #     #assert res == ("I got this input: %d\n" % myint)


def test_exec_with_res():
    res = Exec_with_resource.exec_with_resource(object, sym, arg_read, arg_write)
    #assert res == ("")
    #assert res == ("I got this input: %d\n" % arg_read)

