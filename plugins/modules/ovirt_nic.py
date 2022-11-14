#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2017, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: ovirt_nic
short_description: Module to manage network interfaces of Virtual Machines in oVirt/RHV
version_added: "1.0.0"
author:
- "Ondra Machacek (@machacekondra)"
- "Martin Necas (@mnecas)"
description:
    - Module to manage network interfaces of Virtual Machines in oVirt/RHV.
options:
    id:
        description:
            - "ID of the nic to manage."
        type: str
    name:
        description:
            - Name of the network interface to manage.
        required: true
        type: str
    vm:
        description:
            - Name of the Virtual Machine to manage.
            - You must provide either C(vm) parameter or C(template) parameter.
        type: str
    template:
        description:
            - Name of the template to manage.
            - You must provide either C(vm) parameter or C(template) parameter.
        type: str
    template_version:
        description:
            - Version number of the template.
        type: int
        version_added: 1.2.0
    state:
        description:
            - Should the Virtual Machine NIC be present/absent/plugged/unplugged.
        choices: [ absent, plugged, present, unplugged ]
        default: present
        type: str
    network:
        description:
            - Logical network to which the VM network interface should use,
              by default Empty network is used if network is not specified.
        type: str
    profile:
        description:
            - Virtual network interface profile to be attached to VM network interface.
            - When not specified and network has only single profile it will be auto-selected, otherwise you must specify profile.
        type: str
    interface:
        description:
            - "Type of the network interface. For example e1000, pci_passthrough, rtl8139, rtl8139_virtio, spapr_vlan or virtio."
            - "It's required parameter when creating the new NIC."
        type: str
    mac_address:
        description:
            - Custom MAC address of the network interface, by default it's obtained from MAC pool.
        type: str
    linked:
        description:
            - Defines if the NIC is linked to the virtual machine.
        type: bool
    network_filter_parameters:
        description:
            - "The list of network filter parameters."
        elements: dict
        type: list
        version_added: 3.1.0
        suboptions:
            name:
                description:
                    - "Name of the network filter parameter."
            value:
                description:
                    - "Value of the network filter parameter."
extends_documentation_fragment: @NAMESPACE@.@NAME@.ovirt
'''

EXAMPLES = '''
# Examples don't contain auth parameter for simplicity,
# look at ovirt_auth module to see how to reuse authentication:

- name: Add NIC to VM
  @NAMESPACE@.@NAME@.ovirt_nic:
    state: present
    vm: myvm
    name: mynic
    interface: e1000
    mac_address: 00:1a:4a:16:01:56
    profile: ovirtmgmt
    network: ovirtmgmt

- name: Plug NIC to VM
  @NAMESPACE@.@NAME@.ovirt_nic:
    state: plugged
    vm: myvm
    name: mynic

- name: Unplug NIC from VM
  @NAMESPACE@.@NAME@.ovirt_nic:
    state: unplugged
    linked: false
    vm: myvm
    name: mynic

- name: Add NIC to template
  @NAMESPACE@.@NAME@.ovirt_nic:
    auth: "{{ ovirt_auth }}"
    state: present
    template: my_template
    name: nic1
    interface: virtio
    profile: ovirtmgmt
    network: ovirtmgmt

- name: Remove NIC from VM
  @NAMESPACE@.@NAME@.ovirt_nic:
    state: absent
    vm: myvm
    name: mynic

# Change NIC Name
- @NAMESPACE@.@NAME@.ovirt_nic:
    id: 00000000-0000-0000-0000-000000000000
    name: "new_nic_name"
    vm: myvm

# Add NIC network filter parameters
- @NAMESPACE@.@NAME@.ovirt_nic:
    state: present
    name: mynic
    vm: myvm
    network_filter_parameters:
      - name: GATEWAY_MAC
        value: 01:02:03:ab:cd:ef
      - name: GATEWAY_MAC
        value: 01:02:03:ab:cd:eg
      - name: GATEWAY_MAC
        value: 01:02:03:ab:cd:eh
'''

RETURN = '''
id:
    description: ID of the network interface which is managed
    returned: On success if network interface is found.
    type: str
    sample: 7de90f31-222c-436c-a1ca-7e655bd5b60c
nic:
    description: "Dictionary of all the network interface attributes. Network interface attributes can be found on your oVirt/RHV instance
                  at following url: http://ovirt.github.io/ovirt-engine-api-model/master/#types/nic."
    returned: On success if network interface is found.
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
    equal,
    get_link_name,
    ovirt_full_argument_spec,
    search_by_name,
)


