# SPDX-License-Identifier: Apache-2.0

"""Interface to the `struct vaccel_plugin` C object."""

from enum import IntFlag

from ._c_types.utils import CEnumBuilder
from ._libvaccel import lib

enum_builder = CEnumBuilder(lib)
PluginType = enum_builder.from_prefix("PluginType", "VACCEL_PLUGIN_", IntFlag)
