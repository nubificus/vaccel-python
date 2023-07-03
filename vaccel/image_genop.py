from typing import List
from vaccel.session import Session
from vaccel.genop import Genop, VaccelArg, VaccelOpType


class __ImageOperation__:
    """An Image Operation model vAccel resource
    
    Attributes:
        def_arg_write (bytes): The result of the operation
    """

    def_arg_write: bytes = bytes(100 * " ", encoding="utf-8")

    @staticmethod
    def __genop__(arg_read: List[VaccelArg], arg_write: List[VaccelArg], index: int) -> str:
        """Performs the genop operation provided in arg_read.
        
        Args:
            arg_read : A list of inputs
            arg_write : A list of outputs
            index : An integer

        Returns:
            The content of the `arg_write` indicated by `index`.
        """
        ses = Session(flags=0)
        Genop.genop(ses, arg_read, arg_write)
        return arg_write[index].content

    @staticmethod
    def __parse_image__(image: "str | bytes") -> bytes:
        """Reads image data from file.
        
        Args:
            image: A string or bytes object containing the image's file path

        Returns:
            Returns image file content.

        Raises:
            TypeError: If image object is not a string or bytes object
        """

        if not isinstance(image, str) and not isinstance(image, bytes):
            raise TypeError(
                f"Invalid image type. Expected str or bytes, got {type(image)}.")
 
        if isinstance(image, str):
            with open(image, "rb") as imgfile:
                image = imgfile.read()

        return image


class ImageClassify(__ImageOperation__):

    __op__ = VaccelOpType.VACCEL_IMG_CLASS

    @classmethod
    def classify(cls, image: "str | bytes"):
        """Executes image classification operation using vAccel over genop.

        Args:
            image : A string or bytes object containing the image's file path

        Returns:
            A string containing the classifiaction tag
        """
        image = cls.__parse_image__(image=image)
        arg_read = [VaccelArg(data=int(cls.__op__)),
                    VaccelArg(data=image)]
        arg_write = [VaccelArg(data=bytes(100 * " ", encoding="utf-8")),
                     VaccelArg(data=bytes(100 * " ", encoding="utf-8"))]
        return cls.__genop__(arg_read=arg_read, arg_write=arg_write, index=0)


class ImageDetect(__ImageOperation__):

    __op__ = VaccelOpType.VACCEL_IMG_DETEC

    @classmethod
    def detect(cls, image: "str | bytes"):
        """Executes image detection operation using vAccel over genop.

        Args:
            image : A string or bytes object containing the image's file path

        Returns:
            A string containing the detection result
        """
        image = cls.__parse_image__(image=image)
        arg_read = [VaccelArg(data=int(cls.__op__)),
                    VaccelArg(data=image)]
        arg_write = [VaccelArg(data=bytes(100 * " ", encoding="utf-8"))]
        return cls.__genop__(arg_read=arg_read, arg_write=arg_write, index=0)


class ImageSegment(__ImageOperation__):

    __op__ = VaccelOpType.VACCEL_IMG_SEGME

    @classmethod
    def segment(cls, image: "str | bytes"):
        """Executes image segmentation operation using vAccel over genop.

        Args:
            image : A string or bytes object containing the image's file path

        Returns:
            A string containing the segmentation result
        """
        image = cls.__parse_image__(image=image)
        arg_read = [VaccelArg(data=int(cls.__op__)),
                    VaccelArg(data=image)]
        arg_write = [VaccelArg(data=bytes(100 * " ", encoding="utf-8"))]
        return cls.__genop__(arg_read=arg_read, arg_write=arg_write, index=0)


class ImagePose(__ImageOperation__):

    __op__ = VaccelOpType.VACCEL_IMG_POSE

    @classmethod
    def pose(cls, image: "str | bytes"):
        """Executes image pose estimation operation using vAccel over genop.

        Args:
            image : A string or bytes object containing the image's file path

        Returns:
            A string containing the pose estimation result
        """
        image = cls.__parse_image__(image=image)
        arg_read = [VaccelArg(data=int(cls.__op__)),
                    VaccelArg(data=image)]
        arg_write = [VaccelArg(data=bytes(100 * " ", encoding="utf-8"))]
        return cls.__genop__(arg_read=arg_read, arg_write=arg_write, index=0)


class ImageDepth(__ImageOperation__):

    __op__ = VaccelOpType.VACCEL_IMG_DEPTH

    @classmethod
    def depth(cls, image: "str | bytes"):
        """Executes image depth estimation operation using vAccel over genop.

        Args:
            image : A string or bytes object containing the image's file path

        Returns:
            A string containing the depth estimation result
        """
        image = cls.__parse_image__(image=image)
        arg_read = [VaccelArg(data=int(cls.__op__)),
                    VaccelArg(data=image)]
        arg_write = [VaccelArg(data=bytes(100 * " ", encoding="utf-8"))]
        return cls.__genop__(arg_read=arg_read, arg_write=arg_write, index=0)
