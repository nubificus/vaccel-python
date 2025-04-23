"""Build script for CFFI module library."""

import os
import re
import subprocess
from typing import Any

import cffi
import pkgconfig

PKG = "vaccel"
PKG_MIN_VERSION = "0.6.1"
MODULE_NAME = f"{PKG}._lib{PKG}"
HEADER_INCLUDE = f'#include "{PKG}.h"'


def generate_cdef(pkg: str, pkg_min_version: str) -> (str, dict[str, Any]):
    """Preprocess package header and generate cdef."""
    if not pkgconfig.exists(pkg) or pkgconfig.installed(
        pkg, f"< {pkg_min_version}"
    ):
        msg = (
            f"Required pkg-config package "
            f"'{pkg}' >= {pkg_min_version} not found"
        )
        raise ModuleNotFoundError(msg)

    cflags = pkgconfig.cflags(pkg).split()
    kwargs = pkgconfig.parse(pkg)

    cc = os.environ.get("CC", "cc")

    proc = subprocess.run(
        [cc, *cflags, "-E", "-"],
        input=HEADER_INCLUDE,
        capture_output=True,
        text=True,
        check=True,
    )

    return (proc.stdout, kwargs)


def remove_extern(line: str) -> bool:
    """Check if line contains 'extern' declaration that should be skipped."""
    extern_re = re.compile(r"\bextern\b")
    return bool(extern_re.search(line))


def handle_atomic_declaration(line: str) -> str | None:
    """Handle atomic declarations by replacing them with '...;'."""
    atomic_re = re.compile(r"\b(_Atomic|atomic_[a-zA-Z0-9_]+)\b")
    if atomic_re.search(line):
        indent = re.match(r"^(\s*)", line).group(1)
        return f"{indent}...;"
    return None


def handle_deprecated_function(line: str, *, in_function: bool) -> (bool, bool):
    """Handle removal of deprecated function declarations."""
    deprecated_re = re.compile(r"__attribute__\(\(deprecated\b")

    if in_function:
        if line.strip().endswith("}"):
            in_function = False
        return (in_function, True)
    if deprecated_re.search(line):
        return (True, True)

    return (in_function, False)


def handle_inline_function(
    line: str, brace_depth: int, *, in_function: bool
) -> (bool, int, str):
    """Handle removal of inline function declarations."""
    inline_re = re.compile(r"\bstatic\s+inline\b")

    if in_function:
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            in_function = False
            brace_depth = 0
        return in_function, brace_depth, None

    match = inline_re.search(line)
    if match:
        prefix = line[: match.start()].rstrip()
        if prefix:
            # Still check for atomics in that prefix
            atomic_result = handle_atomic_declaration(prefix)
            result_line = atomic_result if atomic_result else prefix
        brace_depth = line.count("{") - line.count("}")
        if brace_depth > 0:
            in_function = True
        return in_function, brace_depth, result_line

    return in_function, brace_depth, line


def sanitize_cdef(cdef: str, pkg: str) -> str:
    """Sanitize cdef by removing unsupported declarations."""
    output_lines = cdef.splitlines()
    filtered_lines = []

    line_re = re.compile(r'# \d+ "(.*?)"')

    current_file = None
    pkg_lines = True
    in_deprecated_function = False
    in_inline_function = False
    brace_depth = 0

    for line in output_lines:
        if line.startswith("#"):
            match = line_re.match(line)
            if match:
                current_file = match.group(1)
                pkg_lines = pkg in current_file
            continue

        # Remove non-package declarations
        if not pkg_lines:
            continue

        # Remove 'extern' functions
        if remove_extern(line):
            continue

        # Handle atomic declarations
        atomic_result = handle_atomic_declaration(line)
        if atomic_result:
            filtered_lines.append(atomic_result)
            continue

        # Handle deprecated functions
        (in_deprecated_function, skip) = handle_deprecated_function(
            line, in_function=in_deprecated_function
        )
        if skip:
            continue

        # Handle inline functions
        (in_inline_function, brace_depth, result_line) = handle_inline_function(
            line, brace_depth, in_function=in_inline_function
        )
        if result_line is not None:
            filtered_lines.append(result_line)
            continue

        filtered_lines.append(line)

    return "\n".join(filtered_lines)


def compile_ffi() -> cffi.FFI:
    """Generate and compile ffi bindings."""
    (cdef, kwargs) = generate_cdef(PKG, PKG_MIN_VERSION)
    sanitized_cdef = sanitize_cdef(cdef, PKG)

    ffibuilder = cffi.FFI()
    ffibuilder.set_source(MODULE_NAME, HEADER_INCLUDE, **kwargs, py_limited_api=True)
    ffibuilder.cdef(sanitized_cdef)
    ffibuilder.compile(verbose=True)
    return ffibuilder


if __name__ == "__main__":
    compile_ffi()
