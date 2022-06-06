#!/bin/bash -xe

ROOT_PATH=$PWD

# Remove any previous artifacts
rm -rf "$ROOT_PATH/ansible_collections"
rm -f "$ROOT_PATH/*tar.gz"

# Create builds

./build.sh build ovirt "$ROOT_PATH"
./build.sh build rhv "$ROOT_PATH"

OVIRT_BUILD="$ROOT_PATH/ansible_collections/ovirt/ovirt/"
RHV_BUILD="$ROOT_PATH/ansible_collections/redhat/rhv/"

cd "$OVIRT_BUILD"

# Create the src.rpm
rpmbuild \
    -D "_srcrpmdir $ROOT_PATH/output" \
    -D "_topmdir $ROOT_PATH/rpmbuild" \
    -ts ./*.gz

# Create exported-artifacts dir
[[ -d exported-artifacts ]] || mkdir "$ROOT_PATH/exported-artifacts/"

# Remove the tarball so it will not be included in galaxy build
mv ./*.gz "$ROOT_PATH/exported-artifacts/"

# Overwrite github README with dynamic
mv ./README.md.in ./README.md

# Create tar for galaxy
ansible-galaxy collection build

# Create the rpms
rpmbuild \
    -D "_rpmdir $ROOT_PATH/output" \
    -D "_topmdir $ROOT_PATH/rpmbuild" \
    --rebuild "$ROOT_PATH"/output/*.src.rpm

cd "$RHV_BUILD"

# Remove the tarball so it will not be included in automation hub build
rm -rf ./*.gz

# Overwrite github README with dynamic
mv ./README.md.in ./README.md

# create tar for automation hub
ansible-galaxy collection build

# Store any relevant artifacts in exported-artifacts for the ci system to
# archive
find "$ROOT_PATH/output" -iname \*rpm -exec mv "{}" "$ROOT_PATH/exported-artifacts/" \;

# Export build for Ansible Galaxy
mv "$OVIRT_BUILD/*tar.gz" "$ROOT_PATH/exported-artifacts/"
# Export build for Automation Hub
mv "$RHV_BUILD/*tar.gz" "$ROOT_PATH/exported-artifacts/"

COLLECTION_DIR="/usr/local/share/ansible/collections/ansible_collections/ovirt/ovirt"
export ANSIBLE_LIBRARY="$COLLECTION_DIR/plugins/modules"
mkdir -p $COLLECTION_DIR
cp -r "$OVIRT_BUILD/*" "$COLLECTION_DIR"
cd "$COLLECTION_DIR"

# The sanity import test failed with error. (https://github.com/ansible/ansible/issues/76473)
ansible-test sanity --skip-test import
antsibull-changelog lint
# 204 - lines should be no longer than 160 chars
ansible-lint roles/* -x 204

cd "$ROOT_PATH"

# If PR changed something in ./plugins or ./roles it is required to have changelog
if [[ $(git diff --quiet HEAD^ ./plugins ./roles)$? -eq 1 && $(git diff --quiet HEAD^ ./changelogs)$? -eq 0 ]]; then
        echo "ERROR: Please add changelog.";
        exit 1;
fi
