#!/usr/bin/env python3

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

#
# Macros
#
CREDENTIALS_FILE = '.maestro_credentials'

#
# Utils
#
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

#
# Authentication parser
#
class AuthenticationParser (Logger):

  def __init__ (self, args=None):
    
    Logger.__init__(self)

    if args:

      # Authenticate
      parser = argparse.ArgumentParser(description = '', add_help = False)
      parser.add_argument(
        '-u', '--username', action='store', dest='username', required = True,
        help = "Your username"
      )
      parser.add_argument(
        '-p', '--password', action='store', dest='password', required = True,
        help = "Your password"
      )

      args.add_parser( 'authenticate', parents=[parser] )

  def compile( self, args ):
    if args.mode == 'authenticate':
      self.authenticate(args.username, args.password)

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

#
# Dataset parser
#
class DatasetParser(Logger):

  def __init__(self, args=None):

    Logger.__init__(self)
    if args:

      # Upload
      upload_parser = argparse.ArgumentParser(description = 'Dataset upload CLI.' , add_help = False)
      upload_parser.add_argument('-d', '--dataset', action='store', dest='datasetname', required=True,
                                  help = "The dataset name that will be registered on the database (e.g: user.jodafons...)")
      upload_parser.add_argument('-p','--path', action='store', dest='path', required=True,
                                  help = "The path to the dataset file")
      
      # Download
      download_parser = argparse.ArgumentParser(description = 'Dataset donwload CLI', add_help = False)
      download_parser.add_argument('-d', '--dataset', action='store', dest='datasetname', required=True,
                                   help = "The dataset name to be downloaded")

      # Delete                             
      delete_parser = argparse.ArgumentParser(description = 'Dataset delete CLI', add_help = False)
      delete_parser.add_argument('-d', '--dataset', action='store', dest='datasetname', required=True,
                                   help = "The dataset name to be removed")

      # List                             
      list_parser = argparse.ArgumentParser(description = 'Dataset listing', add_help = False)
      list_parser.add_argument('-u', '--user', action='store', dest='username', required=True,
                                   help = "List all datasets for a selected user")

      parent = argparse.ArgumentParser(description = '',add_help = False)
      subparser = parent.add_subparsers(dest='option')

      subparser.add_parser('upload', parents=[upload_parser])
      subparser.add_parser('download', parents=[download_parser])
      subparser.add_parser('delete', parents=[delete_parser])
      subparser.add_parser('list', parents=[list_parser])
      args.add_parser( 'castor', parents=[parent] )

  def compile( self, args ):
    if args.mode == 'castor':
      if args.option == 'upload':
        self.upload(args.datasetname, args.path)
      elif args.option == 'download':
        self.download(args.datasetname)
      elif args.option == 'delete':
        self.delete(args.datasetname)
      elif args.option == 'list':
        self.list(args.username)

  def list( self, username ):

    credentials = getCredentialsData()
    if credentials == False:
      return

    data = {
      'username':username,
      'credentials':credentials
    }
    try:
      r = requests.post(url='http://146.164.147.170:5020/list-datasets', data=data)
      print (r.json()['message'])
    except requests.exceptions.ConnectionError:
      MSG_ERROR (self, "Failed to connect to LPS Cluster.")

  def delete( self, datasetname ):

    if datasetname.split('.')[0] != 'user':
      MSG_FATAL( self, 'The dataset name must start with "user.<username>.taskname."')
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
      MSG_ERROR (self, "Failed to connect to LPS Cluster.")

  def download( self, datasetname ):

    if datasetname.split('.')[0] != 'user':
      MSG_FATAL( self, 'The dataset name must start with "user.<username>.taskname."')
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
      MSG_ERROR (self, "Failed to connect to LPS Cluster.")

  def upload( self , datasetname, path ):

    if datasetname.split('.')[0] != 'user':
      MSG_FATAL( self, 'The dataset name must start with "user.<username>.taskname."')
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
        MSG_ERROR (self, "File does not exist.")
    else:
      if (not os.path.exists(path)):
        MSG_ERROR (self, "File does not exist.")
      else:
        file_list.append(path)
    
    for filename in file_list:
      fin = open(filename, 'rb')
      files = {'file':fin}
      try:
        r = requests.post(url='http://146.164.147.170:5020/upload-dataset', data=data, files=files)
        print (r.text)
      except requests.exceptions.ConnectionError:
        MSG_ERROR (self, "Failed to connect to LPS Cluster.")
      finally:
        fin.close()

