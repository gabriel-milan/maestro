__all__ = [
  'authenticate'
]

import os
import sys
import argparse
from Gaugi import Logger
from Gaugi.messenger.macros import *
import requests
from hashlib import sha256, md5
import pickle
import base64
from pathlib import Path
from lps_maestro.utils import getCredentialsData
from lps_maestro.constants import *

class Authenticate (Logger):

  def __init__(self):
    Logger.__init__(self)
    self.__class__ = type(self.__class__.__name__, (self.__class__,), {})
    self.__class__.__call__ = self.authenticate

  def hashPw (self, password):
    m = md5()
    m.update(password.encode('utf-8'))
    return m.hexdigest()

  def authenticate (self, username, password):
    MSG_INFO (self, "Trying to connect...")
    data = {
      'username':username,
      'password':self.hashPw(password)
    }
    try:
      r = requests.post(url='http://146.164.147.170:5020/authenticate', data=data)
      MSG_INFO (self, r.text)
      if (r.json()['error_code'] == 200):
        pickled_data = pickle.dumps(data)
        b64_pickled_data = base64.b64encode(pickled_data)
        home = str(Path.home())
        f = open("{}/{}".format(home, CREDENTIALS_FILE), "wb+")
        f.write(b64_pickled_data)
        f.close()
    except requests.exceptions.ConnectionError:
      MSG_ERROR (self, "Failed to connect to LPS Cluster.")

authenticate = Authenticate()