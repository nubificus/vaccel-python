from vaccel._vaccel import lib, ffi
from vaccel.error import VaccelError
from vaccel.session import Session
from typing import List


class ImageClassify:
    """An Image Classify model vAccel resource."""

    out_size = 500

    def __init__(self):
        print("test init")

    def __del__(self):
        print("test del")

    @classmethod
    def __classify__(self, session: Session, data: List[int]) -> str:
        """Execute image classification operation.
        
        Parameters
        ----------
        session : `Any`
        data : `list`

        Returns
        ----------
        `str` : Classification tag
        """
        csession = session._to_inner()

        img = ffi.cast("const void *", data)

        out_text = ffi.new(f"unsigned char[{self.out_size}]")

        out_imgname = ffi.NULL
        len_img = len(data)

        len_out_text = self.out_size
        len_out_imgname = 0

        ret = lib.vaccel_image_classification(
            csession, img, out_text, out_imgname, len_img, len_out_text, len_out_imgname)
        if ret != 0:
            raise VaccelError(
                ret, "Could not execute image classification operation")

        out_res = "".join([chr(i) for i in out_text]).rstrip('\x00')

        return out_res

    @classmethod
    def classify_from_filename(self, session: Session, source: str) -> str:
        """Initialize an ImageClassify model by loading image from filename
        
        Parameters
        ----------
        session : `Any`
        source : `str`

        Returns
        ----------
        `str` : Classification tag
        """
        with open(source, "rb") as imgfile:
            data = imgfile.read()
        pointer = ffi.from_buffer(data)
        res = self.__classify__(session=session, data=pointer)
        return res


class ImageDetect:
    """An Image Detect model vAccel resource"""

    out_size = 500

    def __init__(self):
        print("test init")

    def __del__(self):
        print("test del")

    @classmethod
    def __detect__(self, session: Session, data: List[int]) -> str:
        """Execute image detection operation
        
        Parameters
        ----------
        session : `Any`
        data : `list`

        Returns
        ----------
        `str` : Detection result
        """
        csession = session._to_inner()

        img = ffi.cast("const void *", data)

        out_imagename = ffi.NULL
        len_img = len(data)

        len_out_imagename = 0

        ret = lib.vaccel_image_detection(
            csession, img, out_imagename, len_img, len_out_imagename)
        if ret != 0:
            raise VaccelError(
                ret, "Could not execute image detection operation")

        return ret

    @classmethod
    def detect_from_filename(self, session: Session, source: str) -> str:
        """Initialize an ImageDetect model by loading image from filename
        
        Parameters
        ----------
        session : `Any`
        source : `str`

        Returns
        ----------
        `str` : Detection tag
        """
        with open(source, "rb") as imgfile:
            data = imgfile.read()
        pointer = ffi.from_buffer(data)
        res = self.__detect__(session=session, data=pointer)

        return res


class ImageSegment:
    """An Image Segment model vAccel resource"""

    out_size = 500

    def __init__(self):
        print("test init")

    def __del__(self):
        print("test del")

    @classmethod
    def __segment__(self, session: Session, data: List[int]) -> str:
        """Execute image segmentation operation
        
        Parameters
        ----------
        session : `Any`
        data : `list`

        Returns
        ----------
        `str` : Segmentation result
        """
        csession = session._to_inner()

        img = ffi.cast("const void *", data)

        out_imagename = ffi.NULL
        len_img = len(data)

        len_out_imagename = 0

        ret = lib.vaccel_image_segmentation(
            csession, img, out_imagename, len_img, len_out_imagename)
        if ret != 0:
            raise VaccelError(
                ret, "Could not execute image segmentation operation")

        return ret

    @classmethod
    def segment_from_filename(self, session: Session, source: str) -> str:
        """Initialize an ImageSegment model by loading image from filename
        Parameters
        ----------
        session : `Any`
        source : `str`

        Returns
        ----------
        `str` : Segmentation tag
        """
        with open(source, "rb") as imgfile:
            data = imgfile.read()
        pointer = ffi.from_buffer(data)
        res = self.__segment__(session=session, data=pointer)

        return res


class ImagePose:
    """An ImageC Pose model vAccel resource"""

    out_size = 500

    def __init__(self):
        print("test init")

    def __del__(self):
        print("test del")

    @classmethod
    def __pose__(self, session: Session, data: List[int]) -> str:
        """Execute image pose operation
        
        Parameters
        ----------
        session : `Any`
        data : `list`

        Returns
        ----------
        `str` : Pose result
        """
        csession = session._to_inner()

        img = ffi.cast("const void *", data)

        out_imagename = ffi.NULL
        len_img = len(data)

        len_out_imagename = 0

        ret = lib.vaccel_image_pose(
            csession, img, out_imagename, len_img, len_out_imagename)
        if ret != 0:
            raise VaccelError(ret, "Could not execute image pose operation")

        return ret

    @classmethod
    def pose_from_filename(self, session: Session, source: str) -> str:
        """Initialize an ImagePose model by loading image from filename
        
        Parameters
        ----------
        session : `Any`
        source : `str`

        Returns
        ----------
        `str` : Pose result
        """
        with open(source, "rb") as imgfile:
            data = imgfile.read()
        pointer = ffi.from_buffer(data)
        res = self.__pose__(session=session, data=pointer)

        return res


class ImageDepth:
    """An Image Depth model vAccel resource"""

    out_size = 500

    def __init__(self):
        print("test init")

    def __del__(self):
        print("test del")

    @classmethod
    def __depth__(self, session: Session, data: List[int]) -> str:
        """Execute image depth operation
        
        Parameters
        ----------
        session : `Any`
        data : `list`

        Returns
        ----------
        `str` : Depth reult
        """
        csession = session._to_inner()

        img = ffi.cast("const void *", data)

        out_imagename = ffi.NULL
        len_img = len(data)

        len_out_imagename = 0

        ret = lib.vaccel_image_depth(
            csession, img, out_imagename, len_img, len_out_imagename)
        if ret != 0:
            raise VaccelError(ret, "Could not execute image depth operation")

        return ret

    @classmethod
    def depth_from_filename(self, session: Session, source: str) -> str:
        """Initialize an ImageDepth model by loading image from filename
        
        Parameters
        ----------
        session : `Any`
        source : `str`

        Returns
        ----------
        `str` : Depth reult
        """
        with open(source, "rb") as imgfile:
            data = imgfile.read()
        pointer = ffi.from_buffer(data)
        res = self.__depth__(session=session, data=pointer)

        return res
