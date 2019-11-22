#!/bin/bash

# Macros
BIN_DIR="$HOME/.bin"
SCRIPT_NAME="$BIN_DIR/zeus_cli"
HEADER="#!"$(which python3)

echo "Setting up the script..."

if [ ! -d $BIN_DIR ]
then
  mkdir $BIN_DIR
fi

cp main.py $SCRIPT_NAME

if [[ ":$PATH:" != *":$HOME/.bin:"* ]]
then
  echo "export PATH=$PATH:$HOME/.bin" >> $HOME/.bashrc
  echo "export PATH=$PATH:$HOME/.bin" >> $HOME/.bash_profile
  source $HOME/.bashrc
fi

echo $HEADER | cat - $SCRIPT_NAME > temp && mv temp $SCRIPT_NAME
chmod a+x $SCRIPT_NAME

echo "All done! Run it by typing 'zeus_cli'"