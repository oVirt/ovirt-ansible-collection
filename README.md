[![Build Status](https://jenkins.ovirt.org/job/oVirt_ovirt-ansible-collection_standard-check-pr/badge/icon)](https://jenkins.ovirt.org/job/oVirt_ovirt-ansible-collection_standard-check-pr/)
[![Build Status](https://img.shields.io/badge/docs-latest-blue.svg)](https://docs.ansible.com/ansible/2.10/collections/ovirt/ovirt/index.html)

oVirt ansible collection
====================================

The `ovirt.ovirt` manages all ansible modules of oVirt.

The pypi installation is no longer supported if you want
to install all dependencies do it manually or install the
collection from RPM and it will be done automatically.

Note
----
Please note that when installing this collection from Ansible Galaxy you are instructed to run following command:

```bash
$ ansible-galaxy collection install ovirt.ovirt
```

Requirements
------------

 * Ansible version 2.9.11 or higher
 * Python SDK version 4.4 or higher
 * Python netaddr library on the ansible controller node

Modules documentation
--------------
https://docs.ansible.com/ansible/2.10/collections/ovirt/ovirt/index.html

Example Playbook
----------------

```yaml
---
- name: oVirt ansible collection
  hosts: localhost
  connection: local
  vars_files:
    # Contains encrypted `engine_password` varibale using ansible-vault
    - passwords.yml
  tasks:
    - block:
        # The use of ovirt.ovirt before ovirt_auth is to check if the collection is correctly loaded
        - name: Obtain SSO token with using username/password credentials
          ovirt.ovirt.ovirt_auth:
            url: https://ovirt.example.com/ovirt-engine/api
            username: admin@internal
            ca_file: ca.pem
            password: "{{ ovirt_password }}"

        # Previous task generated I(ovirt_auth) fact, which you can later use
        # in different modules as follows:
        - ovirt_vm:
            auth: "{{ ovirt_auth }}"
            state: absent
            name: myvm

      always:
        - name: Always revoke the SSO token
          ovirt_auth:
            state: absent
            ovirt_auth: "{{ ovirt_auth }}"
  collections:
    - ovirt.ovirt
```

Licenses
-------

- Apache License 2.0
- GNU General Public License 3.0
