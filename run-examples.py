# SPDX-License-Identifier: Apache-2.0

import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pkgconfig

from build_ffi import compile_ffi

EXAMPLES_DIR = Path(__file__).parent / "examples"


def setup_vaccel():
    if importlib.util.find_spec("vaccel") is None:
        ffi_lib = Path("vaccel/_libvaccel.abi3.so")
        if not ffi_lib.is_file():
            compile_ffi()

    os.environ["VACCEL_PLUGINS"] = "libvaccel-noop.so"
    os.environ["VACCEL_LOG_LEVEL"] = "4"


def get_vaccel_paths() -> dict[str, Path]:
    variables = pkgconfig.variables("vaccel")
    return {
        "prefix": Path(variables["prefix"]),
        "lib": Path(variables["libdir"]),
        "images": Path(variables["prefix"]) / "share" / "vaccel" / "images",
        "models": Path(variables["prefix"]) / "share" / "vaccel" / "models",
        "input": Path(variables["prefix"]) / "share" / "vaccel" / "input",
    }


def get_examples_args(vaccel_paths: dict[str, Path]) -> dict[str, Path]:
    return {
        "classify": [
            vaccel_paths["images"] / "example.jpg",
            "-m",
            vaccel_paths["models"] / "torch" / "cnn_trace.pt",
        ]
    }


def find_examples(directory: Path) -> dict[str, Path]:
    examples = {}
    for file in directory.iterdir():
        if file.suffix == ".py" and not file.stem.startswith("_"):
            examples[file.stem] = file.resolve()
    return examples


def run_example(path: Path, name: str, vaccel_paths: dict[str, Path]) -> int:
    examples_args = get_examples_args(vaccel_paths)
    args = examples_args.get(name, [])
    print(f"Running: {path}")
    result = subprocess.run(
        [sys.executable, str(path), *args], text=True, check=True
    )
    return result.returncode


def main():
    if not EXAMPLES_DIR.is_dir():
        print(f"Examples directory not found: {EXAMPLES_DIR}")
        sys.exit(1)

    setup_vaccel()

    examples = find_examples(EXAMPLES_DIR)
    if not examples:
        print("No examples found.")
        return

    parser = argparse.ArgumentParser(
        description="Manage and run example scripts."
    )
    parser.add_argument(
        "-e", "--example", required=False, help="Name of example to run"
    )
    args = parser.parse_args()

    failures = []
    vaccel_paths = get_vaccel_paths()
    if args.example:
        if args.example not in examples:
            print(f"Error: Example '{args.example}' not found.")
            sys.exit(1)
        ret = run_example(examples[args.example], args.example, vaccel_paths)
        if ret != 0:
            failures.append(args.example)
    else:
        for name, path in examples.items():
            ret = run_example(path, name, vaccel_paths)
            if ret != 0:
                failures.append(name)

    if failures:
        print("\nSome examples failed:")
        for fail in failures:
            print(f"- {fail}")
        sys.exit(1)
    else:
        print("\nAll examples ran successfully.")


if __name__ == "__main__":
    main()
