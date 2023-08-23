# source: https://github.com/SciML/diffeqpy/blob/master/diffeqpy/de.py

import os
import sys

from . import _ensure_installed

# This is terrifying to many people. However, it seems SciML takes pragmatic approach.
_ensure_installed()

# PyJulia have to be loaded after `_ensure_installed()`
from julia import Main

script_dir = os.path.dirname(os.path.realpath(__file__))
Main.include(os.path.join(script_dir, "setup.jl"))

from julia import Knockoffs
sys.modules[__name__] = Knockoffs   # mutate myself
