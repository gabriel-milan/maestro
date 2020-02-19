#!/usr/bin/env python3

import sys
import argparse
from Gaugi import Logger

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

    # TODO:
    # - Make request here using username, in order to list all datasets related
    print ("Make request!")

  def delete( self, datasetname ):

    if datasetname.split('.')[0] != 'user':
      MSG_FATAL( self, 'The dataset name must start with "user.<username>.taskname."')
    username = datasetname.split('.')[1]

    # TODO:
    # - Make request here using username and dataset, in order to check if both exist and then delete the dataset
    print ("Make request!")

  def download( self, datasetname ):

    if datasetname.split('.')[0] != 'user':
      MSG_FATAL( self, 'The dataset name must start with "user.<username>.taskname."')
    username = datasetname.split('.')[1]

    # TODO:
    # - Make request here using username and dataset, in order to check if both exist and then download the dataset
    print ("Make request!")

  def upload( self , datasetname, path ):

    if datasetname.split('.')[0] != 'user':
      MSG_FATAL( self, 'The dataset name must start with "user.<username>.taskname."')
    username = datasetname.split('.')[1]

    # TODO:
    # - Make request here using username and dataset, in order to check if both exist and then upload a new dataset
    print ("Make request!")

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
                    args.bypass_test_job, args.dry_run)
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

    # TODO:
    # - Make request here using everything, in order to check policies and launching a new task
    print ("Make request!")

  def delete( self, taskname ):

    if taskname.split('.')[0] != 'user':
      MSG_FATAL( self, 'The task name must start with "user.<username>.taskname."')
    username = taskname.split('.')[1]

    # TODO:
    # - Make request here using everything, in order to check policies and delete a task
    print ("Make request!")

  def retry( self, taskname ):

    if taskname.split('.')[0] != 'user':
      MSG_FATAL( self, 'The task name must start with "user.<username>.taskname."')
    username = taskname.split('.')[1]

    # TODO:
    # - Make request here using everything, in order to check policies and retry a task
    print ("Make request!")

  def list( self, username ):

    # TODO:
    # - Make request here using the username, in order to list all tasks related to him
    print ("Make request!")

  def kill( self, username, taskname ):

    # TODO:
    # - Make request here using everything, in order to kill a task
    print ("Make request!")

parser = argparse.ArgumentParser()
commands = parser.add_subparsers(dest='mode')

engine = [
  DatasetParser(commands),
  TaskParser(commands),
]

if len(sys.argv)==1:
  print(parser.print_help())
  sys.exit(1)

args = parser.parse_args()

for e in engine:
  e.compile(args)