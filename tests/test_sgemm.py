from vaccel.sgemm import Sgemm

def test_sgemm_genop():
    res = Sgemm.sgemm(m=512, n=512, k=512, alpha=32412.000000, lda=512, ldb=512, beta=2123.000000)
    assert res == ("")