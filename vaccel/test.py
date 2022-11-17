from contextlib import nullcontext
from vaccel.session import Session
from vaccel.noop import Noop
from vaccel.genop import Genop, VaccelArg, VaccelOpType
from vaccel.image import ImageClassify, ImageDetect, ImageSegment, ImagePose, ImageDepth
from vaccel.minmax import MinMax
from vaccel.sgemm import Sgemm
from vaccel import image_genop as genimg

def test_session():
    print("Session test")
    ses_a = Session(flags=0)
    ses_b = Session(flags=1)
    print(f'Session A id is {ses_a.id()} and Session B id is {ses_b.id()}')
    print('')

def test_noop():
    print("Noop test")
    ses = Session(flags=0)
    print(f'Session id is {ses.id()}')
    res = Noop.noop(ses)
    print(res)
    print('')

imgsource = "./libs/vaccelrt/examples/images/example.jpg"
csvsource = "./input_262144.csv"

def test_genop():
    """
    should work, but it doesn't because the sanity check on vAccel
    regarding the number of arguments is not correct
    """
    print("Genop test")
    ses = Session(flags=1)
    print(f'Session id is {ses.id()}')

    arg_read = []
    arg_read.append(VaccelArg(data=0))

    arg_write = []

    res = Genop.genop(ses, arg_read, arg_write)
    print("RESULT=" ,res)
    print('')

def test_image_class_genop():
    print('Image classify over genop test')
    res = genimg.ImageClassify.classify(image=imgsource)
    print(res)
    print('')

def test_image_detect_genop():
    print('Image detection over genop test')
    res = genimg.ImageDetect.detect(image=imgsource)
    print(res)
    print('')

def test_image_segme_genop():
    print('Image segmentation over genop test')
    res = genimg.ImageSegment.segment(image=imgsource)
    print(res)
    print('')

def test_image_pose_genop():
    print('Image pose over genop test')
    res = genimg.ImagePose.pose(image=imgsource)
    print(res)
    print('')

def test_image_depth_genop():
    print('Image depth over genop test')
    res = genimg.ImageDepth.depth(image=imgsource)
    print(res)
    print('')

def test_min_max_genop():
    print('Min-Max test')
    res = MinMax.minmax(indata=262144, ndata=csvsource, low_threshold=10, high_threshold=5000)
    print(res)
    print('')

def test_sgemm_genop():
    print('Sgemm test')
    res = Sgemm.sgemm(m=512, n=512, k=512, alpha=32412.000000, lda=512, ldb=512, beta=2123.000000)
    print(res)
    print('')

def test_image_classify():
    print("Image classify test")
    ses = Session(flags=3)
    print(f'Session id is {ses.id()}')
    res = ImageClassify.classify_from_filename(session=ses, source=imgsource)
    print(res)
    print('')

def test_image_detect():
    print("Image detect test")
    ses = Session(flags=3)
    print(f'Session id is {ses.id()}')
    res = ImageDetect.detect_from_filename(session=ses, source=imgsource)
    print(res)
    print('')

def test_image_segment():
    print("Image segment test")
    ses = Session(flags=3)
    print(f'Session id is {ses.id()}')
    res = ImageSegment.segment_from_filename(session=ses, source=imgsource)
    print(res)
    print('')

def test_image_pose():
    print("Image pose test")
    ses = Session(flags=3)
    print(f'Session id is {ses.id()}')
    res = ImagePose.pose_from_filename(session=ses, source=imgsource)
    print(res)
    print('')

def test_image_depth():
    print("Image depth test")
    ses = Session(flags=3)
    print(f'Session id is {ses.id()}')
    res = ImageDepth.depth_from_filename(session=ses, source=imgsource)
    print(res)
    print('')

if __name__=="__main__":
    test_session()
    test_noop()
    #test genop image operations
    test_image_class_genop()
    test_image_detect_genop()
    test_image_segme_genop()
    test_image_pose_genop()
    test_image_depth_genop()
    test_min_max_genop()
    test_sgemm_genop()
    #test static image operations
    test_image_classify()
    test_image_detect()
    test_image_segment()
    test_image_pose()
    test_image_depth()
