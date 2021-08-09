oVirt Remove Stale LUN
=========

The `remove_stale_lun` role iterates through all the hosts in a data center and remove stale LUN devices from these hosts.
If the playbook is not executed on the engine, user ssh key has to be added on all hosts which belongs to the given data center.

Role Variables
--------------

| Name                    | Default value         |                                                     |
|-------------------------|-----------------------|-----------------------------------------------------|
| data_center             | Default               | Name of the data center from which hosts stale LUN should be removed. |
| lun_wwid                | UNDEF                 | WWID of the stale LUN which should be removed from the hosts. |


Example Playbook
----------------

```yaml
---
- name: oVirt remove stale LUN
  hosts: localhost
  connection: local
  gather_facts: false

  vars_files:
    # Contains encrypted `engine_password` varibale using ansible-vault
    - passwords.yml

  vars:
    engine_fqdn: ovirt.example.com
    engine_user: admin@internal

    data_center: default
    lun_wwid: 36001405a77a1ee25cbf4439b7ddd2062

  roles:
    - remove_stale_lun
  collections:
    - @NAMESPACE@.@NAME@
```
