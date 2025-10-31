# SPDX-License-Identifier: Apache-2.0

"""Utilities for C type conversions."""

from enum import IntEnum, IntFlag
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

    def from_prefix(
        self,
        enum_name: str,
        prefix: str,
        enum_type: type[IntEnum] | type[IntFlag] = IntEnum,
    ) -> IntEnum | IntFlag:
        """Generates a Python enum from a C enum prefix.

        Dynamically create a Python `IntEnum` from C enum constants that share a
        prefix.

        Args:
            enum_name: The name to give the generated Enum.
            prefix: The prefix of the C constants (e.g., "VACCEL_").
            enum_type: The Enum base class to use.

        Returns:
            A Python IntEnum with values mapped from the C library.
        """
        cache_key = (enum_name, enum_type)
        if cache_key in self._cache:
            return self._cache[cache_key]

        members = {
            attr[len(prefix) :]: getattr(self.lib, attr)
            for attr in dir(self.lib)
            if attr.startswith(prefix)
        }

        if not members:
            msg = f"No constants found with prefix '{prefix}'"
            raise ValueError(msg)

        # Build docstring
        docstring = self._build_enum_docstring(enum_name, members)

        enum_cls = enum_type(enum_name, members)
        enum_cls.__doc__ = docstring

        self._cache[cache_key] = enum_cls
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
