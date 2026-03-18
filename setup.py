# SPDX-License-Identifier: Apache-2.0

"""A setuptools based setup module.

This module is only necessary for building the CFFI module library.
"""

from typing import Any

from packaging.version import Version
from setuptools import setup
from setuptools_scm.git import parse as git_parse
from setuptools_scm.version import ScmVersion


def custom_parse(root: str, config: Any) -> ScmVersion | None:
    """Custom parse function that removes tag local segment.

    Removes semver metadata from tags to generate pypi compatible versions.
    """
    version: ScmVersion | None = git_parse(root, config)
    if version is None:
        return None

    # Strip local segment from parsed tag so setuptools-scm does not
    # re-append it
    base = str(version.tag).split("+")[0]
    version.tag = Version(base)

    return version


setup(
    cffi_modules=["build_ffi.py:compile_ffi"],
    use_scm_version={
        "parse": custom_parse,
        "version_scheme": "no-guess-dev",
    },
)
