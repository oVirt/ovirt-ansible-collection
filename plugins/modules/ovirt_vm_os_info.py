#!/usr/bin/python
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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: ovirt_vm_os_info
short_description: Retrieve information on all supported oVirt/RHV operating systems
version_added: "1.1.0"
author:
- "Martin Necas (@mnecas)"
- "Chris Brown (@snecklifter)"
description:
    - "Retrieve information on all supported oVirt/RHV operating systems."
notes:
    - "This module returns a variable C(ovirt_operating_systems), which
       contains a list of operating systems. You need to register the result with
       the I(register) keyword to use it."
options:
    filter_keys:
      description:
        - "List of attributes which should be in returned."
      type: list
      elements: str
    name:
      description:
        - "Name of the operating system which should be returned."
      type: str
extends_documentation_fragment: @NAMESPACE@.@NAME@.ovirt_info
'''

EXAMPLES = '''
# Look at ovirt_auth module to see how to reuse authentication:

- @NAMESPACE@.@NAME@.ovirt_vm_os_info:
    auth: "{{ ovirt_auth }}"
  register: result
- ansible.builtin.debug:
    msg: "{{ result.ovirt_operating_systems }}"

- @NAMESPACE@.@NAME@.ovirt_vm_os_info:
    auth: "{{ ovirt_auth }}"
    filter_keys: name,architecture
  register: result
- ansible.builtin.debug:
    msg: "{{ result.ovirt_operating_systems }}"
'''

RETURN = '''
ovirt_operating_systems:
    description: "List of dictionaries describing the operating systems. Operating system attributes are mapped to dictionary keys,
                  all operating systems attributes can be found at following url:
                  http://ovirt.github.io/ovirt-engine-api-model/master/#types/operating_system_info."
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


def main():
    argument_spec = ovirt_info_full_argument_spec(
        filter_keys=dict(default=None, type='list', elements='str', no_log=True),
        name=dict(default=None, type='str'),
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
        operating_systems_service = connection.system_service().operating_systems_service()
        operating_systems = operating_systems_service.list()
        if module.params['name']:
            operating_systems = filter(lambda x: x.name == module.params['name'], operating_systems)
        result = dict(
            ovirt_operating_systems=[
                get_dict_of_struct(
                    struct=c,
                    connection=connection,
                    fetch_nested=module.params.get('fetch_nested'),
                    attributes=module.params.get('nested_attributes'),
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
