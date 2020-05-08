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

# Extracted from https://stackoverflow.com/questions/58648739/how-to-check-if-python-package-is-latest-version-programmatically
import subprocess
import sys
def check(name):
    latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'install', '{}==random'.format(name)], capture_output=True, text=True))
    latest_version = latest_version[latest_version.find('(from versions:')+15:]
    latest_version = latest_version[:latest_version.find(')')]
    latest_version = latest_version.replace(' ','').split(',')[-1]

    current_version = str(subprocess.run([sys.executable, '-m', 'pip', 'show', '{}'.format(name)], capture_output=True, text=True))
    current_version = current_version[current_version.find('Version:')+8:]
    current_version = current_version[:current_version.find('\\n')].replace(' ','') 

    if latest_version == current_version:
        return True, latest_version
    else:
        return False, latest_version

print (" Welcome to LPS Maestro!")
print (" - Checking for updates...")
try:
    v = check('lps-maestro')
    if (v[0] == True):
        print (" - This is the latest version ({})".format(v[1]))
    else:
        print (" => Version {} is available, please update!".format(v[1]))
except:
    print (" - Failed to check for updates")