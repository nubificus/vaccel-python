"""Build script for CFFI module library."""

import os
import re
import subprocess
from typing import Any

import cffi
import pkgconfig

PKG = "vaccel"
PKG_MIN_VERSION = "0.7.0"
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


def remove_deprecated_functions(src: str) -> str:
    """Remove deprecated function declarations."""
    out, i, n = [], 0, len(src)
    pat = re.compile(r'__attribute__\s*\(\(deprecated\b')

    while i < n:
        m = pat.search(src, i)
        if not m:
            out.append(src[i:])
            break

        # Go backward to find the start of the function declaration
        start = src.rfind('\n', 0, m.start())
        start = start + 1 if start != -1 else 0
        out.append(src[i:start])

        # Move forward to skip the function body
        j = src.find('{', m.end())
        if j == -1:
            i = m.end()
            # Malformed, skip the attribute
            continue

        brace = 1
        j += 1
        while j < n and brace:
            if src[j] == '{':
                brace += 1
            elif src[j] == '}':
                brace -= 1
            j += 1

        # Skip trailing characters (semicolons, whitespace)
        while j < n and src[j] in " \t\n;":
            j += 1

        i = j

    return ''.join(out)


def remove_static_inline_functions(source: str) -> str:
    """Remove 'static inline' functions."""
    static_inline_re = re.compile(r'\bstatic\s+inline\b')
    result = []
    i = 0
    n = len(source)

    while i < n:
        match = static_inline_re.search(source, i)
        if not match:
            # No more static inlines, copy the rest
            result.append(source[i:])
            break

        start = match.start()

        # Copy anything before the match
        if start > i:
            result.append(source[i:start])

        # Find the function body using brace matching
        brace_count = 0
        body_start = source.find('{', match.end())
        if body_start == -1:
            # Malformed inline without a body, treat as normal text
            result.append(source[match.start():match.end()])
            i = match.end()
            continue

        i = body_start
        brace_count = 1
        i += 1

        while i < n and brace_count > 0:
            if source[i] == '{':
                brace_count += 1
            elif source[i] == '}':
                brace_count -= 1
            i += 1

        # If there is a semicolon mid-line, skip it
        while i < n and source[i] in ' \t\n;':
            i += 1

    return ''.join(result)


def sanitize_cdef(cdef: str, pkg: str) -> str:
    """Sanitize cdef by removing unsupported declarations."""
    # Parse multi-line patterns first
    cdef = remove_static_inline_functions(cdef)
    cdef = remove_deprecated_functions(cdef)

    output_lines = cdef.splitlines()
    filtered_lines = []

    line_re = re.compile(r'# \d+ "(.*?)"')

    current_file = None
    pkg_lines = True

    # Parse single-line patterns next
    for line in output_lines:
        # Parse and ignore GCC comments
        if line.startswith("#"):
            match = line_re.match(line)
            if match:
                current_file = match.group(1)
                pkg_lines = pkg in current_file
            continue

        # Ignore non-package declarations
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
