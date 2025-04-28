# SPDX-License-Identifier: Apache-2.0

"""Interface to the `struct vaccel_op` C object."""

from ._c_types.utils import CEnumBuilder
from ._libvaccel import lib

enum_builder = CEnumBuilder(lib)
OpType = enum_builder.from_prefix("OpType", "VACCEL_OP_")
