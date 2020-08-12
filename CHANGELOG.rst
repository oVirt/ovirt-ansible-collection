=========================
Ovirt.Ovirt Release Notes
=========================

.. contents:: Topics


v1.1.1
======

Release Summary
---------------

Small fixes

Minor Changes
-------------

- ovirt_permission - fix FQCN documentation

v1.1.0
======

Release Summary
---------------

This is second release of the collection.

Minor Changes
-------------

- ovirt inventory - add creation_time
- ovirt_disk - add backup
- ovirt_disk - add upload image warning for correct format
- ovirt_disk- upload_image_path autodetect size
- ovirt_host - add ssh_port
- ovirt_network - add support of removing vlan_tag
- ovirt_vm - fix quotas example

Bugfixes
--------

- ovirt inventory - Set plugin insecure if no cafile defined
- ovirt_disk - fix activate
- ovirt_disk - fix upload
- ovirt_disk - force wait when uploading disk
- ovirt_host_network - fix custom_properties default value
- ovirt_quota - fix vcpu_limit
- ovirt_vm - Add documentation for custom_script under sysprep
- ovirt_vm - fix cd_iso get all disks from storage domains
- ovirt_vm - fix cd_iso search by name

v1.0.0
======

Release Summary
---------------

This is first release of the collection.

Major Changes
-------------

- ovirt_cluster - add migration_encrypted option
- ovirt_datacenter - add iscsi_bonds
- ovirt_vm - add Bios Type option

Minor Changes
-------------

- ovirt - dynamic plugin improvements
- ovirt_vm - remove deprecated warning of boot params

Bugfixes
--------

- ovirt_storage_domain - fix update_check warning_low_space

New Plugins
-----------

Inventory
~~~~~~~~~

- ovirt.ovirt.ovirt - Inventory plugin for ovirt
