from cmd import Cmd
from getpass import getpass
import pysftp
import os
import glob
from paramiko.ssh_exception import AuthenticationException
from time import time
 
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
    self.__password = getpass(' Password: ')
    self.__hasCredentials = True
    print ("Credentials saved!")
    print ()

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
          print ("-- ERROR: File does not exist.")
      else:
        if (not os.path.exists(inp)):
          print ("-- ERROR: File does not exist.")
        else:
          file_list.append(inp)
      
      # Copies
      try:
        with pysftp.Connection ('146.164.147.170', username=self.__username, password=self.__password) as sftp:
          with sftp.cd('/mnt/cluster-volume/{}'.format(self.__username)):
            for filename in file_list:
              self.__currentTransfer = filename
              print ("-- Copying file {}... \t".format(filename), end='')
              sftp.put(filename, callback=printTotals)
      except AuthenticationException:
        print ("-- ERROR: Authentication failed.")

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
