from vaccel._vaccel import lib, ffi
from vaccel.error import VaccelError
from vaccel.session import Session
from typing import List


class ImageClassify:
    """An Image Classify model vAccel resource.
    
    Attributes:
        out_size (int): The maximum length of the output tag
    """

    out_size = 500

    def __init__(self):
        print("test init")

    def __del__(self):
        print("test del")

    @classmethod
    def __classify__(cls, session: Session, data: List[int]) -> str:
        """Executes image classification operation.

        Args:
            session: A vaccel.Session instance
            data: A sequence of integers representing the image
        
        Returns:
            A string containing the classifiaction tag
        
        Raises:
            VaccelError: An error occured while executing the image classification operation
        """
        csession = session._to_inner()

        img = ffi.cast("const void *", data)

        out_text = ffi.new(f"unsigned char[{cls.out_size}]")

        out_imgname = ffi.NULL
        len_img = len(data)

        len_out_text = cls.out_size
        len_out_imgname = 0

        ret = lib.vaccel_image_classification(
            csession, img, out_text, out_imgname, len_img, len_out_text, len_out_imgname)
        if ret != 0:
            raise VaccelError(
                ret, "Could not execute image classification operation")

        out_res = "".join([chr(i) for i in out_text]).rstrip('\x00')

        return out_res

    @classmethod
    def classify_from_filename(cls, session: Session, source: str) -> str:
        """Initialize an ImageClassify model by loading image from filename

        Args:
            session: A vaccel.Session instance
            source: A string containing the image's file path
        
        Returns:
            A string containing the classifiaction tag
        
        Raises:
            VaccelError: An error occured while executing the image classification operation
        """
        with open(source, "rb") as imgfile:
            data = imgfile.read()
        pointer = ffi.from_buffer(data)
        res = cls.__classify__(session=session, data=pointer)
        return res


class ImageDetect:
    """An Image Detect model vAccel resource

     Attributes:
        out_size (int): The maximum length of the output tag
    """

    out_size = 500

    def __init__(self):
        print("test init")

    def __del__(self):
        print("test del")

    @staticmethod
    def __detect__(session: Session, data: List[int]) -> str:
        """Execute image detection operation
        
         Args:
            session: A vaccel.Session instance
            source: A string containing the image's file path
        
        Returns:
            A string containing the detection result
        
        Raises:
            VaccelError: An error occured while executing the image detection operation
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
    def detect_from_filename(cls, session: Session, source: str) -> str:
        """Initialize an ImageDetect model by loading image from filename
                
        Args:
            session: A vaccel.Session instance
            source: A string containing the image's file path

        Returns:
            A string containing the detection result

        Raises:
            VaccelError: An error occured while executing the image detection operation
        """
        with open(source, "rb") as imgfile:
            data = imgfile.read()
        pointer = ffi.from_buffer(data)
        res = cls.__detect__(session=session, data=pointer)

        return res


class ImageSegment:
    """An Image Segment model vAccel resource
    
    Attributes:
        out_size (int): The maximum length of the output tag
    """
    
    out_size = 500

    def __init__(self):
        print("test init")

    def __del__(self):
        print("test del")

    @staticmethod
    def __segment__(session: Session, data: List[int]) -> str:
        """Execute image segmentation operation
        
         Args:
            session: A vaccel.Session instance
            source: A string containing the image's file path
        
        Returns:
            A string containing the segmentation result
        
        Raises:
            VaccelError: An error occured while executing the image segmentation operation
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
    def segment_from_filename(cls, session: Session, source: str) -> str:
        """Initialize an ImageSegment model by loading image from filename
                 
        Args:
            session: A vaccel.Session instance
            source: A string containing the image's file path

        Returns:
            A string containing the segmentation result

        Raises:
            VaccelError: An error occured while executing the image segmentation operation
        """
        with open(source, "rb") as imgfile:
            data = imgfile.read()
        pointer = ffi.from_buffer(data)
        res = cls.__segment__(session=session, data=pointer)

        return res


class ImagePose:
    """An Image Pose model vAccel resource
    
    Attributes:
        out_size (int): The maximum length of the output tag
    """

    out_size = 500

    def __init__(self):
        print("test init")

    def __del__(self):
        print("test del")

    @staticmethod
    def __pose__(session: Session, data: List[int]) -> str:
        """Execute image pose operation
        
        Args:
            session: A vaccel.Session instance
            source: A string containing the image's file path

        Returns:
            A string containing the pose result

        Raises:
            VaccelError: An error occured while executing the image pose operation
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
    def pose_from_filename(cls, session: Session, source: str) -> str:
        """Initialize an ImagePose model by loading image from filename
                 
        Args:
            session: A vaccel.Session instance
            source: A string containing the image's file path

         Returns:
            A string containing the pose result

        Raises:
            VaccelError: An error occured while executing the image pose operation
        """
        with open(source, "rb") as imgfile:
            data = imgfile.read()
        pointer = ffi.from_buffer(data)
        res = cls.__pose__(session=session, data=pointer)

        return res


class ImageDepth:
    """An Image Depth model vAccel resource
    
    Attributes:
        out_size (int): The maximum length of the output tag
    """

    out_size = 500

    def __init__(self):
        print("test init")

    def __del__(self):
        print("test del")

    @staticmethod
    def __depth__(session: Session, data: List[int]) -> str:
        """Execute image depth operation
        
         Args:
            session: A vaccel.Session instance
            source: A string containing the image's file path

        Returns:
            A string containing the depth result

        Raises:
            VaccelError: An error occured while executing the image depth operation
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
    def depth_from_filename(cls, session: Session, source: str) -> str:
        """Initialize an ImageDepth model by loading image from filename
        
        Args:
            session: A vaccel.Session instance
            source: A string containing the image's file path

         Returns:
            A string containing the depth result

        Raises:
            VaccelError: An error occured while executing the image depth operation
        """
        with open(source, "rb") as imgfile:
            data = imgfile.read()
        pointer = ffi.from_buffer(data)
        res = cls.__depth__(session=session, data=pointer)

        return res