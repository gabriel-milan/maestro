from setuptools import setup, find_packages
from setuptools.extension import Extension
import subprocess
import sys

def install(package):
  subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
  from Cython.Build import cythonize
except:
  install('cython')
  from Cython.Build import cythonize

with open("README.md", "r") as fh:
  long_description = fh.read()

extensions = [
  Extension(
    "lps_maestro.*",
    ["lps_maestro/*.py"],
  )
]

setup(
  name = 'lps-maestro',
  version = '0.4.1',
  license='GPL-3.0',
  description = 'Command line interface for the LPS Cluster @ UFRJ.',
  long_description = long_description,
  long_description_content_type="text/markdown",
  packages=['lps_maestro'],
  author = 'Gabriel Gazola Milan',
  author_email = 'gabriel.gazola@poli.ufrj.br',
  url = 'https://github.com/gabriel-milan/maestro',
  keywords = ['cli', 'cluster', 'command-line interface', 'computer grid', 'lps', 'ufrj'],
  install_requires=[
    'requests'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
  ext_modules = cythonize(extensions)
)
