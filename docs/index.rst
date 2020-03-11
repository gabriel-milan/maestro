=======
Maestro
=======

Maestro is the command-line interface for the computer grid at the
Signal Processing Laboratory @ Federal University of Rio de
Janeiro (LPS/UFRJ).

It allows you to manage datasets and tasks, providing everything you
need for best usage of the Orchestra Cluster, that aggregates multiple
computer grids in one, increasing your own productivity.

Installation
------------

Install Maestro by running:

- Clone the Maestro repository

   `git clone https://github.com/gabriel-milan/maestro`

- Go to the cloned directory:

   `cd maestro`

- Run the setup script:

   `source setup.sh`

- Done! You can test your installation by running:

   `maestro --help`

Getting started
---------------

**Disclaimer 1:** for using Maestro CLI, you'll need credentials on the Orchestra Cluster. If you don't have it,
please contact us. More information on contact on section Support_.

**Disclaimer 2:** Internet access is mandatory.

Maestro has three main modules:

- `authenticate` for generating your authentication token that will be stored at `$HOME/.maestro_credentials`
- `castor` for managing datasets (uploading, downloading, deleting and listing)
- `task` for managing workload tasks (creating, retrying, deleting, listing and killing)


maestro authenticate
~~~~~~~~~~~~~~~~~~~~

This is the simplest module on Maestro and it's necessary so you can access the other two. By running:

   `maestro authenticate --user <username> --password <password>`

or

   `maestro authenticate -u <username> -p <password>`

you will attempt to authenticate with the Orchestra API and, if succeeded, a token will be
generated and stored at `$HOME/.maestro_credentials`. After this, you'll no longer need to worry
about authentication, if your credentials file remains untouched.

If you've changed passwords or wish to authenticate with another account, just run this command
again and your credentials will be overwritten.


maestro castor
~~~~~~~~~~~~~~

Castor module has four commands:

- `upload` for uploading new datasets
- `download` for downloading datasets from the Orchestra Cluster
- `delete` for deleting datasets on the Orchestra Cluster
- `list` for listing datasets related to a given username

maestro castor upload
"""""""""""""""""""""

.. code-block:: bash

   usage: maestro upload [-h] -d DATASETNAME -p PATH

   optional arguments:
   -h, --help                                show this help message and exit

   -d DATASETNAME, --dataset DATASETNAME     The dataset name that will be registered on the
                                             database (e.g: user.jodafons...)

   -p PATH, --path PATH                      The path to the dataset file

maestro castor download
"""""""""""""""""""""""

.. code-block:: bash

   usage: maestro download [-h] -d DATASETNAME

   optional arguments:
   -h, --help                                show this help message and exit

   -d DATASETNAME, --dataset DATASETNAME     The dataset name to be downloaded

maestro castor delete
"""""""""""""""""""""

.. code-block:: bash

   usage: maestro delete [-h] -d DATASETNAME

   optional arguments:
   -h, --help                                show this help message and exit

   -d DATASETNAME, --dataset DATASETNAME     The dataset name to be removed

maestro castor list
"""""""""""""""""""

.. code-block:: bash

   usage: maestro list [-h] -u USERNAME

   optional arguments:
   -h, --help                                show this help message and exit

   -u USERNAME, --user USERNAME              List all datasets for a selected user


maestro task
~~~~~~~~~~~~

Task module has five commands:

- `create` for deploying workload
- `retry` for retrying tasks that either failed or got killed
- `delete` for deleting tasks on the Orchestra Cluster
- `list` for listing tasks related to a given username
- `kill` for stopping execution of tasks

maestro task create
"""""""""""""""""""

.. code-block:: bash

   usage: maestro create [-h] -c CONFIGFILE -d DATAFILE --exec EXECCOMMAND
                        --containerImage CONTAINERIMAGE -t TASKNAME
                        [--sd SECONDARYDS] [--gpu] [--et ET] [--eta ETA]
                        [--dry_run]

   optional arguments:
   -h, --help                                      show this help message and exit

   -c CONFIGFILE, --configFile CONFIGFILE          The job config file that will be used to configure the
                                                   job (sort and init).

   -d DATAFILE, --dataFile DATAFILE                The data/target file used to train the model.

   --exec EXECCOMMAND                              The exec command

   --containerImage CONTAINERIMAGE                 The container image point to docker hub. The image
                                                   must be public.

   -t TASKNAME, --task TASKNAME                    The task name to append in the database.

   --sd SECONDARYDS, --secondaryDS SECONDARYDS     The secondary datasets to append in the --exec
                                                   command. This should be:--secondaryData='{'REF':'path/
                                                   to/my/extra/data',...}'

   --gpu                                           Send these jobs to GPU slots

   --et ET                                         The ET region (for ringer users)
   
   --eta ETA                                       The ETA region (for ringer users)
   
   --dry_run                                       For debugging purposes.

maestro task retry
""""""""""""""""""

.. code-block:: bash

   usage: maestro retry [-h] -t TASKNAME

   optional arguments:
   -h, --help                                      show this help message and exit
   
   -t TASKNAME, --task TASKNAME                    The name of the task you want to retry

maestro task delete
"""""""""""""""""""

.. code-block:: bash

   usage: maestro delete [-h] -t TASKNAME

   optional arguments:
   -h, --help                                      show this help message and exit

   -t TASKNAME, --task TASKNAME                    The name of the task you want to remove

maestro task list
"""""""""""""""""

.. code-block:: bash

   usage: maestro list [-h] -u USERNAME

   optional arguments:
   -h, --help                                      show this help message and exit
   -u USERNAME, --user USERNAME                    The username

maestro task kill
"""""""""""""""""

.. code-block:: bash

   usage: maestro kill [-h] -u USERNAME [-t TASKNAME] [-a]

   optional arguments:
   -h, --help                                      show this help message and exit

   -u USERNAME, --user USERNAME                    The username.

   -t TASKNAME, --task TASKNAME                    The name of the task you want to kill

   -a, --all                                       Remove all tasks from given username

Contribute
----------

- Issue Tracker: https://github.com/gabriel-milan/maestro/issues
- Source Code: https://github.com/gabriel-milan/maestro

.. _ShortAnchor:

Support
-------

If you have any issues, please contact us (brazilian portuguese or english):

- Gabriel Gazola Milan <gabriel.milan@lps.ufrj.br>
- João Victor da Fonseca Pinto <jodafons@lps.ufrj.br>

License
-------

The project is licensed under the `GNU GPL v3.0 License <https://github.com/gabriel-milan/maestro/blob/master/LICENSE>`_.