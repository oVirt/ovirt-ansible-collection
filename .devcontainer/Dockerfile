FROM mcr.microsoft.com/devcontainers/python:3

ARG DEBIAN_FRONTEND=noninteractive

RUN python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir \
        "nox>=2025.02.09" \
        antsibull-nox \
        "ansible-core>=2.20.0" \
        ansible-lint \
    && mkdir -p /home/vscode/.ansible/collections/ansible_collections \
    && chown -R vscode /home/vscode/.ansible

ENV ANSIBLE_COLLECTIONS_PATH=/home/vscode/.ansible/collections:/usr/share/ansible/collections
