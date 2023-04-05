from vaccel.exec_many import Exec_with_many_resources
from vaccel.genop import VaccelArg


object = ("/usr/local/lib/libmytestlib.so", "/usr/local/lib/libvaccel-noop.so", "/usr/local/lib/libvaccel-exec.so")
sym = ("mytestfunc", "mytestfunc2", "mytestfunc3")
myint: int = 1048576
mybytes: bytes = bytes(100 * " ", encoding="utf-8")


def test_exec_with_res():
    res = Exec_with_many_resources.exec_with_resources(object, sym, [VaccelArg(data=myint)], [VaccelArg(data=mybytes)])
    assert res == ("")
