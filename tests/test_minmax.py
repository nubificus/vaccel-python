from vaccel.minmax import MinMax

source = "/usr/local/share/vaccel/input/input_2048.csv"

def test_min_max_genop():
    res = MinMax.minmax(indata=2048, ndata=source, low_threshold=10, high_threshold=5000)
    #assert res[1] == 10000.0 and res[2] == -1.0
    assert res[2] == 10000.0 and res[1] == -1.0
