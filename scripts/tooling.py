"""
Poetry scripts, runable using 'poetry run'.
"""
import glob
import os
import os.path
import subprocess
import sys
from typing import List, NamedTuple, Optional

import toml

SUPPORTED_SRC_FOLDERS = ["src", "electricitymap"]


class Directories(NamedTuple):
    src: str
    tests: Optional[str]

    def to_list(self) -> List[str]:
        return list(filter(None, [self.src, self.tests]))


def _get_dirs() -> Directories:
    src_folder = next((d for d in SUPPORTED_SRC_FOLDERS if os.path.isdir(d)), None)

    if src_folder is None:
        parsed_toml = toml.load("pyproject.toml")
        src_folder = parsed_toml["tool"]["poetry"]["name"]

    assert (
        src_folder
    ), f"Source folder was not found, expected one of {SUPPORTED_SRC_FOLDERS}"
    return Directories(
        src=src_folder, tests="tests" if os.path.isdir("tests") else None
    )


pkg_tooling_path = os.path.dirname(os.path.realpath(__file__))
mypy_ini_path = os.path.relpath(os.path.join(pkg_tooling_path, "mypy.ini"))
dirs = _get_dirs()
notebooks = [
    f"'{p}'"
    for p in (
        glob.glob("*.ipynb")
        + glob.glob(f"{dirs.src}/**/*.ipynb", recursive=True)
        + glob.glob(f"notebooks/**/*.ipynb", recursive=True)
    )
]


def _run(cmd: str):
    cmd_with_args = f"{cmd} {' '.join(sys.argv[1:])}"
    print(f"⚙︎ {cmd_with_args}")
    r = subprocess.run(cmd_with_args, shell=True).returncode
    if r != 0:
        print(f"FAILED: {cmd}")
        sys.exit(r)


# ===============================
# External commands
# ===============================


def format():
    isort_config = f"--profile=black --project=electricitymap --known-local-folder=src --known-local-folder=tests"
    _run(f"isort {isort_config} .")
    _run("black .")
    if notebooks:
        _run(f"isort {isort_config} {' '.join(notebooks)}")
        _run(f"nbqa black {' '.join(notebooks)}")


def lint():
    _run(f"pylint -E {' '.join(dirs.to_list())}")
    if notebooks:
        _run(f"nbqa pylint -E {' '.join(notebooks)}")


def test():
    if dirs.tests:
        _run("pytest")
    else:
        print("No tests folder found... 😿")


def test_watch():
    if dirs.tests:
        _run(f"pytest-watch {dirs.src} {dirs.tests} --nobeep --clear -- -lsvv")
    else:
        print("No tests folder found... 😿")


def typecheck():
    mypy_conifg = (
        f"--config-file={mypy_ini_path} --namespace-packages --show-error-codes"
    )
    _run(f"mypy {mypy_conifg} -p {dirs.src}")
    # NOTE: we could run mypy on notebooks but they are rather tricky to typecheck


def check():
    lint()
    typecheck()
    test()


def check_untyped():
    lint()
    test()
