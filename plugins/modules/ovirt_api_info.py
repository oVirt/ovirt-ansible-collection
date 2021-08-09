#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: ovirt_api_info
short_description: Retrieve information about the oVirt/RHV API
version_added: "1.0.0"
author:
- "Ondra Machacek (@machacekondra)"
description:
    - "Retrieve information about the oVirt/RHV API."
    - This module was called C(ovirt_api_facts) before Ansible 2.9, returning C(ansible_facts).
      Note that the M(@NAMESPACE@.@NAME@.ovirt_api_info) module no longer returns C(ansible_facts)!
notes:
    - "This module returns a variable C(ovirt_api),
       which contains a information about oVirt/RHV API. You need to register the result with
       the I(register) keyword to use it."
extends_documentation_fragment: @NAMESPACE@.@NAME@.ovirt_info
'''

EXAMPLES = '''
# Examples don't contain auth parameter for simplicity,
# look at ovirt_auth module to see how to reuse authentication:

# Gather information oVirt API:
- @NAMESPACE@.@NAME@.ovirt_api_info:
  register: result
- ansible.builtin.debug:
    msg: "{{ result.ovirt_api }}"
'''

RETURN = '''
ovirt_api:
    description: "Dictionary describing the oVirt API information.
                  Api attributes are mapped to dictionary keys,
                  all API attributes can be found at following
                  url: https://ovirt.example.com/ovirt-engine/api/model#types/api."
    returned: On success.
    type: dict
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
    argument_spec = ovirt_info_full_argument_spec()
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
        api = connection.system_service().get()
        result = dict(
            ovirt_api=get_dict_of_struct(
                struct=api,
                connection=connection,
                fetch_nested=module.params.get('fetch_nested'),
                attributes=module.params.get('nested_attributes'),
            )
        )
        module.exit_json(changed=False, **result)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=auth.get('token') is None)


if __name__ == '__main__':
    main()
