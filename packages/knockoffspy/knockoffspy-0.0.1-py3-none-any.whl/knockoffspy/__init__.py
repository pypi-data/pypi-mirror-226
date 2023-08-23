# source: https://github.com/SciML/diffeqpy/blob/master/diffeqpy/__init__.py

import os
import shutil
import subprocess
import sys

from jill.install import install_julia

script_dir = os.path.dirname(os.path.realpath(__file__))


def _find_julia():
    # TODO: this should probably fallback to query jill
    return shutil.which("julia")


def install(*, confirm=True):
    """
    Install Julia (if required) and Julia packages required for diffeqpy.
    """
    julia = _find_julia()
    if not julia:
        print("No Julia version found. Installing Julia.")
        install_julia(confirm=confirm)
        julia = _find_julia()
        if not julia:
            raise RuntimeError(
                "Julia installed with jill but `julia` binary cannot be found in the path"
            )
    env = os.environ.copy()
    env["PYTHON"] = sys.executable
    subprocess.check_call([julia, os.path.join(script_dir, "install.jl")], env=env)


def _ensure_installed(*kwargs):
    if not _find_julia():
        # TODO: this should probably ensure that packages are installed too
        install(*kwargs)