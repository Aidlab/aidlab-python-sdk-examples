import sys
if 'linux' in sys.platform or 'win32' in sys.platform:
    from .windows import *
elif 'darwin' in sys.platform:
    from .mac import *
else:
    raise RuntimeError("Unsupported operating system: {}".format(sys.platform))
