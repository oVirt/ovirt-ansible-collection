#!/bin/bash

# remove any previous artifacts
rm -rf output
rm -f ./*tar.gz

# Get the tarball
./build.sh dist

# create the src.rpm
rpmbuild \
    -D "_srcrpmdir $PWD/output" \
    -D "_topmdir $PWD/rpmbuild" \
    -ts ./*.gz

# install any build requirements
yum-builddep output/*src.rpm

# create the rpms
rpmbuild \
    -D "_rpmdir $PWD/output" \
    -D "_topmdir $PWD/rpmbuild" \
    --rebuild output/*.src.rpm

[[ -d exported-artifacts ]] || mkdir -p exported-artifacts
find output -iname \*rpm -exec mv "{}" exported-artifacts/ \;
mv *.tar.gz exported-artifacts

COLLECTION_DIR="/usr/local/share/ansible/collections/ansible_collections/ovirt/ovirt"
mkdir -p $COLLECTION_DIR
cp -r $PWD/* $COLLECTION_DIR
cd $COLLECTION_DIR
ansible-test sanity
