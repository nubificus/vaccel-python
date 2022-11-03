from vaccel.session import Session
from vaccel.noop import Noop


def test_session():
    ses_a = Session(flags=0)
    ses_b = Session(flags=1)
    assert ses_a.id() != ses_b.id()


def test_noop():
    ses = Session(flags=0)
    res = Noop.noop(ses)
    assert res == 0
