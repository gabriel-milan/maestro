__all__ = [
    'getCredentialsData',
    'decode_base64'
]

import os
import sys
import argparse
import requests
import pickle
import base64
from pathlib import Path
from lps_maestro.constants import *
import re

def getCredentialsData ():
  home = str(Path.home())
  try:
    f = open("{}/{}".format(home, CREDENTIALS_FILE), "r")
    if f.mode == 'r':
      content = f.read()
      f.close()
      return content
  except FileNotFoundError:
    print ("Please authenticate first")
    return False

def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)
