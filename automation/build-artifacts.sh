#!/bin/bash -xe

ROOT_PATH=$PWD

# remove any previous artifacts
rm -rf ../ansible_collections
rm -f ./*tar.gz

# Create exported-artifacts
[[ -d exported-artifacts ]] || mkdir -p $ROOT_PATH/exported-artifacts

# Create builds

./build.sh build ovirt $ROOT_PATH
./build.sh build rhv $ROOT_PATH

OVIRT_BUILD=$ROOT_PATH/ansible_collections/ovirt/ovirt/
RHV_BUILD=$ROOT_PATH/ansible_collections/redhat/rhv

cd $OVIRT_BUILD
# create the src.rpm
rpmbuild \
    -D "_srcrpmdir $ROOT_PATH/output" \
    -D "_topmdir $ROOT_PATH/rpmbuild" \
    -ts ./*.gz

# install any build requirements
yum-builddep $ROOT_PATH/output/*src.rpm

# Remove the tarball so it will not be included in galaxy build
mv ./*.gz $ROOT_PATH/exported-artifacts/

# Overwrite github README with dynamic
mv ./README.md.in ./README.md

# create tar for galaxy
ansible-galaxy collection build

# create the rpms
rpmbuild \
    -D "_rpmdir $ROOT_PATH/output" \
    -D "_topmdir $ROOT_PATH/rpmbuild" \
    --rebuild  $ROOT_PATH/output/*.src.rpm

cd $RHV_BUILD

# Remove the tarball so it will not be included in automation hub build
rm -rf *.gz

# Overwrite github README with dynamic
mv ./README.md.in ./README.md

# create tar for automation hub
ansible-galaxy collection build

# Store any relevant artifacts in exported-artifacts for the ci system to
# archive
find $ROOT_PATH/output -iname \*rpm -exec mv "{}" $ROOT_PATH/exported-artifacts/ \;

# Export build for Ansible Galaxy
mv $OVIRT_BUILD/*tar.gz $ROOT_PATH/exported-artifacts/
# Export build for Automation Hub
mv $RHV_BUILD/*tar.gz $ROOT_PATH/exported-artifacts/

COLLECTION_DIR="/usr/local/share/ansible/collections/ansible_collections/ovirt/ovirt"
export ANSIBLE_LIBRARY="$COLLECTION_DIR/plugins/modules"
mkdir -p $COLLECTION_DIR
cp -r $OVIRT_BUILD/* $COLLECTION_DIR
cd $COLLECTION_DIR

pip3 install rstcheck antsibull-changelog ansible-lint

ansible-test sanity
/usr/local/bin/antsibull-changelog lint
if ! /usr/local/bin/ansible-lint roles/* -x 204; then
    echo "ERROR: ansible-lint failed. Ignoring for now, see also:"
    echo "https://github.com/oVirt/ovirt-ansible-collection/issues/219"
fi

cd $ROOT_PATH
