from vaccel import image_genop as genimg

imgsource = "./libs/vaccelrt/examples/images/example.jpg"

def test_image_class_genop():
    res = genimg.ImageClassify.classify(image=imgsource)
    assert res == ("This is a dummy classification tag!")

def test_image_detect_genop():
    res = genimg.ImageDetect.detect(image=imgsource)
    assert res == ("This is a dummy classification tag!")

def test_image_segme_genop():
    res = genimg.ImageSegment.segment(image=imgsource)
    assert res == ("This is a dummy classification tag!")

def test_image_pose_genop():
    res = genimg.ImagePose.pose(image=imgsource)
    assert res == ("This is a dummy classification tag!")

def test_image_depth_genop():
    res = genimg.ImageDepth.depth(image=imgsource)
    assert res == ("This is a dummy classification tag!")

