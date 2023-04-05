from vaccel.exec import Exec, Exec_with_resource
from vaccel.genop import VaccelArg

lib = "/usr/local/lib/libmytestlib.so"
object = "/usr/local/lib/libmytestlib.so"
sym = "mytestfunc"

myint: int = 1048576
mybytes: bytes = bytes(100 * " ", encoding="utf-8")


def test_exec_genop():
    res = Exec.exec(lib, sym, [VaccelArg(data=myint)], [VaccelArg(data=mybytes)])
    assert res == ("")
    #assert res == ("I got this input: %d\n" % myint)


def test_exec_with_res():
    res = Exec_with_resource.exec_with_resource(object, sym, [VaccelArg(data=myint)], [VaccelArg(data=mybytes)])
    assert res == ("")
    #assert res == ("I got this input: %d\n" % myint)


def test_exec_with_res_genop():
    res = Exec_with_resource.exec_with_resource_genop(object, sym, [VaccelArg(data=myint)], [VaccelArg(data=mybytes)])
    assert res == ("")
