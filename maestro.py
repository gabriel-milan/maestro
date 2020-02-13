from cmd import Cmd
from getpass import getpass
import pysftp
import os
import glob
from paramiko.ssh_exception import AuthenticationException
from time import time
import requests
from hashlib import sha256
import argparse
import shlex
from util import Color

class ZeusCLI(Cmd):

  #
  # Init
  #
  def __init__ (self):
    Cmd.__init__(self)
    self.__username = ''
    self.__password = ''
    self.__hasCredentials = False
    self.__currentTransfer = ''

  #
  # Prompt text
  #
  prompt = 'ZeusCLI -> '

  #
  # Intro message
  #
  intro = """
    __    ____  _____    ________           __
   / /   / __ \/ ___/   / ____/ /_  _______/ /____  _____
  / /   / /_/ /\__ \   / /   / / / / / ___/ __/ _ \/ ___/
 / /___/ ____/___/ /  / /___/ / /_/ (__  ) /_/  __/ /
/_____/_/    /____/   \____/_/\__,_/____/\__/\___/_/

Welcome to the LPS Cluster!

If you need anything, please contact:
- Carlos Eduardo Covas <kaducovas@gmail.com>
- Gabriel Gazola Milan <gabriel.milan@lps.ufrj.br>
- João Victor da Fonseca Pinto <jodafons@lps.ufrj.br>
- Micael Veríssimo <micaelvero@hotmail.com>

Type '?' for a list of commands
  """

  #
  # Auxiliar functions
  #
  def hashPw (self, password):
    m = sha256()
    m.update(password.encode('utf-8'))
    return m.hexdigest()

  def msg_error (self, message):
    print ("-- ERROR: {}".format(message))

  #
  # Documentation
  #
  def help_exit (self):
    print ("Exits the application")
  def help_authenticate (self):
    print ("Gets your credentials for the LPS Cluster")
  def help_copy_file (self):
    print ("Copies a file to the LPS Cluster NAS")
    print ("Usage: copy_file <filename>")

  #
  # Autocompletes
  #
  def __append_slash_if_dir (self, p):
      if p and os.path.isdir(p) and p[-1] != os.sep:
          return p + os.sep
      else:
          return p

  def complete_copy_file (self, text, line, begidx, endidx):
    before_arg = line.rfind(" ", 0, begidx)
    if before_arg == -1:
      return
    fixed = line[before_arg+1:begidx]
    arg = line[before_arg+1:endidx]
    pattern = arg + '*'
    completions = []
    for path in glob.glob(pattern):
      path = self.__append_slash_if_dir(path)
      completions.append(path.replace(fixed, "", 1))
    mline = line.partition (' ')[2]
    offs = len(mline) - len(text)
    return [s[offs:] for s in completions if s.startswith(mline)]

  #
  # Getting credentials
  #
  def do_authenticate (self, inp):
    self.__username = input(' Login: ')
    self.__password = self.hashPw(getpass(' Password: '))
    self.__hasCredentials = True
    print ("Trying to connect...")
    data = {
      'username':self.__username,
      'password':self.__password
    }
    try:
      r = requests.post(url='http://localhost:5020/login', data=data)
      print (r.text)
    except requests.exceptions.ConnectionError:
      self.msg_error ("Failed to connect to LPS Cluster.")
    print ()

  #
  # Lists all tasks
  #
  def do_list (self, inp):

    # Requesting task list for the cluster
    try:
      r = requests.get(url='http://localhost:5020/tasks')
      print (r.text)
      # # define the line template
      # line="+------------------+----------------------------------------------------------------------------------+----------+----------+----------+----------+----------+------------+"
      # print(line)
      # print ( "|     "+Color.CGREEN2+"username"+Color.CEND+
      # "     |                                     "+Color.CGREEN2+"taskname"+Color.CEND+
      # "                                     | "+Color.CGREEN2+"assigned"+Color.CEND+
      # " | "+Color.CGREEN2+"testing"+Color.CEND+
      # "  | "+Color.CGREEN2+"running"+Color.CEND+
      # "  | "+Color.CRED2+"failed"+Color.CEND+
      # "   |  "+Color.CGREEN2+"done"+Color.CEND+
      # "    | "+Color.CGREEN2+"status"+Color.CEND+"     |" )
      # print(line)
      # for task in tasks:
      #   if len(task.taskName)>80:
      #     #taskname = task.taskName[0:75]
      #     taskname = task.taskName[0:40]+' ... '+ task.taskName[-30:]
      #   else:
      #     taskname = task.taskName
      #   print ( ("| {0:<16} | {1:<80} | {2:<8} | {3:<8} | {4:<8} | {5:<8} | {6:<8} | {7:<15}"+Color.CEND+" |" ).format( task.username, taskname, task.assigned, task.testing,
      #       task.running, task.failed, task.done, getStatus(task.status)))
      # print(line)
    except:
      self.msg_error ("Failed to connect to LPS Cluster.")

    def getStatus(status):
      if status == 'registered':
        return Color.CWHITE2+"REGISTERED"
      elif status == 'assigned':
        return Color.CWHITE2+"ASSIGNED"
      elif status == 'testing':
        return Color.CGREEN2+"TESTING"
      elif status == 'running':
        return Color.CGREEN2+"RUNNING"
      elif status == 'done':
        return Color.CGREEN2+"DONE"
      elif status == 'failed':
        return Color.CRED2+"FAILED"
      elif status == 'finalized':
        return Color.CRED2+"FINALIZED"


  #
  # Create task
  #
  def do_create (self, inp):
    arg_cli = shlex.split(inp)

    parser = argparse.ArgumentParser(prog='create')
    parser.add_argument('-c','--configFile', action='store',
                    dest='configFile', required = True,
                    help = "The job config file that will be used to configure the job (sort and init).")
    parser.add_argument('-o','--outputFile', action='store',
                    dest='outputFile', required = True,
                    help = "The output tuning name.")
    parser.add_argument('-d','--dataFile', action='store',
                    dest='dataFile', required = True,
                    help = "The data/target file used to train the model.")
    parser.add_argument('--exec', action='store', dest='execCommand', required=True,
                    help = "The exec command")
    parser.add_argument('--containerImage', action='store', dest='containerImage', required=True,
                    help = "The container image that points to docker hub. The container must be public.")
    parser.add_argument('-t','--task', action='store', dest='task', required=True,
                    help = "The task name to append into the DB.")
    parser.add_argument('--sd','--secondaryData', action='store', dest='secondaryData', required=False,  default="{}",
                    help = "The secondary datasets to append in the --exec command. This should be:" +
                    "--secondaryData='{'REF':'path/to/my/extra/data',...}'")
    parser.add_argument('--gpu', action='store_true', dest='gpu', required=False, default=False,
                    help = "Send these jobs to GPU slots")
    parser.add_argument('--et', action='store', dest='et', required=False,default=None,
                    help = "The ET region (ringer staff)")
    parser.add_argument('--eta', action='store', dest='eta', required=False,default=None,
                    help = "The ETA region (ringer staff)")
    parser.add_argument('--dry_run', action='store_true', dest='dry_run', required=False, default=False,
                    help = "Use this as debugger.")
    parser.add_argument('--bypass', action='store_true', dest='bypass_test_job', required=False, default=False,
                    help = "Bypass the job test.")
    parser.add_argument('--cluster', action='store', dest='cluster', required=False, default='LPS',
                    help = "The name of your cluster (LPS/CERN/SDUMONT/LOBOC)")
    parser.add_argument('--storagePath', action='store', dest='storagePath', required=False, default='/mnt/cluster-volume',
                    help = "The path to the storage in the cluster.")

    try:
      args = parser.parse_args(arg_cli)
      data = {
        'configFile'      : args.configFile,
        'outputFile'      : args.outputFile,
        'dataFile'        : args.dataFile,
        'execCommand'     : args.execCommand,
        'containerImage'  : args.containerImage,
        'task'            : args.task,
        'secondaryData'   : args.secondaryData,
        'gpu'             : args.gpu,
        'et'              : args.et,
        'eta'             : args.eta,
        'dry_run'         : args.dry_run,
        'bypass_test_job' : args.bypass_test_job,
        'cluster'         : args.cluster,
        'storagePath'     : args.storagePath
      }

      try:
        r = requests.post(url='http://localhost:5020/create', data=data)
        print (r.text)
      except requests.exceptions.ConnectionError:
        self.msg_error ("Failed to connect to LPS Cluster.")
      print ()
    except:
      parser.print_help()

  #
  # Copying a file
  #
  def do_copy_file (self, inp):

    self.__lastTimestamp = 0
    self.__lastTransferred = 0

    def humanReadableFileSize (n_bytes):
      thresh = 1024
      if (n_bytes < thresh):
        return "{} B".format(n_bytes)
      units = ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
      u = -1
      while (n_bytes >= thresh and u < (len(units) - 1)):
        n_bytes /= thresh
        u += 1
      return  '{:.2f} {}'.format(n_bytes, units[u])

    def printTotals(transferred, toBeTransferred):
      print ("-- Copying file {}... \t {}/{}: {:.1f}% ({}/s)".format(self.__currentTransfer, humanReadableFileSize(transferred), humanReadableFileSize(toBeTransferred), (transferred/toBeTransferred) * 100, humanReadableFileSize((transferred - self.__lastTransferred) / (time() - self.__lastTimestamp))))
      self.__lastTimestamp = time()
      self.__lastTransferred = transferred

    # Checks credentials
    if (self.__hasCredentials):

      # Parsing input
      file_list = []
      if (inp.endswith("*")):
        for i in os.listdir('.'):
          if os.path.isfile(os.path.join('.', i)) and i.startswith(inp[:-1]):
            file_list.append (i)
        if (not file_list):
          self.msg_error ("File does not exist.")
      else:
        if (not os.path.exists(inp)):
          self.msg_error ("File does not exist.")
        else:
          file_list.append(inp)

      for filename in file_list:
        fin = open(filename, 'rb')
        files = {'file':fin}
        try:
          r = requests.post(url='http://localhost:5020/upload', files=files)
          print (r.text)
        except:
          print ("Failed to upload file.")
        finally:
          fin.close()

    else:
      print ("Please authenticate yourself.")

  #
  # Exiting
  #
  def do_exit (self, inp):
    print ("Bye!")
    return True

  #
  # Key handlers
  #
  def cmdloop(self, intro=None):
    print(self.intro)
    while True:
      try:
        super(ZeusCLI, self).cmdloop(intro="")
        break
      except KeyboardInterrupt:
        print("^C")

  def default(self, inp):
    if inp == 'x' or inp == 'q':
      return self.do_exit(inp)
    else:
      print('Command "{}" not found.'.format(inp))

  do_EOF = do_exit
  help_EOF = help_exit

ZeusCLI().cmdloop()