class EntityNicsModule(BaseModule):

    def __init__(self, *args, **kwargs):
        super(EntityNicsModule, self).__init__(*args, **kwargs)
        self.vnic_id = None

    @property
    def vnic_id(self):
        return self._vnic_id

    @vnic_id.setter
    def vnic_id(self, vnic_id):
        self._vnic_id = vnic_id

    def post_update(self, entity):
        self._set_network_filter_parameters(entity.id)

    def _set_network_filter_parameters(self, entity_id):
        if self._module.params['network_filter_parameters'] is not None:
            nfps_service = self._service.service(entity_id).network_filter_parameters_service()
            nfp_list = nfps_service.list()
            # Remove all previous network filter parameters
            for nfp in nfp_list:
                nfps_service.service(nfp.id).remove()

            # Create all specified netwokr filters by user
            for nfp in self._network_filter_parameters():
                nfps_service.add(nfp)

    def build_entity(self):
        return otypes.Nic(
            id=self._module.params.get('id'),
            name=self._module.params.get('name'),
            interface=otypes.NicInterface(
                self._module.params.get('interface')
            ) if self._module.params.get('interface') else None,
            vnic_profile=otypes.VnicProfile(
                id=self.vnic_id,
            ) if self.vnic_id else None,
            mac=otypes.Mac(
                address=self._module.params.get('mac_address')
            ) if self._module.params.get('mac_address') else None,
            linked=self.param('linked') if self.param('linked') is not None else None,
        )

    def update_check(self, entity):
        if self._module.params.get('vm'):
            return (
                equal(self._module.params.get('interface'), str(entity.interface)) and
                equal(self._module.params.get('linked'), entity.linked) and
                equal(self._module.params.get('name'), str(entity.name)) and
                equal(self._module.params.get('profile'), get_link_name(self._connection, entity.vnic_profile)) and
                equal(self._module.params.get('mac_address'), entity.mac.address) and
                equal(self._network_filter_parameters(), entity.network_filter_parameters)
            )
        elif self._module.params.get('template'):
            return (
                equal(self._module.params.get('interface'), str(entity.interface)) and
                equal(self._module.params.get('linked'), entity.linked) and
                equal(self._module.params.get('name'), str(entity.name)) and
                equal(self._module.params.get('profile'), get_link_name(self._connection, entity.vnic_profile))
            )

    def _network_filter_parameters(self):
        if self._module.params['network_filter_parameters'] is None:
            return []
        networkFilterParameters = list()
        for networkFilterParameter in self._module.params['network_filter_parameters']:
            networkFilterParameters.append(
                otypes.NetworkFilterParameter(
                    name=networkFilterParameter.get("name"),
                    value=networkFilterParameter.get("value")
                )
            )
        return networkFilterParameters


def get_vnics(networks_service, network, connection):
    resp = []
    vnic_services = connection.system_service().vnic_profiles_service()
    for vnic in vnic_services.list():
        if vnic.network.id == network.id:
            resp.append(vnic)
    return resp


def main():
    argument_spec = ovirt_full_argument_spec(
        state=dict(type='str', default='present', choices=['absent', 'plugged', 'present', 'unplugged']),
        vm=dict(type='str'),
        id=dict(default=None),
        template=dict(type='str'),
        name=dict(type='str', required=True),
        interface=dict(type='str'),
        template_version=dict(type='int', default=None),
        profile=dict(type='str'),
        network=dict(type='str'),
        mac_address=dict(type='str'),
        linked=dict(type='bool'),
        network_filter_parameters=dict(type='list', default=None, elements='dict'),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[['vm', 'template']],
    )

    check_sdk(module)

    try:
        # Locate the service that manages the virtual machines and use it to
        # search for the NIC:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        entity_name = None

        if module.params.get('vm'):
            # Locate the VM, where we will manage NICs:
            entity_name = module.params.get('vm')
            collection_service = connection.system_service().vms_service()
        elif module.params.get('template'):
            entity_name = module.params.get('template')
            collection_service = connection.system_service().templates_service()

        # TODO: We have to modify the search_by_name function to accept raise_error=True/False,
        if module.params['template_version'] is not None:
            entity = [
                t for t in collection_service.list()
                if t.version.version_number == module.params['template_version']
            ]
            if not entity:
                raise ValueError(
                    "Template with name '%s' and version '%s' was not found'" % (
                        module.params['template'],
                        module.params['template_version']
                    )
                )
            entity = entity[0]
        else:
            entity = search_by_name(collection_service, entity_name)
        if entity is None:
            raise Exception("Vm/Template '%s' was not found." % entity_name)

        service = collection_service.service(entity.id)
        cluster_id = entity.cluster

        nics_service = service.nics_service()
        entitynics_module = EntityNicsModule(
            connection=connection,
            module=module,
            service=nics_service,
        )

        # Find vNIC id of the network interface (if any):
        if module.params['network']:
            profile = module.params.get('profile')
            cluster_name = get_link_name(connection, cluster_id)
            dcs_service = connection.system_service().data_centers_service()
            dc = dcs_service.list(search='Clusters.name=%s' % cluster_name)[0]
            networks_service = dcs_service.service(dc.id).networks_service()
            network = next(
                (n for n in networks_service.list()
                 if n.name == module.params['network']),
                None
            )
            if network is None:
                raise Exception(
                    "Network '%s' was not found in datacenter '%s'." % (
                        module.params['network'],
                        dc.name
                    )
                )
            if profile:
                for vnic in connection.system_service().vnic_profiles_service().list():
                    if vnic.name == profile and vnic.network.id == network.id:
                        entitynics_module.vnic_id = vnic.id
            else:
                # When not specified which vnic use ovirtmgmt/ovirtmgmt
                vnics = get_vnics(networks_service, network, connection)
                if len(vnics) == 1:
                    entitynics_module.vnic_id = vnics[0].id
                else:
                    raise Exception(
                        "You didn't specify any vnic profile. "
                        "Following vnic profiles are in system: '%s', please specify one of them" % ([vnic.name for vnic in vnics])
                    )
        # Handle appropriate action:
        state = module.params['state']
        if state == 'present':
            ret = entitynics_module.create()
        elif state == 'absent':
            ret = entitynics_module.remove()
        elif state == 'plugged':
            entitynics_module.create()
            ret = entitynics_module.action(
                action='activate',
                action_condition=lambda nic: not nic.plugged,
                wait_condition=lambda nic: nic.plugged,
            )
        elif state == 'unplugged':
            entitynics_module.create()
            ret = entitynics_module.action(
                action='deactivate',
                action_condition=lambda nic: nic.plugged,
                wait_condition=lambda nic: not nic.plugged,
            )

        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=auth.get('token') is None)


if __name__ == "__main__":
    main()
