__version__ = '2022.12.19'
__vaccel__ = '0.1.0'

import os
import sys
import ctypes

flags = sys.getdlopenflags()

sys.setdlopenflags(os.RTLD_LAZY | os.RTLD_GLOBAL)
ctypes.CDLL('libvaccel-python.so')

# Reset flags
sys.setdlopenflags(flags)
