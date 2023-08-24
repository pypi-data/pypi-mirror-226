r"""
The CausalRec is a Python package contains.....
"""


# @Author: tuyenvu
# """init module."""

import sys
from CausalRec.CausalRec import *
from CausalRec.binary_evaluation import *
from . import CausalRec



# -------------------------------- VERSION --------------------------------- #
# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
#   X.Y
#   X.Y.Z   # For bugfix releases
#
# Admissible pre-release markers:
#   X.YaN   # Alpha release
#   X.YbN   # Beta release
#   X.YrcN  # Release Candidate
#   X.Y     # Final release
#
# Dev branch marker is: 'X.Y.dev' or 'X.Y.devN' where N is an integer.
# 'X.Y.dev0' is the canonical version of 'X.Y.dev'
#
__version__ = '0.0.1.1'
#10/06/2023: CausalRec0.0.3
#08/06/2023: CausalRec0.0.2
#01/06/2023: CausalRec0.0.1

# 31/05/2023: V0.0.3 tPypack
# 25/05/2023: V0.0.2 add ..."


#18/05/2023 version0.0.1:

# ---------------------------- GLOBAL VARIABLES ---------------------------- #
PYTHON_VERSION = sys.version_info[0]


__all__ = [  'PYTHON_VERSION', ]


