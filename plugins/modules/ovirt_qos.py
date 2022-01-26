#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: ovirt_qos
short_description: "Module to manage QoS entries in oVirt/RHV"
author:
- "Niall O Donnell (niall.odonnell@ppb.com)"
description:
    - "Module to manage QoS entries in oVirt/RHV."
    - "Doesn't support updating a QoS that exists"
    - "Only works with storage QoS entries atm"
options:
    id:
        description:
            - "ID of the QoS to manage. Either C(id) or C(name) is required."
        type: str
    name:
        description:
            - "Name of QoS to manage. Either C(id) or C(name)/C(alias) is required."
        type: str
    description:
        description:
            - "Description of the QoS."
        type: str
    data_center:
        description:
            - "Name of the data center where the QoS entry should be created."
        type: str
        max_iops=dict(default=None),
        read_iops=dict(default=None),
        write_iops=dict(default=None),
        max_throughput=dict(default=None),
        read_throughput=dict(default=None),
        write_throughput=dict(default=None),
    max_iops:
        description:
            - "The max number of read/write iops. If passed you can't pass a value for C(read_iops) or C(write_iops)"
            - "If no value is given it will default to the HE value, assuming C(read_iops) or C(write_iops) hasn't been set"
        type: str
    write_iops:
        description:
            - "The max number of write iops. If passed you can't pass a value for C(max_iops)"
            - "If no value is given it will default to the HE value, assuming C(max_iops) hasn't been set"
        type: str
    read_iops:
        description:
            - "The max number of read iops. If passed you can't pass a value for C(max_iops)"
            - "If no value is given it will default to the HE value, assuming C(max_iops) hasn't been set"
        type: str
    max_throughput:
        description:
            - "The max number of read/write throughput. If passed you can't pass a value for C(read_throughput) or C(write_throughput)"
            - "If no value is given it will default to the HE value, assuming C(read_throughput) or C(write_throughput) hasn't been set"
        type: str
    write_throughput:
        description:
            - "The max number of write throughput. If passed you can't pass a value for C(max_throughput)"
            - "If no value is given it will default to the HE value, assuming C(max_throughput) hasn't been set"
        type: str
    read_throughput:
        description:
            - "The max number of read throughput. If passed you can't pass a value for C(max_throughput)"
            - "If no value is given it will default to the HE value, assuming C(max_throughput) hasn't been set"
        type: str
    type:
        description:
            - "The type of QoS. Allows for one of storage/cpu/network/hostnetwork"
            - "WARNING: Currently only works for storage"
        type: str
    state:
        description:
            - "Should the QoS be present/absent."
        choices: ['present', 'absent']
        default: 'present'
        type: str
extends_documentation_fragment: @NAMESPACE@.@NAME@.ovirt
'''

EXAMPLES = '''
# Create a new storage QoS with default values for max_iops and max_throughput
- ovirt_qos:
    auth: "{{ ovirt_auth }}"
    data_center: "Default"
    name: "test_qos_01"
    state: "present"
    type: "storage"

# Create a new storage QoS with default values for max_iops and read_throughput but 100 for write throughput
- ovirt_qos:
    auth: "{{ ovirt_auth }}"
    data_center: "Default"
    name: "test_qos_01"
    state: "present"
    type: "storage"
    write_throughput: 100

# Create a new storage QoS with default values for write_iops and max_throughput but 100 for read iops
- ovirt_qos:
    auth: "{{ ovirt_auth }}"
    data_center: "Default"
    name: "test_qos_01"
    state: "present"
    type: "storage"
    read_iops: 100

# Create a new storage QoS with 100 max_iops and 200 max_throughput
- ovirt_qos:
    auth: "{{ ovirt_auth }}"
    data_center: "Default"
    name: "test_qos_01"
    state: "present"
    type: "storage"
    max_iops: 100
    max_throughput: 100

# Remove a storage QoS
- ovirt_qos:
    auth: "{{ ovirt_auth }}"
    data_center: "Default"
    name: "test_qos_01"
    state: "absent"
    type: "storage"
