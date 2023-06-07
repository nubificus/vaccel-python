from vaccel.session import Session
from vaccel.noop import Noop
from vaccel.genop import Genop, VaccelArg
from vaccel.image import ImageClassify, ImageDetect, ImageSegment, ImagePose, ImageDepth
from vaccel.minmax import MinMax
from vaccel.exec import Exec, Exec_with_resource
from vaccel.sgemm import Sgemm
from vaccel.pynq_array_copy import Pynq_array_copy
from vaccel.pynq_parallel import Pynq_parallel
from vaccel.pynq_vector_add import Pynq_vector_add
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


imgsource = "/usr/local/share/images/example.jpg"
minmaxsource = "/usr/local/share/input/input_262144.csv"


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
    print("RESULT=", res)
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
    print('Min-Max over genop test')
    res = MinMax.minmax(indata=262144, ndata=minmaxsource, low_threshold=10, high_threshold=5000)
    print(res)
    print('')


def test_sgemm_genop():
    print('Sgemm over genop test')
    res = Sgemm.sgemm(m=512, n=512, k=512, alpha=32412.000000, lda=512, ldb=512, beta=2123.000000)
    print(res)
    print('')


def test_pynq_array_copy_genop():
    print('Pynq array copy over genop test')
    res = Pynq_array_copy.pynq_arr_copy(a=10)
    print(res)
    print('')


def test_pynq_parallel_genop():
    print('Pynq parallel over genop test')
    res = Pynq_parallel.pynq_parellel(a=1.0, len_a=3)
    print(res)
    print('')


def test_pynq_vector_add_genop():
    print('Pynq vector add over genop test')
    res = Pynq_vector_add.pynq_vector_add(len_a=5, len_b=5)
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

def test_exec_genop():
    print('Exec over genop test')
    myint: int = 1048576
    mybytes: bytes = bytes(100 * " ", encoding="utf-8")
    res = Exec.exec("/usr/local/lib/libmytestlib.so", "mytestfunc", [VaccelArg(data=myint)], [VaccelArg(data=mybytes)])
    print(res)
    print('')

def test_exec_with_resource():
    print('Exec with resource test')
    read_args = [1048576,12,32,43]
    write_args = ["                               ", "         "]
    mybytes: bytes = bytes(100 * " ", encoding="utf-8")
    res = Exec_with_resource.exec_with_resource("/usr/local/lib/libmytestlib.so", "mytestfunc", read_args, write_args)
    print(res)
    print('')


if __name__ == "__main__":
    test_exec_with_resource()
