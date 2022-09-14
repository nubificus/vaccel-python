from typing import List
from vaccel.session import Session
from vaccel.genop import Genop, VaccelArg, VaccelOpType


class __ImageOperation__:

    def_arg_write: bytes = bytes(100 * " ", encoding="utf-8")

    @staticmethod
    def __genop__(arg_read: List[VaccelArg], arg_write: List[VaccelArg], index: int) -> str:
        """
        Performs the genop operation provided in arg_read.

        Returns the content of the arg_write indicated by index.
        """
        ses = Session(flags=0)
        Genop.genop(ses, arg_read, arg_write)
        return arg_write[index].content

    @staticmethod
    def __parse_image__(image: str | bytes) -> bytes:
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
    def classify(self, image: str | bytes):
        """
        Classify image using vAccel over genop

        Parameters:
            image (str | bytes): Filename or bytes object of the image 

        Returns:
            str: Classification tag
        """
        image = self.__parse_image__(image=image)
        arg_read = [VaccelArg(data=int(self.__op__)),
                    VaccelArg(data=image)]
        arg_write = [VaccelArg(data=self.def_arg_write)]*2
        return self.__genop__(arg_read=arg_read, arg_write=arg_write, index=0)


class ImageDetect(__ImageOperation__):

    __op__ = VaccelOpType.VACCEL_IMG_DETEC

    @classmethod
    def detect(self, image: str | bytes):
        """
        Perform image detection operation using vAccel over genop

        Parameters:
            image (str | bytes): Filename or bytes object of the image 

        Returns:
            str: Detection result
        """
        image = self.__parse_image__(image=image)
        arg_read = [VaccelArg(data=int(self.__op__)),
                    VaccelArg(data=image)]
        arg_write = [VaccelArg(data=self.def_arg_write)]
        return self.__genop__(arg_read=arg_read, arg_write=arg_write, index=0)