'''

RETURN = '''
id:
    description: "ID of the managed QoS"
    returned: "On success if QoS is found."
    type: str
    sample: 7de90f31-222c-436c-a1ca-7e655bd5b60c
qos:
    description: "Dictionary of all the QoS attributes. QoS attributes can be found on your oVirt/RHV instance
                  at following url: http://ovirt.github.io/ovirt-engine-api-model/master/#types/qos."
    returned: "On success if QoS is found."
    type: dict
'''
try:
    import ovirtsdk4.types as otypes
except ImportError:
    pass

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.@NAMESPACE@.@NAME@.plugins.module_utils.ovirt import (
    BaseModule,
    check_sdk,
    create_connection,
    ovirt_full_argument_spec,
    search_by_name,
    get_entity
)

class QosModule(BaseModule):

    def _get_qos_type(self, type):
        if type == 'storage':
            return otypes.QosType.STORAGE
        elif type == 'network':
            return otypes.QosType.NETWORK
        elif type == 'hostnetwork':
            return otypes.QosType.HOSTNETWORK
        elif type == 'cpu':
            return otypes.QosType.CPU
        else:
            return None

    def build_entity(self):
        """
        Abstract method from BaseModule called from create() and remove()

        Builds the QoS from the given params

        :return: otypes.QoS
        """
        return otypes.Qos(
            name=self._module.params.get('id') if self._module.params.get('id') else self._module.params.get('name'),
            type=self._get_qos_type(self._module.params.get('type')),
            description=self._module.params.get('description') if self._module.params.get('description') else None,
            max_iops=int(self._module.params.get('max_iops')) if self._module.params.get('max_iops') is not None else None,
            max_read_iops=int(self._module.params.get('read_iops')) if self._module.params.get('read_iops') is not None else None,
            max_read_throughput=int(self._module.params.get('read_throughput')) if self._module.params.get('read_throughput') is not None else None,
            max_throughput=int(self._module.params.get('max_throughput')) if self._module.params.get('max_throughput') is not None else None,
            max_write_iops=int(self._module.params.get('write_iops')) if self._module.params.get('write_iops') is not None else None,
            max_write_throughput=int(self._module.params.get('write_throughput')) if self._module.params.get('write_throughput') is not None else None,
        )

def _get_qoss_service(connection, dc_name):
    """
    Gets the qoss_service from the data_center provided

    :returns: ovirt.services.QossService or None
    """
    dcs_service = connection.system_service().data_centers_service()
    dc = search_by_name(dcs_service, dc_name)

    if dc is None:
        dc = get_entity(dcs_service.service(dc_name))
        if dc is None:
            return None

    dc_service = dcs_service.data_center_service(dc.id)
    return dc_service.qoss_service()



def main():
    argument_spec = ovirt_full_argument_spec(
        state=dict(
            choices=['present', 'absent'],
            default='present',
        ),
        id=dict(default=None),
        name=dict(default=None),
        data_center=dict(default=None),
        max_iops=dict(default=None),
        read_iops=dict(default=None),
        write_iops=dict(default=None),
        max_throughput=dict(default=None),
        read_throughput=dict(default=None),
        write_throughput=dict(default=None),
        type=dict(default=None)
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=[['id', 'name']],
        mutually_exclusive=[
            ['max_iops','read_iops'],
            ['max_iops', 'write_iops'],
            ['max_throughput','read_throughput'],
            ['max_throughput', 'write_througput']
        ]
    )

    check_sdk(module)

    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        qoss_service = _get_qoss_service(connection, module.params.get('data_center'))

        qos_module = QosModule(
            connection=connection,
            module=module,
            service=qoss_service,
        )

        if module.params.get('state') == 'present':
            ret = qos_module.create()
        elif module.params.get('state') == 'absent':
            ret = qos_module.remove()

        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=auth.get('token') is None)

if __name__ == "__main__":
  main()

