#!/usr/bin/env bash
set -e

cd census-rh-ui-source

# Install libssl-dev for python cryptography lib
apt-get install libssl-dev -y
apt-get install python3-dev -y
pip install --upgrade pip==18.0
pipenv run pip install --upgrade pip==18.0
pipenv install --dev
pipenv run inv smoke
