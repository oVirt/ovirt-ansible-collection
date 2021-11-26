=========================
ovirt.ovirt Release Notes
=========================

.. contents:: Topics


v1.6.6
======

Minor Changes
-------------

- info - Rename follows to follow parameter and add alias (https://github.com/oVirt/ovirt-ansible-collection/pull/367).
- info - bump deprecate version for fetch_nested and nested_attributes (https://github.com/oVirt/ovirt-ansible-collection/pull/378).
- info - Enable follow parameter (https://github.com/oVirt/ovirt-ansible-collection/pull/355).
- manageiq - add deprecation info (https://github.com/oVirt/ovirt-ansible-collection/pull/384).
- ovirt_remove_stale_lun - Allow user to remove multiple LUNs (https://github.com/oVirt/ovirt-ansible-collection/pull/357).
- ovirt_remove_stale_lun - Retry "multipath -f" while removing the LUNs (https://github.com/oVirt/ovirt-ansible-collection/pull/382).

v1.6.5
======

Minor Changes
-------------

- repositories - Update host and engine repositories to 4.4.9 (https://github.com/oVirt/ovirt-ansible-collection/pull/363).

v1.6.4
======

Minor Changes
-------------

- repositories - add no_log to register (https://github.com/oVirt/ovirt-ansible-collection/pull/350).

v1.6.3
======

Minor Changes
-------------

- gluster_heal_info - Replacing gluster module to CLI to support RHV automation hub (https://github.com/oVirt/ovirt-ansible-collection/pull/340).
- repositories - Replace redhat_subscription and rhsm_repository with command (https://github.com/oVirt/ovirt-ansible-collection/pull/346).

Bugfixes
--------

- image_template - Remove static no - unsupported in ansible 2.12 (https://github.com/oVirt/ovirt-ansible-collection/pull/341).

v1.6.2
======

Minor Changes
-------------

- remove_stale_lun - Fix example for `remote_stale_lun` role to be able to run it from engine (https://github.com/oVirt/ovirt-ansible-collection/pull/334).

v1.6.1
======

Bugfixes
--------

- hosted_engine_setup - Use default bridge for IPv6 advertisements (https://github.com/oVirt/ovirt-ansible-collection/pull/331)
- ovirt_auth - Fix token no_log (https://github.com/oVirt/ovirt-ansible-collection/pull/332).

v1.5.5
======

Major Changes
-------------

- remove_stale_lun - Add role for removing stale LUN (https://bugzilla.redhat.com/1966873).

Minor Changes
-------------

- engine_setup - Wait for webserver up after engine-config reboot (https://github.com/oVirt/ovirt-ansible-collection/pull/324).
- hosted_engine_setup - Pause deployment on failure of `engine-backup --mode=restore` (https://github.com/oVirt/ovirt-ansible-collection/pull/327).
- hosted_engine_setup - Text change - Consistently use 'bootstrap engine VM' (https://github.com/oVirt/ovirt-ansible-collection/pull/328).
- hosted_engine_setup - Update Ansible requirements in README (https://github.com/oVirt/ovirt-ansible-collection/pull/321)
- readme - Update Ansible requirement (https://github.com/oVirt/ovirt-ansible-collection/pull/326).

Bugfixes
--------

- ovirt_auth - Fix password and username requirements (https://github.com/oVirt/ovirt-ansible-collection/pull/325).
- ovirt_disk - Fix update_check with no VM (https://github.com/oVirt/ovirt-ansible-collection/pull/323).

v1.5.4
======

Minor Changes
-------------

- hosted_engine_setup - Allow FIPS on HE VM (https://github.com/oVirt/ovirt-ansible-collection/pull/313)

Bugfixes
--------

- hosted_engine_setup - Use forward network during an IPv6 deployment (https://github.com/oVirt/ovirt-ansible-collection/pull/315)
- hosted_engine_setup - remove duplicate tasks (https://github.com/oVirt/ovirt-ansible-collection/pull/314)
- ovirt_permission - fix group search that has space in it's name (https://github.com/oVirt/ovirt-ansible-collection/pull/318)

v1.5.3
======

Minor Changes
-------------

- Don't rely on safe_eval being able to do math/concat (https://github.com/oVirt/ovirt-ansible-collection/pull/307)
- hosted_engine_setup - Fix engine vm add_host for the target machine (https://github.com/oVirt/ovirt-ansible-collection/pull/311)
- hosted_engine_setup - Minor doc update (https://github.com/oVirt/ovirt-ansible-collection/pull/310)

v1.5.2
======

Minor Changes
-------------

- hosted_engine_setup - Do not try to sync at end of full_execution (https://github.com/oVirt/ovirt-ansible-collection/pull/305)
- ovirt_vm - Add default return value to check_placement_policy (https://github.com/oVirt/ovirt-ansible-collection/pull/301).

v1.5.1
======

Minor Changes
-------------

- hosted_engine_setup - use-ansible-host (https://github.com/oVirt/ovirt-ansible-collection/pull/277).
- infra role - Add external_provider parameter on networks role of infra role (https://github.com/oVirt/ovirt-ansible-collection/pull/297)
- ovirt_vm - Add placement_policy_hosts (https://github.com/oVirt/ovirt-ansible-collection/pull/294).

Bugfixes
--------

- hosted_engine_setup - Filter VLAN devices with bad names (https://github.com/oVirt/ovirt-ansible-collection/pull/238)
- hosted_engine_setup - Remove cloud-init configuration (https://github.com/oVirt/ovirt-ansible-collection/pull/295).
- ovirt inventory plugin - allow several valid values for the `plugin` key (https://github.com/oVirt/ovirt-ansible-collection/pull/293).

v1.5.0
======

Minor Changes
-------------

- disaster_recovery - Change conf paths (https://github.com/oVirt/ovirt-ansible-collection/pull/286).
- hosted_engine_setup - Add-pause-option-before-engine-setup (https://github.com/oVirt/ovirt-ansible-collection/pull/273).
- hosted_engine_setup - Remove leftover code and omit parameters (https://github.com/oVirt/ovirt-ansible-collection/pull/281).
- infra - Storage fix parameters typo (https://github.com/oVirt/ovirt-ansible-collection/pull/282).
- ovirt_host - Update iscsi target struct (https://github.com/oVirt/ovirt-ansible-collection/pull/274).

Bugfixes
--------

- hosted_engine_setup - Use ovirt_host module to discover iscsi (https://github.com/oVirt/ovirt-ansible-collection/pull/275).
- hosted_engine_setup - align with ansible-lint 5.0.0 (https://github.com/oVirt/ovirt-ansible-collection/pull/271).

v1.4.2
======

Minor Changes
-------------

- hosted_engine_setup - Add an error message for FIPS on CentOS (https://github.com/oVirt/ovirt-ansible-collection/pull/250).
- hosted_engine_setup - Fix the appliance distribution (https://github.com/oVirt/ovirt-ansible-collection/pull/249).
- infra - remove target from ovirt_storage_connection (https://github.com/oVirt/ovirt-ansible-collection/pull/252).
- ovirt_vm - Allow migration between clusters (https://github.com/oVirt/ovirt-ansible-collection/pull/236).
- repositories - Add host ppc (https://github.com/oVirt/ovirt-ansible-collection/pull/248).
- repositories - Remove ansible channels from RHV 4.4 (https://github.com/oVirt/ovirt-ansible-collection/pull/242).
- repositories - fix ppc repos (https://github.com/oVirt/ovirt-ansible-collection/pull/254).

v1.4.1
======

Bugfixes
--------

- hosted_engine_setup - Fix auth revoke (https://github.com/oVirt/ovirt-ansible-collection/pull/237).

v1.4.0
======

Minor Changes
-------------

- cluster_upgrade - Add correlation-id header (https://github.com/oVirt/ovirt-ansible-collection/pull/222).
- engine_setup - Add skip renew pki confirm (https://github.com/oVirt/ovirt-ansible-collection/pull/228).
- examples - Add recipe for removing DM device (https://github.com/oVirt/ovirt-ansible-collection/pull/233).
- hosted_engine_setup - Filter devices with unsupported bond mode (https://github.com/oVirt/ovirt-ansible-collection/pull/226).
- infra - Add reboot host parameters (https://github.com/oVirt/ovirt-ansible-collection/pull/231).
- ovirt_disk - Add SATA support (https://github.com/oVirt/ovirt-ansible-collection/pull/225).
- ovirt_user - Add ssh_public_key (https://github.com/oVirt/ovirt-ansible-collection/pull/232)

Bugfixes
--------

- Set ``auth`` options into argument spec definition so Ansible will validate the user options
- Set ``no_log`` on ``password`` and ``token`` in the ``auth`` dict so the values are exposed in the invocation log

v1.3.1
======

Minor Changes
-------------

- hosted_engine_setup - Disable reboot_after_installation (https://github.com/oVirt/ovirt-ansible-collection/pull/218).
- ovirt_host - Add reboot_after_installation option (https://github.com/oVirt/ovirt-ansible-collection/pull/217).

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
