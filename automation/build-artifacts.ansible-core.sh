#!/bin/bash -xe

# Install ansible-core from pypi
pip3 install -U pip
pip3 install ansible-core

export ANSIBLE_EXEC_PREFIX="/usr/local/bin"

./automation/build.sh
