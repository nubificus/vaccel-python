__version__ = '2021.6.28'
__vaccel__ = '0.1.0'

import os, sys, ctypes

flags = sys.getdlopenflags()

sys.setdlopenflags(os.RTLD_LAZY | os.RTLD_GLOBAL)
ctypes.CDLL('libvaccel-python.so')

# Reset flags
sys.setdlopenflags(flags)
