#!/bin/bash -xe

ROOT_PATH="$PWD"
BUILD_ROOT_PATH="/tmp"

# Remove any previous artifacts
rm -rf "$BUILD_ROOT_PATH/ansible_collections"
rm -f "$BUILD_ROOT_PATH"/*tar.gz

# Create exported-artifacts dir
[[ -d exported-artifacts ]] || mkdir "$ROOT_PATH/exported-artifacts/"

# Create builds
./build.sh build ovirt "$BUILD_ROOT_PATH"
./build.sh build rhv "$BUILD_ROOT_PATH"

OVIRT_BUILD="$BUILD_ROOT_PATH/ansible_collections/ovirt/ovirt"
RHV_BUILD="$BUILD_ROOT_PATH/ansible_collections/redhat/rhv"

cd "$OVIRT_BUILD"

# Create the src.rpm
rpmbuild \
    -D "_srcrpmdir $BUILD_ROOT_PATH/output" \
    -D "_topmdir $BUILD_ROOT_PATH/rpmbuild" \
    -ts ./*.gz

# Remove the tarball so it will not be included in galaxy build
mv ./*.gz "$ROOT_PATH/exported-artifacts/"

# Overwrite github README with dynamic
mv ./README.md.in ./README.md

# Create tar for galaxy
ansible-galaxy collection build

# Create the rpms
rpmbuild \
    -D "_rpmdir $BUILD_ROOT_PATH/output" \
    -D "_topmdir $BUILD_ROOT_PATH/rpmbuild" \
    --rebuild "$BUILD_ROOT_PATH"/output/*.src.rpm

cd "$RHV_BUILD"

# Remove the tarball so it will not be included in automation hub build
rm -rf ./*.gz

# Overwrite github README with dynamic
mv ./README.md.in ./README.md

# create tar for automation hub
ansible-galaxy collection build

# Store any relevant artifacts in exported-artifacts for the ci system to
# archive
find "$BUILD_ROOT_PATH/output" -iname \*rpm -exec mv "{}" "$ROOT_PATH/exported-artifacts/" \;

# Export build for Ansible Galaxy
mv "$OVIRT_BUILD"/*tar.gz "$ROOT_PATH/exported-artifacts/"
# Export build for Automation Hub
mv "$RHV_BUILD"/*tar.gz "$ROOT_PATH/exported-artifacts/"

COLLECTION_DIR="/usr/local/share/ansible/collections/ansible_collections/ovirt/ovirt"
export ANSIBLE_LIBRARY="$COLLECTION_DIR/plugins/modules"
mkdir -p $COLLECTION_DIR
cp -r "$OVIRT_BUILD"/* "$COLLECTION_DIR"
cd "$COLLECTION_DIR"

ansible-test sanity --docker
antsibull-changelog lint -v
# 204 - lines should be no longer than 160 chars
ansible-lint roles/* -x 204

cd "$ROOT_PATH"

# If PR changed something in ./plugins or ./roles it is required to have changelog
if [[ $(git diff --quiet HEAD^ ./plugins ./roles)$? -eq 1 && $(git diff --quiet HEAD^ ./changelogs)$? -eq 0 ]]; then
    echo "ERROR: Please add changelog.";
    exit 1;
fi
