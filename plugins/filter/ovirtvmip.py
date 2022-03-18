'Module to create filter to find IP addresses in VMs'

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from xml.etree import ElementTree


class FilterModule(object):
    'Filter for IP addresses on newly created VMs'

    def filters(self):
        'Define filters'
        return {
            'ovirtvmip': self.ovirtvmip,
            'ovirtvmips': self.ovirtvmips,
            'ovirtvmipv4': self.ovirtvmipv4,
            'ovirtvmipsv4': self.ovirtvmipsv4,
            'ovirtvmipv6': self.ovirtvmipv6,
            'ovirtvmipsv6': self.ovirtvmipsv6,
            'filtervalue': self.filtervalue,
            'removesensitivevmdata': self.removesensitivevmdata,
            'ovirtdiff': self.ovirtdiff,
            'get_network_xml_to_dict': self.get_network_xml_to_dict,
        }

    def ovirtdiff(self, vm1, vm2):
        """
        This filter takes two dictionaries of two different resources and compare
        them. It return dictionari with keys 'before' and 'after', where 'before'
        containes old values of resources and 'after' contains new values.
        This is mainly good to compare current VM object and next run VM object to see
        the difference for the next_run.
        """
        before = []
        after = []
        if vm1.get('next_run_configuration_exists'):
            keys = [
                key for key in set(list(vm1.keys()) + list(vm2.keys()))
                if (key in vm1 and (key not in vm2 or vm2[key] != vm1[key])) or (key in vm2 and (key not in vm1 or vm1[key] != vm2[key]))
            ]
            for key in keys:
                before.append((key, vm1.get(key)))
                after.append((key, vm2.get(key, vm1.get(key))))

        return {
            'before': dict(before),
            'after': dict(after),
        }

    def filtervalue(self, data, attr, value):
        """ Filter to findall occurance of some value in dict """
        items = []
        for item in data:
            if item[attr] == value:
                items.append(item)
        return items

    def ovirtvmip(self, ovirt_vms, attr=None, network_ip=None):
        'Return first IP'
        return self.__get_first_ip(self.ovirtvmips(ovirt_vms, attr))

    def ovirtvmips(self, ovirt_vms, attr=None, network_ip=None):
        'Return list of IPs'
        return self._parse_ips(ovirt_vms, attr=attr)

    def ovirtvmipv4(self, ovirt_vms, attr=None, network_ip=None):
        'Return first IPv4 IP'
        return self.__get_first_ip(self.ovirtvmipsv4(ovirt_vms, attr, network_ip))

    def ovirtvmipsv4(self, ovirt_vms, attr=None, network_ip=None):
        'Return list of IPv4 IPs'
        ips = self._parse_ips(ovirt_vms, lambda version: version == 'v4', attr)
        resp = [ip for ip in ips if self.__address_in_network(ip, network_ip)]
        return resp

    def ovirtvmipv6(self, ovirt_vms, attr=None, network_ip=None):
        'Return first IPv6 IP'
        return self.__get_first_ip(self.ovirtvmipsv6(ovirt_vms, attr))

    def ovirtvmipsv6(self, ovirt_vms, attr=None, network_ip=None):
        'Return list of IPv6 IPs'
        return self._parse_ips(ovirt_vms, lambda version: version == 'v6', attr)

    def _parse_ips(self, ovirt_vms, version_condition=lambda version: True, attr=None):
        if not isinstance(ovirt_vms, list):
            ovirt_vms = [ovirt_vms]

        if attr is None:
            return self._parse_ips_aslist(ovirt_vms, version_condition)
        else:
            return self._parse_ips_asdict(ovirt_vms, version_condition, attr)

    @staticmethod
    def _parse_ips_asdict(ovirt_vms, version_condition=lambda version: True, attr=None):
        vm_ips = {}
        for ovirt_vm in ovirt_vms:
            ips = []
            for device in ovirt_vm.get('reported_devices', []):
                for curr_ip in device.get('ips', []):
                    if version_condition(curr_ip.get('version')):
                        ips.append(curr_ip.get('address'))
            vm_ips[ovirt_vm.get(attr)] = ips
        return vm_ips

    @staticmethod
    def _parse_ips_aslist(ovirt_vms, version_condition=lambda version: True):
        ips = []
        for ovirt_vm in ovirt_vms:
            for device in ovirt_vm.get('reported_devices', []):
                for curr_ip in device.get('ips', []):
                    if version_condition(curr_ip.get('version')):
                        ips.append(curr_ip.get('address'))
        return ips

    @staticmethod
    def __get_first_ip(res):
        return res[0] if isinstance(res, list) and res else res

    def __address_in_network(self, ip, net):
        "Return boolean if IP is in network."
        if net:
            ipaddr = int(''.join(['%02x' % int(x) for x in ip.split('.')]), 16)
            netstr, bits = net.split('/')
            netaddr = int(''.join(['%02x' % int(x)
                                   for x in netstr.split('.')]), 16)
            mask = (0xffffffff << (32 - int(bits))) & 0xffffffff
            return (ipaddr & mask) == (netaddr & mask)
        return True

    def removesensitivevmdata(self, data, key_to_remove='root_password'):
        for value in data:
            if key_to_remove in value:
                value[key_to_remove] = "******"
            if 'cloud_init' in value and key_to_remove in value['cloud_init']:
                value['cloud_init'][key_to_remove] = "******"
            if 'sysprep' in value and key_to_remove in value['sysprep']:
                value['sysprep'][key_to_remove] = "******"
            if 'profile' in value:
                profile = value['profile']
                if key_to_remove in profile:
                    profile[key_to_remove] = "******"
                if 'cloud_init' in profile and key_to_remove in profile['cloud_init']:
                    profile['cloud_init'][key_to_remove] = "******"
                if 'sysprep' in profile and key_to_remove in profile['sysprep']:
                    profile['sysprep'][key_to_remove] = "******"
        return data

    def get_network_xml_to_dict(self, data):
        tree = ElementTree.fromstring(data)
        resp = {}
        for child in tree:
            if child.tag == 'bridge':
                resp['bridge'] = child.attrib
            if child.tag == 'uuid':
                resp['uuid'] = child.text
        return resp
