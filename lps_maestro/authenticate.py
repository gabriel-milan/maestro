__all__ = [
  'authenticate'
]

import os
import sys
import argparse
import requests
from hashlib import sha256, md5
import pickle
import base64
from pathlib import Path
from lps_maestro.utils import getCredentialsData
from lps_maestro.constants import *

class Authenticate ():

  def __init__(self):
    self.__class__ = type(self.__class__.__name__, (self.__class__,), {})
    self.__class__.__call__ = self.authenticate

  def hashPw (self, password):
    m = md5()
    m.update(password.encode('utf-8'))
    return m.hexdigest()

  def authenticate (self, username, password):
    print ("Trying to connect...")
    data = {
      'username':username,
      'password':password
    }
    try:
      r = requests.post(url='http://146.164.147.170:5020/authenticate', data=data)
      print (r.text)
      if (r.json()['error_code'] == 200):
        home = str(Path.home())
        f = open("{}/{}".format(home, CREDENTIALS_FILE), "wb+")
        f.write("${}${}".format(username, r.json()['token']).encode('utf-8'))
        f.close()
    except requests.exceptions.ConnectionError:
      print ("Failed to connect to LPS Cluster.")

authenticate = Authenticate()