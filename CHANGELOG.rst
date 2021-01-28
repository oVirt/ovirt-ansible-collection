=========================
ovirt.ovirt Release Notes
=========================

.. contents:: Topics


v1.3.0
======

Major Changes
-------------

- ovirt_system_option_info - Add new module (https://github.com/oVirt/ovirt-ansible-collection/pull/206).

Minor Changes
-------------

- ansible-builder - Update bindep (https://github.com/oVirt/ovirt-ansible-collection/pull/197).
- hosted_engine_setup - Collect all engine /var/log (https://github.com/oVirt/ovirt-ansible-collection/pull/202).
- hosted_engine_setup - Use ovirt_system_option_info instead of REST API (https://github.com/oVirt/ovirt-ansible-collection/pull/209).
- ovirt_disk - Add install warning (https://github.com/oVirt/ovirt-ansible-collection/pull/208).
- ovirt_info - Fragment add auth suboptions to documentation (https://github.com/oVirt/ovirt-ansible-collection/pull/205).

v1.2.4
======

Minor Changes
-------------

- infra - don't require passowrd for user (https://github.com/oVirt/ovirt-ansible-collection/pull/195).
- inventory - correct os_type name (https://github.com/oVirt/ovirt-ansible-collection/pull/194).
- ovirt_disk - automatically detect virtual size of qcow image (https://github.com/oVirt/ovirt-ansible-collection/pull/183).

v1.2.3
======

Minor Changes
-------------

- engine_setup - Add missing restore task file and vars file (https://github.com/oVirt/ovirt-ansible-collection/pull/180).
- hosted_engine_setup - Add after_add_host hook (https://github.com/oVirt/ovirt-ansible-collection/pull/181).

v1.2.2
======

Bugfixes
--------

- hosted_engine_setup - Clean VNC encryption config (https://github.com/oVirt/ovirt-ansible-collection/pull/175/).
- inventory plugin - Fix timestamp for Python 2 (https://github.com/oVirt/ovirt-ansible-collection/pull/173).

v1.2.1
======

Bugfixes
--------

- disaster_recovery - Fix multiple configuration issues like paths, "~" support, user input messages, etc. (https://github.com/oVirt/ovirt-ansible-collection/pull/160).

v1.2.0
======

Major Changes
-------------

- cluster_upgrade - Migrate role (https://github.com/oVirt/ovirt-ansible-collection/pull/94).
- disaster_recovery - Migrate role (https://github.com/oVirt/ovirt-ansible-collection/pull/134).
- engine_setup - Migrate role (https://github.com/oVirt/ovirt-ansible-collection/pull/69).
- hosted_engine_setup - Migrate role (https://github.com/oVirt/ovirt-ansible-collection/pull/106).
- image_template - Migrate role (https://github.com/oVirt/ovirt-ansible-collection/pull/95).
- infra - Migrate role (https://github.com/oVirt/ovirt-ansible-collection/pull/92).
- manageiq - Migrate role (https://github.com/oVirt/ovirt-ansible-collection/pull/97).
- repositories - Migrate role (https://github.com/oVirt/ovirt-ansible-collection/pull/96).
- shutdown_env - Migrate role (https://github.com/oVirt/ovirt-ansible-collection/pull/112).
- vm_infra - Migrate role (https://github.com/oVirt/ovirt-ansible-collection/pull/93).

Minor Changes
-------------

- Add GPL license (https://github.com/oVirt/ovirt-ansible-collection/pull/101).
- hosted_engine_setup - Add compatibility_version (https://github.com/oVirt/ovirt-ansible-collection/pull/125).
- ovirt_disk - ignore move of HE disks (https://github.com/oVirt/ovirt-ansible-collection/pull/162).
- ovirt_nic - Add template_version (https://github.com/oVirt/ovirt-ansible-collection/pull/145).
- ovirt_nic_info - Add template (https://github.com/oVirt/ovirt-ansible-collection/pull/146).
- ovirt_vm_info - Add current_cd (https://github.com/oVirt/ovirt-ansible-collection/pull/144).

Bugfixes
--------

- 01_create_target_hosted_engine_vm - Force basic authentication (https://github.com/oVirt/ovirt-ansible-collection/pull/131).
- hosted_engine_setup - Allow uppercase characters in mac address (https://github.com/oVirt/ovirt-ansible-collection/pull/150).
- hosted_engine_setup - set custom bios type of hosted-engine VM to Q35+SeaBIOS (https://github.com/oVirt/ovirt-ansible-collection/pull/129).
- hosted_engine_setup - use zcat instead of gzip (https://github.com/oVirt/ovirt-ansible-collection/pull/130).
- ovirt inventory - Add close of connection at the end (https://github.com/oVirt/ovirt-ansible-collection/pull/122).
- ovirt_disk - dont move disk when already in storage_domain (https://github.com/oVirt/ovirt-ansible-collection/pull/135)
- ovirt_disk - fix upload when direct upload fails (https://github.com/oVirt/ovirt-ansible-collection/pull/120).
- ovirt_vm - Fix template search (https://github.com/oVirt/ovirt-ansible-collection/pull/132).
- ovirt_vm - Rename q35_sea to q35_sea_bios (https://github.com/oVirt/ovirt-ansible-collection/pull/111).

v1.1.2
======

v1.1.1
======

Minor Changes
-------------

- ovirt_permission - Fix FQCN documentation (https://github.com/oVirt/ovirt-ansible-collection/pull/63).

v1.1.0
======

Major Changes
-------------

- ovirt_disk - Add backup (https://github.com/oVirt/ovirt-ansible-collection/pull/57).
- ovirt_disk - Support direct upload/download (https://github.com/oVirt/ovirt-ansible-collection/pull/35).
- ovirt_host - Add ssh_port (https://github.com/oVirt/ovirt-ansible-collection/pull/60).
- ovirt_vm_os_info - Creation of module (https://github.com/oVirt/ovirt-ansible-collection/pull/26).

Minor Changes
-------------

- ovirt inventory - Add creation_time (https://github.com/oVirt/ovirt-ansible-collection/pull/34).
- ovirt inventory - Set inventory plugin insecure if no cafile defined (https://github.com/oVirt/ovirt-ansible-collection/pull/58).
- ovirt_disk - Add upload image warning for correct format (https://github.com/oVirt/ovirt-ansible-collection/pull/22).
- ovirt_disk - Force wait when uploading disk (https://github.com/oVirt/ovirt-ansible-collection/pull/43).
- ovirt_disk - Upload_image_path autodetect size (https://github.com/oVirt/ovirt-ansible-collection/pull/19).
- ovirt_network - Add support of removing vlan_tag (https://github.com/oVirt/ovirt-ansible-collection/pull/21).
- ovirt_vm - Add documentation for custom_script under sysprep (https://github.com/oVirt/ovirt-ansible-collection/pull/52).
- ovirt_vm - Hard code nic on_boot to true (https://github.com/oVirt/ovirt-ansible-collection/pull/45).

Bugfixes
--------

- ovirt_disk - Fix activate (https://github.com/oVirt/ovirt-ansible-collection/pull/61).
- ovirt_host_network - Fix custom_properties default value (https://github.com/oVirt/ovirt-ansible-collection/pull/65).
- ovirt_quota - Fix vcpu_limit (https://github.com/oVirt/ovirt-ansible-collection/pull/44).
- ovirt_vm - Fix cd_iso get all disks from storage domains (https://github.com/oVirt/ovirt-ansible-collection/pull/66).
- ovirt_vm - Fix cd_iso search by name (https://github.com/oVirt/ovirt-ansible-collection/pull/51).

New Modules
-----------

- ovirt.ovirt.ovirt_vm_os_info - Retrieve information on all supported oVirt/RHV operating systems

v1.0.0
======

Minor Changes
-------------

- ovirt_cluster - Add migration_encrypted option (https://github.com/oVirt/ovirt-ansible-collection/pull/17).
- ovirt_vm - Add bios_type (https://github.com/oVirt/ovirt-ansible-collection/pull/15).

Bugfixes
--------

- ovirt_snapshot - Disk id was incorrectly set as disk_snapshot_id (https://github.com/oVirt/ovirt-ansible-collection/pull/5).
- ovirt_storage_domain - Fix update_check warning_low_space (https://github.com/oVirt/ovirt-ansible-collection/pull/10).
- ovirt_vm - Remove deprecated warning of boot params (https://github.com/oVirt/ovirt-ansible-collection/pull/3).

New Plugins
-----------

Inventory
~~~~~~~~~

- ovirt.ovirt.ovirt - oVirt inventory source

New Modules
-----------

- ovirt.ovirt.ovirt_affinity_group - Module to manage affinity groups in oVirt/RHV
- ovirt.ovirt.ovirt_affinity_label - Module to manage affinity labels in oVirt/RHV
- ovirt.ovirt.ovirt_affinity_label_info - Retrieve information about one or more oVirt/RHV affinity labels
- ovirt.ovirt.ovirt_api_info - Retrieve information about the oVirt/RHV API
- ovirt.ovirt.ovirt_auth - Module to manage authentication to oVirt/RHV
- ovirt.ovirt.ovirt_cluster - Module to manage clusters in oVirt/RHV
- ovirt.ovirt.ovirt_cluster_info - Retrieve information about one or more oVirt/RHV clusters
- ovirt.ovirt.ovirt_datacenter - Module to manage data centers in oVirt/RHV
- ovirt.ovirt.ovirt_datacenter_info - Retrieve information about one or more oVirt/RHV datacenters
- ovirt.ovirt.ovirt_disk - Module to manage Virtual Machine and floating disks in oVirt/RHV
- ovirt.ovirt.ovirt_disk_info - Retrieve information about one or more oVirt/RHV disks
- ovirt.ovirt.ovirt_event - Create or delete an event in oVirt/RHV
- ovirt.ovirt.ovirt_event_info - This module can be used to retrieve information about one or more oVirt/RHV events
- ovirt.ovirt.ovirt_external_provider - Module to manage external providers in oVirt/RHV
- ovirt.ovirt.ovirt_external_provider_info - Retrieve information about one or more oVirt/RHV external providers
- ovirt.ovirt.ovirt_group - Module to manage groups in oVirt/RHV
- ovirt.ovirt.ovirt_group_info - Retrieve information about one or more oVirt/RHV groups
- ovirt.ovirt.ovirt_host - Module to manage hosts in oVirt/RHV
- ovirt.ovirt.ovirt_host_info - Retrieve information about one or more oVirt/RHV hosts
- ovirt.ovirt.ovirt_host_network - Module to manage host networks in oVirt/RHV
- ovirt.ovirt.ovirt_host_pm - Module to manage power management of hosts in oVirt/RHV
- ovirt.ovirt.ovirt_host_storage_info - Retrieve information about one or more oVirt/RHV HostStorages (applicable only for block storage)
- ovirt.ovirt.ovirt_instance_type - Module to manage Instance Types in oVirt/RHV
- ovirt.ovirt.ovirt_job - Module to manage jobs in oVirt/RHV
- ovirt.ovirt.ovirt_mac_pool - Module to manage MAC pools in oVirt/RHV
- ovirt.ovirt.ovirt_network - Module to manage logical networks in oVirt/RHV
- ovirt.ovirt.ovirt_network_info - Retrieve information about one or more oVirt/RHV networks
- ovirt.ovirt.ovirt_nic - Module to manage network interfaces of Virtual Machines in oVirt/RHV
- ovirt.ovirt.ovirt_nic_info - Retrieve information about one or more oVirt/RHV virtual machine network interfaces
- ovirt.ovirt.ovirt_permission - Module to manage permissions of users/groups in oVirt/RHV
- ovirt.ovirt.ovirt_permission_info - Retrieve information about one or more oVirt/RHV permissions
- ovirt.ovirt.ovirt_quota - Module to manage datacenter quotas in oVirt/RHV
- ovirt.ovirt.ovirt_quota_info - Retrieve information about one or more oVirt/RHV quotas
- ovirt.ovirt.ovirt_role - Module to manage roles in oVirt/RHV
- ovirt.ovirt.ovirt_scheduling_policy_info - Retrieve information about one or more oVirt scheduling policies
- ovirt.ovirt.ovirt_snapshot - Module to manage Virtual Machine Snapshots in oVirt/RHV
- ovirt.ovirt.ovirt_snapshot_info - Retrieve information about one or more oVirt/RHV virtual machine snapshots
- ovirt.ovirt.ovirt_storage_connection - Module to manage storage connections in oVirt
- ovirt.ovirt.ovirt_storage_domain - Module to manage storage domains in oVirt/RHV
- ovirt.ovirt.ovirt_storage_domain_info - Retrieve information about one or more oVirt/RHV storage domains
- ovirt.ovirt.ovirt_storage_template_info - Retrieve information about one or more oVirt/RHV templates relate to a storage domain.
- ovirt.ovirt.ovirt_storage_vm_info - Retrieve information about one or more oVirt/RHV virtual machines relate to a storage domain.
- ovirt.ovirt.ovirt_tag - Module to manage tags in oVirt/RHV
- ovirt.ovirt.ovirt_tag_info - Retrieve information about one or more oVirt/RHV tags
- ovirt.ovirt.ovirt_template - Module to manage virtual machine templates in oVirt/RHV
- ovirt.ovirt.ovirt_template_info - Retrieve information about one or more oVirt/RHV templates
- ovirt.ovirt.ovirt_user - Module to manage users in oVirt/RHV
- ovirt.ovirt.ovirt_user_info - Retrieve information about one or more oVirt/RHV users
- ovirt.ovirt.ovirt_vm - Module to manage Virtual Machines in oVirt/RHV
- ovirt.ovirt.ovirt_vm_info - Retrieve information about one or more oVirt/RHV virtual machines
- ovirt.ovirt.ovirt_vmpool - Module to manage VM pools in oVirt/RHV
- ovirt.ovirt.ovirt_vmpool_info - Retrieve information about one or more oVirt/RHV vmpools
- ovirt.ovirt.ovirt_vnic_profile - Module to manage vNIC profile of network in oVirt/RHV
- ovirt.ovirt.ovirt_vnic_profile_info - Retrieve information about one or more oVirt/RHV vnic profiles
