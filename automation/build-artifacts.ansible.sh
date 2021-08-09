#!/bin/bash -xe

dnf install ansible ansible-test

export ANSIBLE_EXEC_PREFIX="/usr/bin"

./automation/build.sh
