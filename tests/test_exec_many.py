from vaccel.exec_many import Exec_with_many_resources
from vaccel.genop import VaccelArg

object = ("/usr/local/lib/libmytestlib.so", "/usr/local/lib/libmytestlib.so", "/usr/local/lib/libmytestlib.so")
sym = ("mytestfunc", "mytestfunc2", "mytestfunc3")
arg_read = ([1,2,3,4],[1,2],[1,2,3,4,5])
mybytes: bytes = bytes(100 * " ", encoding="utf-8")
arg_write = ['     ', '       ', '          ', '           ']

#def test_exec_with_res():
#    print(type(object))
#    print(type(sym))
#    print(type(arg_read))
#    res = Exec_with_many_resources.exec_with_resources(object, sym, arg_read, arg_write)
#    #assert res == ("")
