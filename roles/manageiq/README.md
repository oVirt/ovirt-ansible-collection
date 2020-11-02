Deploy ManageIQ in oVirt
==================================================

The `manageiq` role downloads a ManageIQ/CloudForms QCOW image and deploys it into oVirt/Red Hat Virtualization (RHV).

The role also enables you to create a virtual machine and attach the ManageIQ disk, then wait for the ManageIQ system to initialize, and register oVirt as an infrastructure provider.

Requirements
------------

* [ovirt-imageio](http://www.ovirt.org/develop/release-management/features/storage/image-upload/) must be installed and running.

Additionally, perform the following checks to ensure the required processes are running.
* Check whether `ovirt-imageio-proxy` is running on the engine:

 ```
systemctl status ovirt-imageio-proxy
```

* Check whether `ovirt-imageio-daemon` is running on the hosts:

 ```
systemctl status ovirt-imageio-daemon
```

You will also require the CA certificate of the engine. To do this, configure the `ovirt_ca` variable with the path to the CA certificate.

Limitations
-----------

 * We don not support Ansible Check Mode (Dry Run), because this role is using few modules(command module),
   which do not support it. Once all modules used by this role will support it, we will support it.

Role Variables
--------------

QCOW variables:

| Name          | Default value                                            |  Description                                                 |
|---------------|----------------------------------------------------------|--------------------------------------------------------------|
| miq_qcow_url  | http://releases.manageiq.org/manageiq-ovirt-hammer-6.qc2 | The URL of the ManageIQ QCOW image. |
| miq_image_path | /tmp/ | Path where the QCOW2 image will be downloaded to. If directory the base name of the URL on the remote server will be used. |
| miq_image_checksum | UNDEF | If a checksum is defined, the digest of the destination file will be calculated after it is downloaded to ensure its integrity and verify that the transfer completed successfully. Format: :, e.g. checksum="sha256:D98291AC[...]B6DC7B97". |

Engine login variables:

| Name                | Default value     |  Description                            |
|---------------------|-------------------|-----------------------------------------|
| engine_user         | UNDEF             | The user to access the engine.          |
| engine_password     | UNDEF             | The password of the 'engine_user'.      |
| engine_fqdn         | UNDEF             | The FQDN of the engine.                 |
| engine_ca           | UNDEF             | The path to the engine's CA certificate.|

Virtual machine variables:

| Name                  | Default value       |  Description                                                   |
|-----------------------|---------------------|----------------------------------------------------------------|
| miq_vm_name           | manageiq_gaprindashvili-3      | The name of the ManageIQ virtual machine.           |
| miq_vm_cluster        | Default             | The cluster of the virtual machine.                            |
| miq_vm_memory         | 16GiB               | The virtual machine's system memory.                           |
| miq_vm_memory_guaranteed | UNDEF            | Amount of minimal guaranteed memory of the Virtual Machine. miq_vm_memory_guaranteed parameter can't be lower than miq_vm_memory parameter. |
| miq_vm_memory_max     | UNDEF               | Upper bound of virtual machine memory up to which memory hot-plug can be performed. |
| miq_vm_cpu            | 4                   | The number of virtual machine CPU cores.                       |
| miq_vm_cpu_shares     | UNDEF               | Set a CPU shares for this Virtual Machine.                     |
| miq_vm_cpu_sockets    | UNDEF               | Number of virtual CPUs sockets of the Virtual Machine.         |
| miq_vm_cpu_threads    | UNDEF               | Number of virtual CPUs threads of the Virtual Machine.         |
| miq_vm_os             | rhel_7x64           | The virtual machine operating system.                          |
| miq_vm_root_password  | `miq_app_password`  | The root password for the virtual machine.                     |
| miq_vm_cloud_init     | UNDEF               | The cloud init dictionary to be passed to the virtual machine. |
| miq_vm_high_availability | true             | If yes ManageIQ virtual machine will be set as highly available. |
| miq_vm_high_availability_priority | 50      | Indicates the priority of the virtual machine inside the run and migration queues. The value is an integer between 0 and 100. The higher the value, the higher the priority. |
| miq_vm_delete_protected | true              | If yes ManageIQ virtual machine will be set as delete protected. |
| miq_debug_create        | false             | If true log sensitive data, useful for debug purposes.           |
| miq_wait_for_ip_version  | v4               | Specify which IP version should be wait for. Either v4 or v6.  |
| miq_wait_for_ip_timeout | 240               | Maximum ammount of time the playbook should wait for the IP to be reported. |

Virtual machine main disks variables (e.g. operating system):

| Name                | Default value        |  Description                            |
|---------------------|----------------------|-----------------------------------------|
| miq_vm_disk_name    | `miq_vm_name`        | The name of the virtual machine disk.   |
| miq_vm_disk_storage | UNDEF                | The target storage domain of the disk.  |
| miq_vm_disk_size    | Size of qcow disk    | The virtual machine disk size.          |
| miq_vm_disk_interface | virtio_scsi        | The virtual machine disk interface type.|
| miq_vm_disk_format  | cow                  | The format of the virtual machine disk. |

Virtual machine extra disks (e.g. database, log, tmp): a dict named
`miq_vm_disks` allows to describe each of the extra disks (see example
playbook). Note, that this works only with CFME.
For each disk, the following attributes can be set:

| Name      | Default value |  Description                                                         |
|-----------|---------------|----------------------------------------------------------------------|
| name      | `miq_vm_name`_`type` | The name of the virtual machine disk.                 |
| size      | UNDEF         | The virtual machine disk size (`XXGiB`).                             |
| interface | virtio_scsi   | The virtual machine disk interface type (`virtio` or `virtio_scsi`). `virtio_scsi` is recommended, as `virtio` has low limit of count of disks. |
| format    | UNDEF         | The format of the virtual machine disk (`raw` or `cow`).             |
| timeout   | UNDEF         | Timeout of disk creation.                                            |

Virtual machine NICs variables:

| Name                | Default value     |  Description                                         |
|---------------------|-------------------|------------------------------------------------------|
| miq_vm_nics         | {'name': 'nic1', 'profile_name': 'ovirtmgmt', 'interaface': 'virtio'} | List of dictionaries that defines the virtual machine network interfaces. |

The item in `miq_vm_nics` list of can contain following attributes:

| Name               | Default value  |                                              |
|--------------------|----------------|----------------------------------------------|
| name               | UNDEF          | The name of the network interface.           |
| interface          | UNDEF          | Type of the network interface.              |
| mac_address        | UNDEF          | Custom MAC address of the network interface, by default it's obtained from MAC pool. |
| profile_name       | UNDEF          | Virtual network interface profile to be attached to VM network interface. |

ManageIQ variables:

| Name               | Default value       |  Description                                                               |
|--------------------|---------------------|----------------------------------------------------------------------------|
| miq_app_username   | admin               | The username used to login to ManageIQ.                                    |
| miq_app_password   | smartvm             | The password of user specific in username used to login to ManageIQ.       |
| miq_username       | admin               | Alias of `miq_app_username` for backward compatibility.                    |
| miq_password       | smartvm             | Alias of `miq_app_password` for backward compatibility.                    |
| miq_db_username    | root                | The username to connect to the database.                                   |
| miq_db_password    | `miq_app_password`  | The password of user specific in username used to connect to the database. |
| miq_region         | 0                   | The ManageIQ region created in the database. Note: Works only with CFME.   |
| miq_company        | My Company          | The company name of the appliance.                                         |
| miq_disabled_roles | []                  | List of ManageIQ server roles to disable on the appliance.                 |
| miq_enabled_roles  | []                  | List of ManageIQ server roles to enable on the appliance.                  |

Both on ManageIQ and CloudForms, the default enabled server roles are:
 - `automate` - Automation Engine
 - `database_operations` - Database Operations
 - `event` - Event Monitor
 - `ems_inventory` - Provider Inventory
 - `ems_operations` - Provider Operations
 - `reporting` - Reporting
 - `scheduler` - Scheduler
 - `smartstate` - SmartState Analysis
 - `user_interface` - User Interface
 - `websocket` - Websocket
 - `web_services` - Web Services

RHV provider and RHV metrics variables:

| Name                  | Default value  |  Description                                           |
|-----------------------|----------------|--------------------------------------------------------|
| miq_rhv_provider_name | RHV provider   | Name of the RHV provider to be displayed in ManageIQ.  |
| metrics_fqdn          | UNDEF          | FQDN of the oVirt/RHV metrics.                         |
| metrics_user          | engine_history | The user to connection to metrics server.              |
| metrics_password      | ""             | The password of the `metrics_user` .                   |
| metrics_port          | 5432           | Port to connect to oVirt/RHV metrics.                  |
| metrics_db_name       | ovirt_engine_history | Database name of the oVirt engine metrics database. |

Example Playbook
----------------

Note that for passwords you should use Ansible vault.

Here is an example how to deploy CFME:

```yaml
    - name: Deploy CFME to oVirt engine
      hosts: localhost
      gather_facts: no

      vars_files:
        # Contains encrypted `engine_password` varibale using ansible-vault
        - passwords.yml

      vars:
        engine_fqdn: ovirt-engine.example.com
        engine_user: admin@internal

        miq_qcow_url: https://cdn.example.com/cfme-rhevm-5.9.1.2-1.x86_64.qcow2
        miq_vm_name: cfme_59
        miq_vm_cluster: mycluster
        miq_vm_cloud_init:
          host_name: "{{ miq_vm_name }}"
        miq_vm_disks:
          database:
            name: "{{ miq_vm_name }}_database"
            size: 10GiB
            interface: virtio_scsi
            format: raw
          log:
            name: "{{ miq_vm_name }}_log"
            size: 10GiB
            interface: virtio_scsi
            format: cow
          tmp:
            name: "{{ miq_vm_name }}_tmp"
            size: 10GiB
            interface: virtio_scsi
            format: cow
        miq_disabled_roles:
          - smartstate
        miq_enabled_roles:
          - notifier
          - ems_metrics_coordinator
          - ems_metrics_collector
          - ems_metrics_processor
          - embedded_ansible

      roles:
        - manageiq
      collections:
        - @NAMESPACE@.@NAME@
```

Here is an example how to deploy ManageIQ:

```yaml
---
- name: oVirt ManageIQ deployment
  hosts: localhost
  connection: local
  gather_facts: false

  vars_files:
    # Contains encrypted `engine_password` and `metrics_password`
    # varibale using ansible-vault
    - passwords.yml

  vars:
    engine_fqdn: ovirt.example.com
    engine_user: admin@internal
    engine_cafile: /etc/pki/ovirt-engine/ca.pem

    miq_qcow_url: http://releases.manageiq.org/manageiq-ovirt-hammer-6.qc2
    miq_vm_name: manageiq_hammer6
    miq_vm_cluster: mycluster

    metrics_fqdn: metrics.example.com
    metrics_port: 8443
    metrics_user: admin


  roles:
    - manageiq
  collections:
    - @NAMESPACE@.@NAME@
```
