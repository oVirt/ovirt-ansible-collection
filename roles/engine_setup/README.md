oVirt Engine Setup
==================

Installs required packages for oVirt Engine deployment, generates answerfile
and runs engine-setup.
Optionally the role updates oVirt engine packages.

Role Variables
--------------

By default engine-setup uses an answer file specific for version of oVirt
based on ``ovirt_engine_setup_version`` parameter. You can provide your own answer file
to ``ovirt_engine_setup_answer_file_path`` variable.

* Common options for role:

| Name                            | Default value         |  Description                                              |
|---------------------------------|-----------------------|-----------------------------------------------------------|
| ovirt_engine_setup_answer_file_path   | UNDEF                 | Path to custom answerfile for `engine-setup`. |
| ovirt_engine_setup_use_remote_answer_file | False             | If `True`, use answerfile's path on the remote machine. This option should be used if the installation occurs on the remote machine and the answerfile is located there as well. |
| ovirt_engine_setup_update_setup_packages | False              | If `True`, setup packages will be updated before `engine-setup` is executed. It makes sense if Engine has already been installed. |
| ovirt_engine_setup_perform_upgrade    | False                 | If `True`, this role is used to perform an upgrade. |
| ovirt_engine_setup_product_type       | oVirt                 | One of ["oVirt", "RHV"], case insensitive. |
| ovirt_engine_setup_offline            | False                 | If `True`, updates for all packages will be disabled. |

* Common options for engine:

| Name                            | Default value         |  Description                                              |
|---------------------------------|-----------------------|-----------------------------------------------------------|
| ovirt_engine_setup_version            | 4.4                   | Allowed versions: [4.1, 4.2, 4.3, 4.4]. |
| ovirt_engine_setup_package_list       | []                    | List of extra packages to be installed on engine apart from `ovirt_engine` package. |
| ovirt_engine_setup_fqdn               | UNDEF                 | Host fully qualified DNS name of the server. |
| ovirt_engine_setup_organization       | UNDEF                 | Organization name for certificate. |
| ovirt_engine_setup_firewall_manager   | firewalld             | Specify the type of firewall manager to configure on Engine host, following values are available: `firewalld`,`iptables` or empty value (`null`) to skip firewall configuration. |
| ovirt_engine_setup_require_rollback   | UNDEF                 | If `True`, setup will require to be able to rollback new packages in case of a failure. If not specified, the default answer from `engine-setup` will be used. Valid for updating/upgrading. |
| ovirt_engine_setup_admin_password     | UNDEF                 | Password for the automatically created administrative user of the oVirt Engine.
| ovirt_engine_setup_wait_running_tasks | False                 | If `True`, engine-setup will wait for running tasks to finish. Valid for `ovirt_engine_setup_version` >= 4.2. |
| ovirt_engine_cinderlib_enable         | False                 | If `True`, cinderlib is enabled. Valid for `ovirt_engine_setup_version` >= 4.3. |
| ovirt_engine_setup_engine_configs     | []                    | List of dictionaries with keys `key`, `value` and `version`. The engine-config will be called with parametrs "-s `key`=`value`" when specified `version` it will append "--cver=`version`" to the config.  |

* Engine Database:

| Name                            | Default value         |  Description                                              |
|---------------------------------|-----------------------|-----------------------------------------------------------|
| ovirt_engine_setup_db_host            | localhost             | IP address or host name of a PostgreSQL server for Engine database. By default the database will be configured on the same host as the Engine. |
| ovirt_engine_setup_db_port            | 5432                  | Engine database port. |
| ovirt_engine_setup_db_name            | engine                | Engine database name. |
| ovirt_engine_setup_db_user            | engine                | Engine database user. |
| ovirt_engine_setup_db_password        | UNDEF                 | Engine database password. |
| ovirt_engine_setup_engine_vacuum_full | False                 | Used only when upgrading. If `True`, engine database vacuum will be performed before upgrade. |

* Engine Data Warehouse Database:

| Name                            | Default value         |  Description                                              |
|---------------------------------|-----------------------|-----------------------------------------------------------|
| ovirt_engine_setup_dwh_db_configure   | True            | If `True`, the DWH Database will be configured manually. |
| ovirt_engine_setup_dwh_db_host        | localhost             | IP address or host name of a PostgreSQL server for DWH database. By default the DWH database will be configured on the same host as the Engine. |
| ovirt_engine_setup_dwh_db_port        | 5432                  | DWH database port. |
| ovirt_engine_setup_dwh_db_name        | ovirt_engine_history  | DWH database name. |
| ovirt_engine_setup_dwh_db_user        | ovirt_engine_history  | DWH database user. |
| ovirt_engine_setup_dwh_db_password    | UNDEF                 | DWH database password. |
| ovirt_engine_setup_dwh_vacuum_full    | False                 | Used only when upgrading. If `True`, DWH databse vacuum will be performed before upgrade. |

* OVN related options:

| Name                            | Default value         |  Description                                              |
|---------------------------------|-----------------------|-----------------------------------------------------------|
| ovirt_engine_setup_provider_ovn_configure| True               | If `True`, OVN provider will be configured. Valid for `ovirt_engine_setup_version` >= 4.2. |
| ovirt_engine_setup_provider_ovn_username | admin@internal     | Username for OVN. |
| ovirt_engine_setup_provider_ovn_password | UNDEF              | Password for OVN. |

* Apache related options:

| Name                            | Default value         |  Description                                              |
|---------------------------------|-----------------------|-----------------------------------------------------------|
| ovirt_engine_setup_apache_config_root_redirection | True               | If `True`, `engine-setup` will configure the default page in Apache to automatically redirect clients to ovirt_engine default page.   |
| ovirt_engine_setup_apache_config_ssl | True     | If `False`, `engine-setup` will not configure Apache SSL settings and administrators will need to configure it manually. |

Dependencies
------------

None

Example Playbook
----------------

```yaml
---
# Example of oVirt setup:
- name: Setup oVirt
  hosts: engine
  vars_files:
    # Contains encrypted `ovirt_engine_setup_admin_password` variable using ansible-vault
    - passwords.yml
  vars:
    ovirt_engine_setup_version: '4.2'
    ovirt_engine_setup_organization: 'of.ovirt.engine.com'
  roles:
    - engine-setup
  collections:
    - ovirt.ovirt


# Example of RHV setup:
- name: Setup RHV
  hosts: engine
  vars_files:
    # Contains encrypted `ovirt_engine_setup_admin_password` variable using ansible-vault
    - passwords.yml
  vars:
    ovirt_engine_setup_version: '4.2'
    ovirt_engine_setup_organization: 'rhv.redhat.com'
    ovirt_engine_setup_product_type: 'rhv'
  roles:
    - engine-setup
  collections:
    - ovirt.ovirt


# Example of oVirt setup with engine_configs:
- name: Setup oVirt
  hosts: engine
  vars_files:
    # Contains encrypted `ovirt_engine_setup_admin_password` variable using ansible-vault
    - passwords.yml
  vars:
    ovirt_engine_setup_version: '4.4'
    ovirt_engine_setup_organization: 'of.ovirt.engine.com'
    ovirt_engine_setup_engine_configs:
      - key: SpiceProxyDefault
        value: prot://proxy
        version: general

  roles:
    - engine-setup
  collections:
    - ovirt.ovirt
```
