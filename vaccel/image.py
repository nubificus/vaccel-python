"""Image-related operations."""

from ._c_types import CBytes
from ._libvaccel import lib
from .error import FFIError


class ImageMixin:
    """Mixin providing image operations for a `Session`.

    This mixin is intended to be used in combination with `BaseSession` and
    should not be instantiated on its own.

    Intended usage:
        class Session(BaseSession, ImageMixin):
            ...

    Attributes:
        _out_len (int): The maximum length of the output buffers
    """

    _out_len = 512

    def classify(self, image: bytes) -> (str, str):
        """Performs the image classification operation.

        Wraps the `vaccel_image_classification()` C operation.

        Args:
            image: The image data as a `bytes` object.

        Returns:
            A tuple containing:
                - The classification tag.
                - The resulting image filename.

        Raises:
            RuntimeError: If the `Session` is uninitialized.
            FFIError: If the C operation fails.
        """
        if not self._c_ptr:
            msg = "Uninitialized session"
            raise RuntimeError(msg)

        img = CBytes(image)
        out_text = CBytes(bytearray(self._out_len))
        out_imgname = CBytes(bytearray(self._out_len))

        ret = lib.vaccel_image_classification(
            self._c_ptr,
            img._c_ptr,
            out_text._c_ptr,
            out_imgname._c_ptr,
            len(img),
            len(out_text),
            len(out_imgname),
        )
        if ret:
            raise FFIError(ret, "Image classification failed")

        return out_text.to_str(), out_imgname.to_str()

    def detect(self, image: bytes) -> str:
        """Performs the image detection operation.

        Wraps the `vaccel_image_detection()` C operation.

        Args:
            image: The image data as a `bytes` object.

        Returns:
            The resulting image filename.

        Raises:
            RuntimeError: If the `Session` is uninitialized.
            FFIError: If the C operation fails.
        """
        if not self._c_ptr:
            msg = "Uninitialized session"
            raise RuntimeError(msg)

        img = CBytes(image)
        out_imgname = CBytes(bytearray(self._out_len))

        ret = lib.vaccel_image_detection(
            self._c_ptr,
            img._c_ptr,
            out_imgname._c_ptr,
            len(img),
            len(out_imgname),
        )
        if ret:
            raise FFIError(ret, "Image detection failed")

        return out_imgname.to_str()

    def segment(self, image: bytes) -> str:
        """Performs the image segmentation operations.

        Wraps the `vaccel_image_segmentation()` C operation.

        Args:
            image: The image data as a `bytes` object.

        Returns:
            The resulting image filename.

        Raises:
            RuntimeError: If the `Session` is uninitialized.
            FFIError: If the C operation fails.
        """
        if not self._c_ptr:
            msg = "Uninitialized session"
            raise RuntimeError(msg)

        img = CBytes(image)
        out_imgname = CBytes(bytearray(self._out_len))

        ret = lib.vaccel_image_segmentation(
            self._c_ptr,
            img._c_ptr,
            out_imgname._c_ptr,
            len(img),
            len(out_imgname),
        )
        if ret:
            raise FFIError(ret, "Image segmentation failed")

        return out_imgname.to_str()

    def pose(self, image: bytes) -> str:
        """Performs the image pose estimation operation.

        Wraps the `vaccel_image_pose()` C operation.

        Args:
            image: The image data as a `bytes` object.

        Returns:
            The resulting image filename.

        Raises:
            RuntimeError: If the `Session` is uninitialized.
            FFIError: If the C operation fails.
        """
        if not self._c_ptr:
            msg = "Uninitialized session"
            raise RuntimeError(msg)

        img = CBytes(image)
        out_imgname = CBytes(bytearray(self._out_len))

        ret = lib.vaccel_image_pose(
            self._c_ptr,
            img._c_ptr,
            out_imgname._c_ptr,
            len(img),
            len(out_imgname),
        )
        if ret:
            raise FFIError(ret, "Image pose estimation failed")

        return out_imgname.to_str()

    def depth(self, image: bytes) -> str:
        """Performs the image depth estimation operation.

        Wraps the `vaccel_image_depth()` C operation.

        Args:
            image: The image data as a `bytes` object.

        Returns:
            The resulting image filename.

        Raises:
            RuntimeError: If the `Session` is uninitialized.
            FFIError: If the C operation fails.
        """
        if not self._c_ptr:
            msg = "Uninitialized session"
            raise RuntimeError(msg)

        img = CBytes(image)
        out_imgname = CBytes(bytearray(self._out_len))

        ret = lib.vaccel_image_depth(
            self._c_ptr,
            img._c_ptr,
            out_imgname._c_ptr,
            len(img),
            len(out_imgname),
        )
        if ret:
            raise FFIError(ret, "Image depth estimation failed")

        return out_imgname.to_str()
