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

OVIRT_BUILD="$BUILD_ROOT_PATH/ansible_collections/ovirt/ovirt"

cd "$OVIRT_BUILD"

# Create the src.rpm
rpmbuild \
    -D "_srcrpmdir $BUILD_ROOT_PATH/output" \
    -D "_topmdir $BUILD_ROOT_PATH/rpmbuild" \
    -ts ./*.gz

# Remove the tarball so it will not be included in galaxy build
mv ./*.gz "$ROOT_PATH/exported-artifacts/"

# Overwrite github README with dynamic
mv ./COLLECTION_README.md ./README.md

# Create tar for galaxy
ansible-galaxy collection build

# Create the rpms
rpmbuild \
    -D "_rpmdir $BUILD_ROOT_PATH/output" \
    -D "_topmdir $BUILD_ROOT_PATH/rpmbuild" \
    --rebuild "$BUILD_ROOT_PATH"/output/*.src.rpm

# Store any relevant artifacts in exported-artifacts for the ci system to
# archive
find "$BUILD_ROOT_PATH/output" -iname \*rpm -exec mv "{}" "$ROOT_PATH/exported-artifacts/" \;

# Export build for Ansible Galaxy
mv "$OVIRT_BUILD"/*tar.gz "$ROOT_PATH/exported-artifacts/"

COLLECTION_DIR="/usr/local/share/ansible/collections/ansible_collections/ovirt/ovirt"
export ANSIBLE_LIBRARY="$COLLECTION_DIR/plugins/modules"
mkdir -p $COLLECTION_DIR
cp -r "$OVIRT_BUILD"/* "$COLLECTION_DIR"
cd "$COLLECTION_DIR"

antsibull-changelog lint -v
#skip linting, done in separate github workflow
#ansible-lint roles/*

cd "$ROOT_PATH"

# If PR changed something in ./plugins or ./roles it is required to have changelog
if [[ $(git diff --quiet HEAD^ ./plugins ./roles)$? -eq 1 && $(git diff --quiet HEAD^ ./changelogs)$? -eq 0 ]]; then
    echo "ERROR: Please add changelog.";
    exit 1;
fi
