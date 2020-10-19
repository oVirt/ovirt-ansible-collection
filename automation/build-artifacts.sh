#!/bin/bash -xe

ROOT_PATH=$PWD

# remove any previous artifacts
rm -rf ../ansible_collections
rm -f ./*tar.gz

# Create builds

./build.sh build ovirt $ROOT_PATH
./build.sh build rhv $ROOT_PATH

OVIRT_BUILD=$ROOT_PATH/ansible_collections/ovirt/ovirt/
RHV_BUILD=$ROOT_PATH/ansible_collections/redhat/rhv

cd $OVIRT_BUILD
# create the src.rpm
rpmbuild \
    -D "_srcrpmdir $PWD/output" \
    -D "_topmdir $PWD/rpmbuild" \
    -ts ./*.gz

# install any build requirements
yum-builddep output/*src.rpm

# create tar for galaxy
ansible-galaxy collection build

# create the rpms
rpmbuild \
    -D "_rpmdir $PWD/output" \
    -D "_topmdir $PWD/rpmbuild" \
    --rebuild output/*.src.rpm

cd $RHV_BUILD

# create tar for automation hub
ansible-galaxy collection build

# Store any relevant artifacts in exported-artifacts for the ci system to
# archive
[[ -d exported-artifacts ]] || mkdir -p $ROOT_PATH/exported-artifacts $ROOT_PATH/exported-artifacts/

find $OVIRT_BUILD/output -iname \*rpm -exec mv "{}" $ROOT_PATH/exported-artifacts/ \;
mv $OVIRT_BUILD/*tar.gz $ROOT_PATH/exported-artifacts/

mv $RHV_BUILD/*tar.gz $ROOT_PATH/exported-artifacts/

COLLECTION_DIR="/usr/local/share/ansible/collections/ansible_collections/ovirt/ovirt"
mkdir -p $COLLECTION_DIR
cp -r $OVIRT_BUILD/* $COLLECTION_DIR
cd $COLLECTION_DIR

pip3 install rstcheck antsibull-changelog ansible-lint

ansible-test sanity
/usr/local/bin/antsibull-changelog lint
/usr/local/bin/ansible-lint roles/* -x 204

cd $ROOT_PATH
