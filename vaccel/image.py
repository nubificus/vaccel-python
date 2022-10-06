from vaccel._vaccel import lib, ffi
from vaccel.error import VaccelError
from vaccel.session import Session
from typing import List

import cffi
ffi = cffi.FFI()


class ImageClassify:
    """An ImageClassify model vAccel resource"""

    out_size = 500

    def __init__(self):
        """Create an ImageClassify model resource"""
        print("test init")

    def __del__(self):
        """Destroy a vAccel ImageClassify model"""
        print("test del")

    @classmethod
    def __classify__(self, session: Session, data: List[int]) -> str:
        """Execute image classification operation"""
        csession = session._to_inner()

        img = ffi.cast("const void *",data)

        out_text = ffi.new(f"unsigned char[{self.out_size}]")

        out_imgname = ffi.NULL
        len_img = len(data)

        len_out_text = self.out_size
        len_out_imgname = 0

        ret = lib.vaccel_image_classification(csession, img, out_text, out_imgname, len_img, len_out_text, len_out_imgname)
        if ret != 0:
            raise VaccelError(ret, "Could not execute image classification operation")

        out_res = "".join([chr(i) for i in out_text]).rstrip('\x00')

        return out_res

    @classmethod
    def classify_from_filename(self, session: Session, source: str) -> str:
        """Initialize an ImageClassify model by loading image from filename"""
        with open(source, "rb") as imgfile:
            data = imgfile.read()
        pointer = ffi.from_buffer(data)
        res = self.__classify__(session=session, data=pointer)

        return res


class ImageDetect:

    out_size = 500

    def __init__(self):
        """Create an ImageDetect model resource"""
        print("test init")

    def __del__(self):
        """Destroy a vAccel ImageDetect model"""
        print("test del")

    @classmethod
    def __detect__(self, session:Session, data: List[int]) -> str :
        """Execute image detection operation"""
        csession = session._to_inner()

        img = ffi.cast("const void *",data)

        out_imagename = ffi.NULL
        len_img = len(data)

        len_out_imagename = 0

        ret = lib.vaccel_image_detection(csession, img, out_imagename, len_img, len_out_imagename)
        if ret != 0:
            raise VaccelError(ret, "Could not execute image detection operation")

        return ret

    @classmethod
    def detect_from_filename(self, session:Session, source: str) -> str :
        """Initialize an ImageDetect model by loading image from filename"""
        with open(source, "rb") as imgfile:
            data = imgfile.read()
        pointer = ffi.from_buffer(data)
        res = self.__detect__(session=session, data=pointer)

        return res


class ImageSegment:

    out_size = 500

    def __init__(self):
        """Create an ImageSegment model resource"""
        print("test init")

    def __del__(self):
        """Destroy a vAccel ImageSegment model"""
        print("test del")

    @classmethod
    def __segment__(self, session:Session, data: List[int]) -> str :
        """Execute image segmentation operation"""
        csession = session._to_inner()

        img = ffi.cast("const void *",data)

        out_imagename = ffi.NULL
        len_img = len(data)

        len_out_imagename = 0

        ret = lib.vaccel_image_segmentation(csession, img, out_imagename, len_img, len_out_imagename)
        if ret != 0:
            raise VaccelError(ret, "Could not execute image segmentation operation")

        return ret

    @classmethod
    def segment_from_filename(self, session:Session, source: str) -> str :
        """Initialize an ImageSegment model by loading image from filename"""
        with open(source, "rb") as imgfile:
            data = imgfile.read()
        pointer = ffi.from_buffer(data)
        res = self.__segment__(session=session, data=pointer)

        return res


class ImagePose:

    out_size = 500

    def __init__(self):
        """Create an ImagePose model resource"""
        print("test init")

    def __del__(self):
        """Destroy a vAccel ImagePose model"""
        print("test del")

    @classmethod
    def __pose__(self, session:Session, data: List[int]) -> str :
        """Execute image pose operation"""
        csession = session._to_inner()

        img = ffi.cast("const void *",data)

        out_imagename = ffi.NULL
        len_img = len(data)

        len_out_imagename = 0

        ret = lib.vaccel_image_pose(csession, img, out_imagename, len_img, len_out_imagename)
        if ret != 0:
            raise VaccelError(ret, "Could not execute image pose operation")

        return ret

    @classmethod
    def pose_from_filename(self, session:Session, source: str) -> str :
        """Initialize an ImagePose model by loading image from filename"""
        with open(source, "rb") as imgfile:
            data = imgfile.read()
        pointer = ffi.from_buffer(data)
        res = self.__pose__(session=session, data=pointer)

        return res


class ImageDepth:

    out_size = 500

    def __init__(self):
        """Create an ImageDepth model resource"""
        print("test init")

    def __del__(self):
        """Destroy a vAccel ImageDepth model"""
        print("test del")

    @classmethod
    def __depth__(self, session:Session, data: List[int]) -> str :
        """Execute image depth operation"""
        csession = session._to_inner()

        img = ffi.cast("const void *",data)

        out_imagename = ffi.NULL
        len_img = len(data)

        len_out_imagename = 0

        ret = lib.vaccel_image_depth(csession, img, out_imagename, len_img, len_out_imagename)        
        if ret != 0:
            raise VaccelError(ret, "Could not execute image depth operation")

        return ret

    @classmethod
    def depth_from_filename(self, session:Session, source: str) -> str :
        """Initialize an ImageDepth model by loading image from filename"""
        with open(source, "rb") as imgfile:
            data = imgfile.read()
        pointer = ffi.from_buffer(data)
        res = self.__depth__(session=session, data=pointer)

        return res
