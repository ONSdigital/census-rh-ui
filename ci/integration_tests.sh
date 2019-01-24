#!/usr/bin/env bash
set -e

cd census-rh-ui-source

# Install libssl-dev for python cryptography lib
apt-get install libssl-dev -y
pipenv install --dev
pipenv run inv integration --live
