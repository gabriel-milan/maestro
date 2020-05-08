__name__ = "lps_maestro"

__all__ = []

from . import authenticate
__all__.extend(authenticate.__all__)
from .authenticate import *

from . import castor
__all__.extend(castor.__all__)
from .castor import *

from . import constants
__all__.extend(constants.__all__)
from .constants import *

from . import task
__all__.extend(task.__all__)
from .task import *

from . import utils
__all__.extend(utils.__all__)
from .utils import *

# Checking for new versions
import pkg_resources
import requests
def check(name):
    # Getting current version
    current_version = pkg_resources.get_distribution('lps_maestro').version
    # Getting latest version
    r = requests.get('https://pypi.org/pypi/lps-maestro/json')
    d = r.json()
    latest_version = list(d['releases'].keys())[-1]
    if latest_version == current_version:
        return True, latest_version, current_version
    else:
        return False, latest_version, current_version

print (" Welcome to LPS Maestro!")
print (" - Checking for updates...")
try:
    v = check('lps-maestro')
    if (v[0] == True):
        print (" - This is the latest version available! (current={}, latest={})".format(v[1], v[2]))
    else:
        print (" => Version {} is available, please update over your {}!".format(v[1], v[2]))
except:
    print (" - Failed to check for updates")