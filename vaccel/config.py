# SPDX-License-Identifier: Apache-2.0

"""Interface to the `struct vaccel_config` C object."""

import logging

from ._c_types import CStr, CType
from ._libvaccel import ffi, lib
from .error import FFIError, NullPointerError

logger = logging.getLogger(__name__)


class Config(CType):
    """Wrapper for the `struct vaccel_config` C object.

    Manages the creation and initialization of a C `struct vaccel_config` and
    provides access to it through Python properties.

    Inherits:
        CType: Abstract base class for defining C data types.

    Attributes:
        _plugins (str): Colon-separated list of plugin names to load.
        _log_level (int): Logging verbosity level (1-4).
        _log_file (str | None): Path to the log file, or None to disable file
            logging.
        _profiling_enabled (bool): Whether profiling is enabled.
        _version_ignore (bool): Whether to ignore version mismatches.
    """

    def __init__(
        self,
        plugins: str = "libvaccel-noop.so",
        log_level: int = 1,
        log_file: str | None = None,
        *,
        profiling_enabled: bool = False,
        version_ignore: bool = False,
    ):
        """Initializes a new `Config` object.

        Args:
            plugins (str): Colon-separated list of plugin names to load.
            log_level (int): Logging level (1=ERROR, 4=DEBUG).
            log_file (str | None): Path to log file or None to disable logging
                to file.
            profiling_enabled (bool): Enable or disable profiling.
            version_ignore (bool): Ignore version mismatches if True.
        """
        self._plugins = str(plugins)
        self._log_level = log_level
        self._log_file = log_file
        self._profiling_enabled = profiling_enabled
        self._version_ignore = version_ignore
        self._c_obj_ptr = ffi.NULL
        super().__init__()

    def _init_c_obj(self):
        """Initializes the underlying C `struct vaccel_config` object.

        Raises:
            FFIError: If config initialization fails.
        """
        log_file = (
            self._log_file.encode() if self._log_file is not None else ffi.NULL
        )
        self._c_obj_ptr = ffi.new("struct vaccel_config **")
        ret = lib.vaccel_config_new(
            self._c_obj_ptr,
            self._plugins.encode(),
            self._log_level,
            log_file,
            self._profiling_enabled,
            self._version_ignore,
        )
        if ret != 0:
            raise FFIError(ret, "Could not initialize config")

        self._c_obj = self._c_obj_ptr[0]
        self._c_size = ffi.sizeof("struct vaccel_config")

    @property
    def value(self) -> ffi.CData:
        """Returns the value of the underlying C struct.

        Returns:
            The dereferenced 'struct vaccel_config`
        """
        return self._c_ptr_or_raise[0]

    def _del_c_obj(self):
        """Deletes the underlying `struct vaccel_config` C object.

        Raises:
            FFIError: If resource deletion fails.
        """
        ret = lib.vaccel_config_delete(self._c_ptr_or_raise)
        if ret != 0:
            raise FFIError(ret, "Could not delete resource")
        self._c_obj = ffi.NULL

    def __del__(self):
        try:
            self._del_c_obj()
        except NullPointerError:
            pass
        except FFIError:
            logger.exception("Failed to clean up Config")

    @property
    def plugins(self) -> str:
        """The configured plugins.

        Returns:
            The config's plugins.
        """
        return CStr.from_c_obj(self._c_ptr_or_raise.plugins).value

    @property
    def log_level(self) -> int:
        """The configured log level.

        Returns:
            The config's log level.
        """
        return int(self._c_ptr_or_raise.log_level)

    @property
    def log_file(self) -> str | None:
        """The configured log file.

        Returns:
            The config's log file.
        """
        log_file = self._c_ptr_or_raise.log_file
        if log_file == ffi.NULL:
            return None
        return CStr.from_c_obj(log_file).value

    @property
    def profiling_enabled(self) -> bool:
        """If profiling is enabled or disabled.

        Returns:
            True if profiling is enabled.
        """
        return bool(self._c_ptr_or_raise.profiling_enabled)

    @property
    def version_ignore(self) -> bool:
        """Whether a plugin/vAccel version mismatch is ignored.

        Returns:
            True if version mismatch is ignored.
        """
        return bool(self._c_ptr_or_raise.version_ignore)

    def __repr__(self):
        try:
            c_ptr = (
                f"0x{int(ffi.cast('uintptr_t', self._c_obj)):x}"
                if self._c_obj != ffi.NULL
                else "NULL"
            )
            plugins = self.plugins
            log_level = self.log_level
            log_file = self.log_file or "None"
            profiling = self.profiling_enabled
            version_ignore = self.version_ignore
        except (AttributeError, TypeError, NullPointerError):
            return f"<{self.__class__.__name__} (uninitialized or invalid)>"
        return (
            f"<{self.__class__.__name__} plugins={plugins!r} "
            f"log_level={log_level} "
            f"log_file={log_file!r} "
            f"profiling_enabled={profiling} "
            f"version_ignore={version_ignore} "
            f"at {c_ptr}>"
        )
