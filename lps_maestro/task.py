__all__ = [
  'task'
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
from lps_maestro.utils import getCredentialsData, decode_base64
from lps_maestro.constants import *

class Task (Logger):

  def __init__ (self):
    Logger.__init__(self)
  
  def create( self, taskname, dataFile,
                    configFile, secondaryDS,
                    execCommand, containerImage, et=None, eta=None, gpu=False,
                    dry_run=False):

    if taskname.split('.')[0] != 'user':
      MSG_FATAL( self, 'The task name must start with "user.<username>.taskname."')
    username = taskname.split('.')[1]

    credentials = getCredentialsData()
    if credentials == False:
      return

    if dry_run:
      MSG_WARNING (self, "Please disable dry run.")
      return

    data = {
      'username'              : username,
      'taskname'              : taskname,
      'configFile'            : configFile,
      'dataFile'              : dataFile,
      'containerImage'        : containerImage,
      'secondaryDS'           : secondaryDS,
      'execCommand'           : execCommand,
      'et'                    : et,
      'eta'                   : eta,
      'gpu'                   : int(gpu),
      'credentials'           : credentials
    }

    try:
      r = requests.post(url='http://146.164.147.170:5020/create-task', data=data)
      print (r.text)
    except requests.exceptions.ConnectionError:
      MSG_ERROR (self, "Failed to connect to LPS Cluster.")

  def delete( self, taskname ):

    if taskname.split('.')[0] != 'user':
      MSG_FATAL( self, 'The task name must start with "user.<username>.taskname."')
    username = taskname.split('.')[1]

    credentials = getCredentialsData()
    if credentials == False:
      return

    data = {
      'username':username,
      'taskname':taskname,
      'credentials':credentials
    }

    try:
      r = requests.post(url='http://146.164.147.170:5020/delete-task', data=data)
      print (r.text)
    except requests.exceptions.ConnectionError:
      MSG_ERROR (self, "Failed to connect to LPS Cluster.")

  def retry( self, taskname ):

    if taskname.split('.')[0] != 'user':
      MSG_FATAL( self, 'The task name must start with "user.<username>.taskname."')
    username = taskname.split('.')[1]

    credentials = getCredentialsData()
    if credentials == False:
      return

    data = {
      'username':username,
      'taskname':taskname,
      'credentials':credentials
    }

    try:
      r = requests.post(url='http://146.164.147.170:5020/retry-task', data=data)
      print (r.text)
    except requests.exceptions.ConnectionError:
      MSG_ERROR (self, "Failed to connect to LPS Cluster.")

  def list( self, username, cli=False ):

    credentials = getCredentialsData()
    if credentials == False:
      return

    data = {
      'username':username,
      'credentials':credentials
    }
    try:
      if cli:
        r = requests.post(url='http://146.164.147.170:5020/list-tasks', data=data)
        print (r.json()['message'])
      else:
        r = requests.post(url='http://146.164.147.170:5020/list-tasks-py', data=data)
        try:
          return r.json()
        except:
          pickled_response = r.content.decode('utf-8')
          df = pickle.loads(decode_base64(pickled_response.encode()))
          return df
    except requests.exceptions.ConnectionError:
      MSG_ERROR (self, "Failed to connect to LPS Cluster.")

  def kill( self, username, taskname ):

    if taskname.split('.')[0] != 'user':
      MSG_FATAL( self, 'The task name must start with "user.<username>.taskname."')

    credentials = getCredentialsData()
    if credentials == False:
      return

    data = {
      'username':username,
      'taskname':taskname,
      'credentials':credentials
    }

    try:
      r = requests.post(url='http://146.164.147.170:5020/kill-task', data=data)
      print (r.text)
    except requests.exceptions.ConnectionError:
      MSG_ERROR (self, "Failed to connect to LPS Cluster.")

task = Task()