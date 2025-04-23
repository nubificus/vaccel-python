"""Utilities for C type conversions."""

from enum import IntEnum
from typing import Any


class CEnumBuilder:
    """Python from C enum builder.

    Utility class for creating Python IntEnum types from C enum constants
    exposed through a CFFI-loaded shared library.

    Attributes:
        lib (Any): The CFFI-loaded shared library with the C enum constants.
        _cache (dict): A cache for the generated `IntEnum` types.
    """

    def __init__(self, lib: Any):
        """Initializes a new `CEnumBuilder` object.

        Args:
            lib: A CFFI-loaded shared library.
        """
        self.lib = lib
        self._cache = {}

    def from_prefix(self, enum_name: str, prefix: str) -> IntEnum:
        """Generates a Python enum from a C enum prefix.

        Dynamically create a Python `IntEnum` from C enum constants that share a
        prefix.

        Args:
            enum_name: The name to give the `IntEnum`.
            prefix: The prefix of the C constants (e.g., "VACCEL_").

        Returns:
            A Python IntEnum with values mapped from the C library.
        """
        if enum_name in self._cache:
            return self._cache[enum_name]

        members = {
            attr[len(prefix) :]: getattr(self.lib, attr)
            for attr in dir(self.lib)
            if attr.startswith(prefix)
        }

        # Build docstring
        docstring = self._build_enum_docstring(enum_name, members)

        # Generate enum
        enum_cls = IntEnum(enum_name, members)
        enum_cls.__doc__ = docstring

        self._cache[enum_name] = enum_cls
        return enum_cls

    def _build_enum_docstring(
        self, enum_name: str, members: dict[str, int]
    ) -> str:
        """Builds a Google-style docstring for an enum.

        Args:
            enum_name: The name of the `IntEnum`
            members: The members with the values of the `IntEnum`

        Returns:
            A docstring for the generated `IntEnum`
        """
        lines = [f"{enum_name} enumeration.", "", "Attributes:"]
        for name, value in members.items():
            lines.append(f"    {name} (int): {value}.")
        return "\n".join(lines)
