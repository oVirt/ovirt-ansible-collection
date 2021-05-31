#!/bin/bash -xe

dnf install ansible ansible-test

export ANSIBLE_EXEC_PREFIX="/bin"

./automation/build.sh
