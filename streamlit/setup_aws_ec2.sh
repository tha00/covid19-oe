#!/usr/bin/env bash

sudo apt-get update

# Install miniconda
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p ~/miniconda

# Update PATH
PATH=$PATH:$HOME/miniconda/bin
export PATH

# Install dependencies
cd "$(dirname "$0")" || exit
pip install -r requirements.txt

# Persist PATH
echo "$PATH" >> ~/.bashrc
