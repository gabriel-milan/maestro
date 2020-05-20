__all__ = [
  'task'
]

import os
import sys
import argparse
import requests
import pickle
import base64
from pathlib import Path
from lps_maestro.utils import getCredentialsData, decode_base64
from lps_maestro.constants import *

class Task ():
  def create( self, taskname,
                    dataFile,
                    configFile,
                    execCommand,
                    containerImage,
                    queue='cpu_small',
                    secondaryDS=None,
                    et=None,
                    eta=None,
                    dry_run=False):

    if taskname.split('.')[0] != 'user':
      print( 'The task name must start with "user.<username>.taskname."')
      raise BaseException
    username = taskname.split('.')[1]

    credentials = getCredentialsData()
    if credentials == False:
      return

    if dry_run:
      print ("Please disable dry run.")
      return

    data = {
      'username'              : username,
      'taskname'              : taskname,
      'configFile'            : configFile,
      'dataFile'              : dataFile,
      'containerImage'        : containerImage,
      'secondaryDS'           : secondaryDS if secondaryDS else '',
      'execCommand'           : execCommand,
      'et'                    : et if et else 0,
      'eta'                   : eta if eta else 0,
      'gpu'                   : int(gpu),
      'credentials'           : credentials
    }

    try:
      r = requests.post(url='http://146.164.147.170:5020/create-task', data=data)
      print (r.text)
    except requests.exceptions.ConnectionError:
      print ("Failed to connect to LPS Cluster.")

  def delete( self, taskname ):

    if taskname.split('.')[0] != 'user':
      print( 'The task name must start with "user.<username>.taskname."')
      raise BaseException
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
      print ("Failed to connect to LPS Cluster.")

  def retry( self, taskname ):

    if taskname.split('.')[0] != 'user':
      print( 'The task name must start with "user.<username>.taskname."')
      raise BaseException
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
      print ("Failed to connect to LPS Cluster.")

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
      print ("Failed to connect to LPS Cluster.")

  def kill( self, username, taskname ):

    if taskname.split('.')[0] != 'user':
      print( 'The task name must start with "user.<username>.taskname."')
      raise BaseException

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
      print ("Failed to connect to LPS Cluster.")

task = Task()