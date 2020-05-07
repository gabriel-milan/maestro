__all__ = [
  'castor'
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

class Castor ():

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
        r = requests.post(url='http://146.164.147.170:5020/list-datasets', data=data)
        print (r.json()['message'])
      else:
        r = requests.post(url='http://146.164.147.170:5020/list-datasets-py', data=data)
        try:
          return r.json()
        except:
          pickled_response = r.content.decode('utf-8')
          df = pickle.loads(decode_base64(pickled_response.encode()))
          return df
    except requests.exceptions.ConnectionError:
      print ("Failed to connect to LPS Cluster.")

  def delete( self, datasetname ):

    if datasetname.split('.')[0] != 'user':
      print( 'The dataset name must start with "user.<username>.taskname."')
      raise BaseException
    username = datasetname.split('.')[1]

    credentials = getCredentialsData()
    if credentials == False:
      return

    data = {
      'username':username,
      'datasetname':datasetname,
      'credentials':credentials
    }

    try:
      r = requests.post(url='http://146.164.147.170:5020/delete-dataset', data=data)
      print (r.text)
    except requests.exceptions.ConnectionError:
      print ("Failed to connect to LPS Cluster.")

  def download( self, datasetname ):

    if datasetname.split('.')[0] != 'user':
      print ( 'The dataset name must start with "user.<username>.taskname."')
    username = datasetname.split('.')[1]

    credentials = getCredentialsData()
    if credentials == False:
      return

    data = {
      'username':username,
      'datasetname':datasetname,
      'credentials':credentials
    }

    try:
      r = requests.post(url='http://146.164.147.170:5020/download-dataset', data=data)
      try:
        if r.json()['message'] == "Internal Server Error":
          print (r.text)
          return
        error_code = r.json()['error_code']
        print (r.text)
      except:
        with open('./{}'.format('{}.zip'.format(datasetname)), 'wb') as f:
          f.write(r.content)
    except requests.exceptions.ConnectionError:
      print ("Failed to connect to LPS Cluster.")

  def upload( self , datasetname, path ):

    if datasetname.split('.')[0] != 'user':
      print( 'The dataset name must start with "user.<username>.taskname."')
      raise BaseException
    username = datasetname.split('.')[1]

    credentials = getCredentialsData()
    if credentials == False:
      return

    data = {
      'username':username,
      'datasetname':datasetname,
      'credentials':credentials
    }

    # Parsing input
    file_list = []
    if (os.path.isdir(path)):
      for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)):
          file_list.append (os.path.join(path, i))
      if (not file_list):
        print ("File does not exist.")
    else:
      if (not os.path.exists(path)):
        print ("File does not exist.")
      else:
        file_list.append(path)
    
    for filename in file_list:
      fin = open(filename, 'rb')
      files = {'file':fin}
      try:
        r = requests.post(url='http://146.164.147.170:5020/upload-dataset', data=data, files=files)
        print (r.text)
      except requests.exceptions.ConnectionError:
        print ("Failed to connect to LPS Cluster.")
      finally:
        fin.close()

castor = Castor()