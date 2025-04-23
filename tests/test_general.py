from vaccel import Session


def test_session():
    ses_a = Session(flags=0)
    ses_b = Session(flags=1)
    assert ses_b.id == ses_a.id + 1


def test_noop():
    session = Session(flags=0)
    session.noop()
