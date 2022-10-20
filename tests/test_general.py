from vaccel.session import Session
from vaccel.noop import Noop
from vaccel.genop import Genop, VaccelArg

def test_session():
    ses_a = Session(flags=0)
    ses_b = Session(flags=1)
    assert ses_a.id() != ses_b.id()

def test_noop():
    ses = Session(flags=0)
    res = Noop.noop(ses)
    assert res == 0

##def test_genop():
#    """
#    should work, but it doesn't because the sanity check on vAccel
#    regarding the number of arguments is not correct
#    """
#    ses = Session(flags=1)
#    arg_read = []
#    arg_read.append(VaccelArg(data=0))
#    arg_write = []
#    res = Genop.genop(ses, arg_read, arg_write)
#    assert res == 22 #should this be 22?
