"""Interface to the `struct vaccel_session` C object."""

from ._c_types import CType
from ._libvaccel import ffi, lib
from .error import FFIError
from .ops.blas import BlasMixin
from .ops.exec import ExecMixin
from .ops.fpga import FpgaMixin
from .ops.genop import GenopMixin
from .ops.image import ImageMixin
from .ops.minmax import MinmaxMixin
from .ops.noop import NoopMixin
from .ops.tf import TFMixin
from .ops.tflite import TFLiteMixin
from .ops.torch import TorchMixin
from .resource import Resource


class BaseSession(CType):
    """Wrapper for the `struct vaccel_session` C object.

    Manages the creation and initialization of a C `struct vaccel_session` and
    provides access to it through Python properties.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _flags (int): The flags used to create the session.
    """

    def __init__(self, flags: int = 0):
        """Initializes a new `BaseSession` object.

        Args:
            flags: The flags to configure the session creation. Defaults to 0.
        """
        self._flags = flags
        super().__init__()

    def _init_c_obj(self):
        """Initializes the underlying `struct vaccel_session` C object.

        Raises:
            FFIError: If session initialization fails.
        """
        # TODO: Use vaccel_session_new()  # noqa: FIX002
        self._c_obj = ffi.new("struct vaccel_session *")
        ret = lib.vaccel_session_init(self._c_obj, self._flags)
        if ret != 0:
            raise FFIError(ret, "Could not init session")

        self._c_size = ffi.sizeof("struct vaccel_session")

    @property
    def value(self) -> ffi.CData:
        """Returns the value of the underlying C struct.

        Returns:
            The dereferenced 'struct vaccel_session`
        """
        return self._c_obj[0]

    def _del_c_obj(self):
        """Releases the underlying C `struct vaccel_session` object.

        Raises:
            FFIError: If session release fails.
        """
        if self._c_obj:
            ret = lib.vaccel_session_release(self._c_obj)
            if ret != 0:
                raise FFIError(ret, "Could not release session")
            self._c_obj = None

    def __del__(self):
        self._del_c_obj()

    @property
    def id(self) -> int:
        """The session identifier.

        Returns:
            The session's unique ID.
        """
        return int(self._c_obj.id)

    @property
    def remote_id(self) -> int:
        """The remote session identifier.

        Returns:
            The session's remote ID.
        """
        return int(self._c_obj.remote_id)

    @property
    def flags(self) -> int:
        """The session flags.

        Returns:
            The flags set during session creation.
        """
        return int(self._c_obj.flags)

    def has_resource(self, resource: Resource) -> bool:
        """Check if a resource is registered with the session.

        Args:
            resource: The resource to check for registration.

        Returns:
            True if the resource is registered.
        """
        return (
            lib.vaccel_session_has_resource(
                self._c_obj, resource._get_inner_resource()
            )
            != 0
        )


class Session(
    BaseSession,
    NoopMixin,
    GenopMixin,
    ExecMixin,
    ImageMixin,
    BlasMixin,
    FpgaMixin,
    MinmaxMixin,
    TFMixin,
    TFLiteMixin,
    TorchMixin,
):
    """Extended session with operations' functionalities.

    Inherits from `BaseSession` and the operation mixins, adding support for the
    operation functions.

    Inherits:
        BaseSession: Core session management.
        NoopMixin: Debug operation.
        GenopMixin: Generic operation.
        ExecMixin: Exec operations.
        ImageMixin: Image-related operations.
        BlasMixin: BLAS operations.
        FpgaMixin: FPGA operations.
        MinmaxMixin: Minmax operations.
        TensorflowMixin: TensorFlow operations.
    """
