#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Red Hat, Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: ovirt_vm_os_info
short_description: Retrieve information about all supported oVirt/RHV operating systems
version_added: "1.0.1"
author:
- "Martin Necas (@mnecas)"
description:
    - "Retrieve information all supported oVirt/RHV operating systems."
notes:
    - "This module returns a variable C(ovirt_vm_os), which
       contains a list of operating systems. You need to register the result with
       the I(register) keyword to use it."
options:
    max:
      description:
        - "The maximum number of results to return."
    filter_keys:
      description:
        - "List of atributes which should be in return."
      type: list
    name:
      description:
        - "Name of the operating system which should be return."
extends_documentation_fragment: ovirt.ovirt.ovirt_info
'''

EXAMPLES = '''
# Look at ovirt_auth module to see how to reuse authentication:

- ovirt_vm_os_info:
    auth: "{{ ovirt_auth }}"
  register: result
- debug:
    msg: "{{ result.ovirt_vm_os }}"

- ovirt_vm_os_info:
    auth: "{{ ovirt_auth }}"
    filter_keys: name,architecture
  register: result
- debug:
    msg: "{{ result.ovirt_vm_os }}"
'''

RETURN = '''
ovirt_vm_os:
    description: "List of dictionaries describing the operating systems. Operating system attributes are mapped to dictionary keys,
                  all operating systems attributes can be found at following url: http://ovirt.github.io/ovirt-engine-api-model/master/#types/operating_system_info."
    returned: On success.
    type: list
'''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ovirt.ovirt.plugins.module_utils.ovirt import (
    check_sdk,
    create_connection,
    get_dict_of_struct,
    ovirt_info_full_argument_spec,
)


def main():
    argument_spec = ovirt_info_full_argument_spec(
        max=dict(default=None, type='int'),
        filter_keys=dict(default=None, type='list'),
        name=dict(default=None, type='str'),
    )
    module = AnsibleModule(argument_spec)
    check_sdk(module)

    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        operating_systems_service = connection.system_service().operating_systems_service()
        operating_systems = operating_systems_service.list(
            max=module.params['max'],
        )
        if module.params['name']:
          operating_systems = filter(lambda x: x.name == module.params['name'], operating_systems)
        result = dict(
            ovirt_vm_os=[
                get_dict_of_struct(
                    struct=c,
                    connection=connection,
                    filter_keys=module.params['filter_keys'],
                ) for c in operating_systems
            ],
        )
        module.exit_json(changed=False, **result)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=auth.get('token') is None)


if __name__ == '__main__':
    main()
