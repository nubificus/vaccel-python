from vaccel.minmax import MinMax

imgsource = "/usr/local/share/images/example.jpg"

def test_min_max_genop():
    res = MinMax.minmax(indata=262144, ndata=imgsource, low_threshold=10, high_threshold=5000)
    assert res