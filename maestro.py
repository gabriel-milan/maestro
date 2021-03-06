#!/usr/bin/env python3

import os
import sys
import argparse
import requests
import pickle
import base64
from pathlib import Path
import lps_maestro
from lps_maestro.utils import getCredentialsData
from lps_maestro.castor import castor
from lps_maestro.task import task
from lps_maestro.authenticate import authenticate

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
class AuthenticationParser ():

  def __init__ (self, args=None):
    self.__authenticate = authenticate
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
      print(args.password)
      self.authenticate(args.username, args.password)

  def authenticate (self, username, password):
    return self.__authenticate.authenticate(username, password)

#
# Dataset parser
#
class DatasetParser():

  def __init__(self, args=None):
    self.__castor = castor
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
        self.list(args.username,)

  def list( self, username ):
    return self.__castor.list (username, cli=True)
    
  def delete( self, datasetname ):
    return self.__castor.delete (datasetname)

  def download( self, datasetname ):
    return self.__castor.download (datasetname)

  def upload( self , datasetname, path ):
    return self.__castor.upload (datasetname, path)

#
# Task parser
#
class TaskParser():


  def __init__(self , args=None):
    self.__task = task
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
      create_parser.add_argument('--queue', action='store', dest='queue', required=True, default='cpu_small',
                          help = "The desired cluster queue: cpu_small, nvidia or cpu_large")
      create_parser.add_argument('--sd','--secondaryDS', action='store', dest='secondaryDS', required=False,  default="{}",
                          help = "The secondary datasets to append in the --exec command. This should be:" +
                          "--secondaryData='{'REF':'path/to/my/extra/data',...}'")
      create_parser.add_argument('--et', action='store', dest='et', required=False,default=None,
                          help = "The ET region (for ringer users)")
      create_parser.add_argument('--eta', action='store', dest='eta', required=False,default=None,
                          help = "The ETA region (for ringer users)")
      create_parser.add_argument('--dry_run', action='store_true', dest='dry_run', required=False, default=False,
                          help = "Use this as debugger.")
      create_parser.add_argument('--is_dummy_data', action='store_true', dest='is_dummy_data', required=False, default=False,
                          help = "Not use the data (%DATA).")
      create_parser.add_argument('--is_dummy_config', action='store_true', dest='is_dummy_config', required=False, default=False,
                          help = "Not use the data (%IN).")



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
      kill_parser.add_argument('-t','--task', action='store', dest='taskname', required=False,
                    help = "The name of the task you want to kill")

      queue_parser = argparse.ArgumentParser(description = '', add_help = False)
      queue_parser.add_argument('-n','--name', action='store', dest='queuename', required=True,
                    help = "The queue name")






      parent = argparse.ArgumentParser(description = '', add_help = False)
      subparser = parent.add_subparsers(dest='option')

      subparser.add_parser('create', parents=[create_parser])
      subparser.add_parser('retry', parents=[retry_parser])
      subparser.add_parser('delete', parents=[delete_parser])
      subparser.add_parser('list', parents=[list_parser])
      subparser.add_parser('kill', parents=[kill_parser])
      subparser.add_parser('queue', parents=[queue_parser])
      args.add_parser( 'task', parents=[parent] )

  def compile( self, args ):
    if args.mode == 'task':

      if args.option == 'create':
        return self.__task.create(
          args.taskname, 
          args.dataFile, 
          args.configFile, 
          args.execCommand,
          args.containerImage, 
          queue=args.queue, 
          secondaryDS=args.secondaryDS, 
          et=args.et, 
          eta=args.eta, 
          dry_run=args.dry_run, 
          is_dummy_data=args.is_dummy_data, 
          is_dummy_config=args.is_dummy_config,
        )
      elif args.option == 'retry':
        return self.__task.retry(args.taskname)
      elif args.option == 'delete':
        return self.__task.delete(args.taskname)
      elif args.option == 'list':
        return self.__task.list(args.username, cli=True)
      elif args.option == 'kill':
        return self.__task.kill(args.taskname)
      elif args.option == 'queue':
        return self.__task.queue(args.queuename)





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
