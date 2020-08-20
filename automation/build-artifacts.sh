#!/bin/bash -xe

ROOT_PATH=$PWD

# remove any previous artifacts
rm -rf ../ovirt-build ../rhv-build
rm -f ./*tar.gz

# Create paths for builds
mkdir -p ../ovirt-build ../rhv-build
# Create builds

./build.sh build ovirt ../ovirt-build
./build.sh build rhv ../rhv-build

cd ../ovirt-build
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

cd ../rhv-build

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

# Store any relevant artifacts in exported-artifacts for the ci system to
# archive
[[ -d exported-artifacts ]] || mkdir -p $ROOT_PATH/exported-artifacts $ROOT_PATH/exported-artifacts/ovirt-build $ROOT_PATH/exported-artifacts/rhv-build

find ../ovirt-build/output -iname \*rpm -exec mv "{}" $ROOT_PATH/exported-artifacts/ovirt-build \;
mv ../ovirt-build/*tar.gz $ROOT_PATH/exported-artifacts/ovirt-build

find ../rhv-build/output -iname \*rpm -exec mv "{}" $ROOT_PATH/exported-artifacts/rhv-build \;
mv ../rhv-build/*tar.gz $ROOT_PATH/exported-artifacts/rhv-build

COLLECTION_DIR="/usr/local/share/ansible/collections/ansible_collections/ovirt/ovirt"
mkdir -p $COLLECTION_DIR
cp -r ../ovirt-build/* $COLLECTION_DIR
cd $COLLECTION_DIR

pip3 install rstcheck antsibull-changelog

ansible-test sanity
/usr/local/bin/antsibull-changelog lint

cd $ROOT_PATH
