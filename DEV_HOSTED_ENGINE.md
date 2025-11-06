# Testing hosted_engine_setup Role

## Minimum Requirements

**Host OS**: A > RHEL 9 clone

**Packages**:
```bash
dnf install -y ansible-core nfs-utils ovirt-engine-appliance
```
(Role installs `ovirt-hosted-engine-setup` which pulls in libvirt, qemu-kvm, virt-install)

**Required Ansible Collections**:
```bash
sudo ansible-galaxy collection install ansible.posix
```

**Services**:
```bash
systemctl enable --now libvirtd nfs-server
```

## Minimal Configuration

**Required vars** (save as `test_vars.json`):
```json
{
  "he_bridge_if": "eth0",
  "he_fqdn": "engine.local",
  "he_vm_mac_addr": "52:54:00:11:22:33",
  "he_domain_type": "nfs",
  "he_storage_domain_addr": "127.0.0.1",
  "he_storage_domain_path": "/exports/hosted-engine",
  "he_appliance_password": "password",
  "he_admin_password": "password"
}
```

**NFS setup**:
```bash
mkdir -p /exports/hosted-engine
chown 36:36 /exports/hosted-engine
echo "/exports/hosted-engine 127.0.0.1(rw,sync,no_root_squash)" >> /etc/exports
exportfs -ra
```

**Network** (if using static IP instead of DHCP):
```json
{
  "he_vm_ip_addr": "192.168.122.100",
  "he_vm_ip_prefix": "24",
  "he_gateway": "192.168.122.1",
  "he_dns_addr": "192.168.122.1",
  "he_vm_etc_hosts": true
}
```

## Run Test

```bash
sudo ansible-playbook test_playbook.yml -e @test_vars.json
```

**Minimal playbook** (`test_playbook.yml`):
```yaml
---
- hosts: localhost
  connection: local
  become: true
  roles:
    - ovirt.ovirt.hosted_engine_setup
```

## Testing from Git Checkout (Local Development)

To test changes from your local git checkout instead of the installed collection:

**2. Create symlink to collection path (role needs root)**:
```bash
sudo mkdir -p /root/.ansible/collections/ansible_collections/ovirt
sudo ln -s /path/to/ovirt-ansible-collection /root/.ansible/collections/ansible_collections/ovirt/ovirt
```

**3. Verify**:
```bash
ansible-galaxy collection list | grep ovirt
```

Now your playbook will use the local checkout instead of the installed version.

## Optional: UEFI Boot

Add to vars:
```json
{
  "he_use_uefi": true
}
```

## Optional: Custom Appliance

Add one of these vars:
```json
{
  "he_appliance": "/path/to/appliance.[ova/qcow2]",
  "he_appliance_package": "/path/to/package.rpm",
  "he_appliance_package": "alternative-appliance-name"
}
```

Default: uses installed `ovirt-engine-appliance-[host distro][host major version]` package.
