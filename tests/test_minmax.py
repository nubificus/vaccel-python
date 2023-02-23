from vaccel.minmax import MinMax

source = "/usr/local/share/input/input_262144.csv"

def test_min_max_genop():
    res = MinMax.minmax(indata=262144, ndata=source, low_threshold=10, high_threshold=5000)
    assert res[1] == 10000.0 and res[2] == -1.0
