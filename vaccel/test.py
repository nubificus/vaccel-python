from vaccel.session import Session
from vaccel.noop import Noop
from vaccel.genop import Genop, VaccelArg, VaccelOpType
from vaccel._vaccel import ffi


def test_session():
    print("Session test")
    ses_a = Session(flags=0)
    ses_b = Session(flags=1)
    print(f'Session A id is {ses_a.id()} and Session B id is {ses_b.id()}')
    print("")

def test_noop():
    print("Noop test")
    ses = Session(flags=0)
    print(f'Session id is {ses.id()}')
    res = Noop.noop(ses)
    print(res)
    print("")

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

def test_genop_classify():
    print("Genop test")
    ses = Session(flags=1)
    source = "img.jpg"
    print(f'Session id is {ses.id()}')

    arg_read = []
    with open(source, "rb") as imgfile:
        data = imgfile.read()
    arg_read.append(VaccelArg(data=2))
    arg_read.append(VaccelArg(data=data))

    arg_write = []
    #out_text = 100 * "a"
    out_text = bytes(100 * " ", encoding = "utf-8")
    out_imagename = bytes(100 * " ", encoding = "utf-8")
    arg_write.append(VaccelArg(data=out_text))
    arg_write.append(VaccelArg(data=out_imagename))

    res = Genop.genop(ses, arg_read, arg_write) 
    print("RESULT=" ,res)
    for i in range(len(arg_write)):
        print(arg_write[i].buf)

def test_genop_detect():
    print("Genop test")
    ses = Session(flags=1)
    source = "img.jpg"
    print(f'Session id is {ses.id()}')

    arg_read = []
    with open(source, "rb") as imgfile:
        data = imgfile.read()
    arg_read.append(VaccelArg(data=3))
    arg_read.append(VaccelArg(data=data))

    arg_write = []
    #out_text = 100 * "a"
    out_imagename = bytes(100 * " ", encoding = "utf-8")
    arg_write.append(VaccelArg(data=out_imagename))

    res = Genop.genop(ses, arg_read, arg_write) 
    print("RESULT=" ,res)
    for i in range(len(arg_write)):
        print(arg_write[i].buf)

if __name__=="__main__":
    test_session()
    test_noop()
    #test_genop()
    test_genop_classify()
    test_genop_detect()
