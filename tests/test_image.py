from vaccel.session import Session
from vaccel.image import ImageClassify, ImageDetect, ImageSegment, ImagePose, ImageDepth

imgsource = "./libs/vaccelrt/examples/images/example.jpg"

def test_image_classify():
   ses = Session(flags=3)
   res = ImageClassify.classify_from_filename(session=ses, source=imgsource)
   assert res == ("This is a dummy classification tag!", 0)


def test_image_detect():
   ses = Session(flags=3)
   res = ImageDetect.detect_from_filename(session=ses, source=imgsource)
   assert res == 0


def test_image_segment():
   ses = Session(flags=3)
   res = ImageSegment.segment_from_filename(session=ses, source=imgsource)
   assert res == 0


def test_image_pose():
   ses = Session(flags=3)
   res = ImagePose.pose_from_filename(session=ses, source=imgsource)
   assert res == 0 # is this supposed to be 95?

def test_image_depth():
   ses = Session(flags=3)
   res = ImageDepth.depth_from_filename(session=ses, source=imgsource)
   assert res == 0 # is this supposed to be 95?