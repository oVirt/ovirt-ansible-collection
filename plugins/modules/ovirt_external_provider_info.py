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
module: ovirt_external_provider_info
short_description: Retrieve information about one or more oVirt/RHV external providers
version_added: "1.0.0"
author: "Ondra Machacek (@machacekondra)"
description:
    - "Retrieve information about one or more oVirt/RHV external providers."
    - This module was called C(ovirt_external_provider_facts) before Ansible 2.9, returning C(ansible_facts).
      Note that the M(@NAMESPACE@.@NAME@.ovirt_external_provider_info) module no longer returns C(ansible_facts)!
notes:
    - "This module returns a variable C(ovirt_external_providers), which
       contains a list of external_providers. You need to register the result with
       the I(register) keyword to use it."
options:
    type:
        description:
            - "Type of the external provider."
        choices: ['os_image', 'os_network', 'os_volume', 'foreman']
        required: true
        type: str
        aliases: ['provider']
    name:
        description:
            - "Name of the external provider, can be used as glob expression."
        type: str
extends_documentation_fragment: @NAMESPACE@.@NAME@.ovirt_info
'''

EXAMPLES = '''
# Examples don't contain auth parameter for simplicity,
# look at ovirt_auth module to see how to reuse authentication:

# Gather information about all image external providers named C<glance>:
- @NAMESPACE@.@NAME@.ovirt_external_provider_info:
    type: os_image
    name: glance
  register: result
- ansible.builtin.debug:
    msg: "{{ result.ovirt_external_providers }}"
'''

RETURN = '''
ovirt_external_providers:
    description:
        - "List of dictionaries. Content depends on I(type)."
        - "For type C(foreman), attributes appearing in the dictionary can be found on your oVirt/RHV instance
           at the following url: http://ovirt.github.io/ovirt-engine-api-model/master/#types/external_host_provider."
        - "For type C(os_image), attributes appearing in the dictionary can be found on your oVirt/RHV instance
           at the following url: http://ovirt.github.io/ovirt-engine-api-model/master/#types/openstack_image_provider."
        - "For type C(os_volume), attributes appearing in the dictionary can be found on your oVirt/RHV instance
           at the following url: http://ovirt.github.io/ovirt-engine-api-model/master/#types/openstack_volume_provider."
        - "For type C(os_network), attributes appearing in the dictionary can be found on your oVirt/RHV instance
           at the following url: http://ovirt.github.io/ovirt-engine-api-model/master/#types/openstack_network_provider."
    returned: On success
    type: list
'''

import fnmatch
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.@NAMESPACE@.@NAME@.plugins.module_utils.ovirt import (
    check_sdk,
    create_connection,
    get_dict_of_struct,
    ovirt_info_full_argument_spec,
)


def _external_provider_service(provider_type, system_service):
    if provider_type == 'os_image':
        return system_service.openstack_image_providers_service()
    elif provider_type == 'os_network':
        return system_service.openstack_network_providers_service()
    elif provider_type == 'os_volume':
        return system_service.openstack_volume_providers_service()
    elif provider_type == 'foreman':
        return system_service.external_host_providers_service()


def main():
    argument_spec = ovirt_info_full_argument_spec(
        name=dict(default=None, required=False),
        type=dict(
            required=True,
            choices=[
                'os_image', 'os_network', 'os_volume', 'foreman',
            ],
            aliases=['provider'],
        ),
    )
    module = AnsibleModule(argument_spec)
    check_sdk(module)
    if module.params['fetch_nested'] or module.params['nested_attributes']:
        module.deprecate(
            "The 'fetch_nested' and 'nested_attributes' are deprecated please use 'follow' parameter",
            version='3.0.0',
            collection_name='ovirt.ovirt'
        )

    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        external_providers_service = _external_provider_service(
            provider_type=module.params.pop('type'),
            system_service=connection.system_service(),
        )
        if module.params['name']:
            external_providers = [
                e for e in external_providers_service.list(follow=",".join(module.params['follows']))
                if fnmatch.fnmatch(e.name, module.params['name'])
            ]
        else:
            external_providers = external_providers_service.list(follow=",".join(module.params['follows']))

        result = dict(
            ovirt_external_providers=[
                get_dict_of_struct(
                    struct=c,
                    connection=connection,
                    fetch_nested=module.params.get('fetch_nested'),
                    attributes=module.params.get('nested_attributes'),
                ) for c in external_providers
            ],
        )
        module.exit_json(changed=False, **result)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=auth.get('token') is None)


if __name__ == '__main__':
    main()
