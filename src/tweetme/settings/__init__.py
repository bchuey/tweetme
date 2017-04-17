# must import the base, local, production files
# whatever is on the bottom will override anything above

from .base import *

from .production import *

try:
    from .local import *
except:
    pass
