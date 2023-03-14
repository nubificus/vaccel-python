from vaccel.exec import Exec, Exec_with_resource
from vaccel.genop import VaccelArg

lib="/usr/local/lib/libvaccel-noop.so"
sym="mytestfunc"
myint: int = 1048576
mybytes: bytes = bytes(100 * " ", encoding="utf-8")

def test_exec_genop():
    res = Exec.exec(lib, sym, [VaccelArg(data=myint)], [VaccelArg(data=mybytes)])
    assert res == ("")

def test_exec_with_res_genop():
    res = Exec_with_resource.exec_with_resource(lib, sym, [VaccelArg(data=myint)], [VaccelArg(data=mybytes)])
    assert res == ("")