#
# Task parser
#
class TaskParser(Logger):


  def __init__(self , args=None):
    Logger.__init__(self)
    if args:
      # Create
      create_parser = argparse.ArgumentParser(description = '', add_help = False)
      create_parser.add_argument('-c','--configFile', action='store',
                          dest='configFile', required = True,
                          help = "The job config file that will be used to configure the job (sort and init).")
      create_parser.add_argument('-d','--dataFile', action='store',
                          dest='dataFile', required = True,
                          help = "The data/target file used to train the model.")
      create_parser.add_argument('--exec', action='store', dest='execCommand', required=True,
                          help = "The exec command")
      create_parser.add_argument('--containerImage', action='store', dest='containerImage', required=True,
                          help = "The container image point to docker hub. The image must be public.")
      create_parser.add_argument('-t','--task', action='store', dest='taskname', required=True,
                          help = "The task name to append in the database.")
      create_parser.add_argument('--sd','--secondaryDS', action='store', dest='secondaryDS', required=False,  default="{}",
                          help = "The secondary datasets to append in the --exec command. This should be:" +
                          "--secondaryData='{'REF':'path/to/my/extra/data',...}'")
      create_parser.add_argument('--gpu', action='store_true', dest='gpu', required=False, default=False,
                          help = "Send these jobs to GPU slots")
      create_parser.add_argument('--et', action='store', dest='et', required=False,default=None,
                          help = "The ET region (for ringer users)")
      create_parser.add_argument('--eta', action='store', dest='eta', required=False,default=None,
                          help = "The ETA region (for ringer users)")
      create_parser.add_argument('--dry_run', action='store_true', dest='dry_run', required=False, default=False,
                          help = "Use this as debugger.")

      # Retry
      retry_parser = argparse.ArgumentParser(description = '', add_help = False)
      retry_parser.add_argument('-t','--task', action='store', dest='taskname', required=True,
                    help = "The name of the task you want to retry")
      
      # Delete
      delete_parser = argparse.ArgumentParser(description = '', add_help = False)
      delete_parser.add_argument('-t','--task', action='store', dest='taskname', required=True,
                    help = "The name of the task you want to remove")
      
      # List
      list_parser = argparse.ArgumentParser(description = '', add_help = False)
      list_parser.add_argument('-u','--user', action='store', dest='username', required=True,
                    help = "The username")

      # Kill
      kill_parser = argparse.ArgumentParser(description = '', add_help = False)
      kill_parser.add_argument('-u','--user', action='store', dest='username', required=True,
                    help = "The username.")
      kill_parser.add_argument('-t','--task', action='store', dest='taskname', required=False,
                    help = "The name of the task you want to kill")
      kill_parser.add_argument('-a','--all', action='store_true', dest='kill_all', required=False, default=False,
                    help = "Remove all tasks from given username")

      parent = argparse.ArgumentParser(description = '', add_help = False)
      subparser = parent.add_subparsers(dest='option')

      subparser.add_parser('create', parents=[create_parser])
      subparser.add_parser('retry', parents=[retry_parser])
      subparser.add_parser('delete', parents=[delete_parser])
      subparser.add_parser('list', parents=[list_parser])
      subparser.add_parser('kill', parents=[kill_parser])
      args.add_parser( 'task', parents=[parent] )

  def compile( self, args ):
    if args.mode == 'task':
      if args.option == 'create':
        self.create(args.taskname, args.dataFile, args.configFile, args.secondaryDS,
                    args.execCommand,args.containerImage,args.et,args.eta,args.gpu,
                    args.dry_run)
      elif args.option == 'retry':
        self.retry(args.taskname)
      elif args.option == 'delete':
        self.delete(args.taskname)
      elif args.option == 'list':
        self.list(args.username)
      elif args.option == 'kill':
        self.kill(args.username, 'all' if args.kill_all else args.taskname)

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

  def list( self, username ):

    credentials = getCredentialsData()
    if credentials == False:
      return

    data = {
      'username':username,
      'credentials':credentials
    }
    try:
      r = requests.post(url='http://146.164.147.170:5020/list-tasks', data=data)
      print (r.json()['message'])
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

parser = argparse.ArgumentParser()
commands = parser.add_subparsers(dest='mode')

engine = [
  DatasetParser(commands),
  TaskParser(commands),
  AuthenticationParser(commands),
]

if len(sys.argv)==1:
  print(parser.print_help())
  sys.exit(1)

args = parser.parse_args()

for e in engine:
  e.compile(args)