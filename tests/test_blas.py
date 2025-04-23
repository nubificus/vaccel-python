import pytest

from vaccel import Session


@pytest.fixture
def test_data():
    m = n = k = 12
    return {
        "m": m,
        "n": n,
        "k": k,
        "alpha": 32412.000000,
        "a": [float(1)] * m * k,
        "lda": k,
        "b": [float(2)] * m * k,
        "ldb": n,
        "beta": 2123.000000,
        "ldc": n,
    }


def test_sgemm_genop(test_data):
    session = Session()
    session.sgemm(
        m=test_data["m"],
        n=test_data["n"],
        k=test_data["k"],
        alpha=test_data["alpha"],
        a=test_data["a"],
        lda=test_data["lda"],
        b=test_data["b"],
        ldb=test_data["ldb"],
        beta=test_data["beta"],
        ldc=test_data["ldc"],
    )
