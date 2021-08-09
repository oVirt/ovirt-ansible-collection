#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: ovirt_host_info
short_description: Retrieve information about one or more oVirt/RHV hosts
version_added: "1.0.0"
author:
- "Ondra Machacek (@machacekondra)"
- "Martin Necas (@mnecas)"
description:
    - "Retrieve information about one or more oVirt/RHV hosts."
    - This module was called C(ovirt_host_facts) before Ansible 2.9, returning C(ansible_facts).
      Note that the M(@NAMESPACE@.@NAME@.ovirt_host_info) module no longer returns C(ansible_facts)!
notes:
    - "This module returns a variable C(ovirt_hosts), which
       contains a list of hosts. You need to register the result with
       the I(register) keyword to use it."
options:
    pattern:
        description:
            - "Search term which is accepted by oVirt/RHV search backend."
            - "For example to search host X from datacenter Y use following pattern:
               name=X and datacenter=Y"
        type: str
    all_content:
        description:
            - "If I(true) all the attributes of the hosts should be
               included in the response."
        default: False
        type: bool
    cluster_version:
        description:
            - "Filter the hosts based on the cluster version."
        type: str

extends_documentation_fragment: @NAMESPACE@.@NAME@.ovirt_info
'''

EXAMPLES = '''
# Examples don't contain auth parameter for simplicity,
# look at ovirt_auth module to see how to reuse authentication:

# Gather information about all hosts which names start with C(host) and
# belong to data center C(west):
- @NAMESPACE@.@NAME@.ovirt_host_info:
    pattern: name=host* and datacenter=west
  register: result
- ansible.builtin.debug:
    msg: "{{ result.ovirt_hosts }}"
# All hosts with cluster version 4.2:
- @NAMESPACE@.@NAME@.ovirt_host_info:
    pattern: name=host*
    cluster_version: "4.2"
  register: result
- ansible.builtin.debug:
    msg: "{{ result.ovirt_hosts }}"
'''

RETURN = '''
ovirt_hosts:
    description: "List of dictionaries describing the hosts. Host attributes are mapped to dictionary keys,
                  all hosts attributes can be found at following url: http://ovirt.github.io/ovirt-engine-api-model/master/#types/host."
    returned: On success.
    type: list
'''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.@NAMESPACE@.@NAME@.plugins.module_utils.ovirt import (
    check_sdk,
    create_connection,
    get_dict_of_struct,
    ovirt_info_full_argument_spec,
)


def get_filtered_hosts(cluster_version, hosts, connection):
    # Filtering by cluster version returns only those which have same cluster version as input
    filtered_hosts = []
    for host in hosts:
        cluster = connection.follow_link(host.cluster)
        cluster_version_host = str(cluster.version.major) + '.' + str(cluster.version.minor)
        if cluster_version_host == cluster_version:
            filtered_hosts.append(host)
    return filtered_hosts


def main():
    argument_spec = ovirt_info_full_argument_spec(
        pattern=dict(default='', required=False),
        all_content=dict(default=False, type='bool'),
        cluster_version=dict(default=None, type='str'),
    )
    module = AnsibleModule(argument_spec)
    check_sdk(module)
    if module.params['fetch_nested'] or module.params['nested_attributes']:
        module.deprecate(
            "The 'fetch_nested' and 'nested_attributes' are deprecated please use 'follow' parameter",
            version='2.0.0',
            collection_name='ovirt.ovirt'
        )

    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        hosts_service = connection.system_service().hosts_service()
        hosts = hosts_service.list(
            search=module.params['pattern'],
            all_content=module.params['all_content']
        )
        cluster_version = module.params.get('cluster_version')
        if cluster_version is not None:
            hosts = get_filtered_hosts(cluster_version, hosts, connection)
        result = dict(
            ovirt_hosts=[
                get_dict_of_struct(
                    struct=c,
                    connection=connection,
                    fetch_nested=module.params.get('fetch_nested'),
                    attributes=module.params.get('nested_attributes'),
                ) for c in hosts
            ],
        )
        module.exit_json(changed=False, **result)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=auth.get('token') is None)


if __name__ == '__main__':
    main()
