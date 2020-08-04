#!/bin/bash

VERSION="1.1.3"
MILESTONE=master
RPM_RELEASE="0.1.$MILESTONE.$(date -u +%Y%m%d%H%M%S)"

BUILD_TYPE=$2
BUILD_PATH=$3

if [[ $BUILD_TYPE = "rhv" ]]; then
COLLECTION_NAMESPACE="redhat"
COLLECTION_NAME="rhv"
else
COLLECTION_NAMESPACE="ovirt"
COLLECTION_NAME="ovirt"
fi
PACKAGE_NAME="ovirt-ansible-collection"
PREFIX=/usr/local
DATAROOT_DIR=$PREFIX/share
COLLECTIONS_DATAROOT_DIR=$DATAROOT_DIR/ansible/collections/ansible_collections
DOC_DIR=$DATAROOT_DIR/doc
PKG_DATA_DIR=${PKG_DATA_DIR:-$COLLECTIONS_DATAROOT_DIR/$COLLECTION_NAMESPACE/$COLLECTION_NAME}
PKG_DATA_DIR_ORIG=${PKG_DATA_DIR_ORIG:-$PKG_DATA_DIR}
PKG_DOC_DIR=${PKG_DOC_DIR:-$DOC_DIR/$PACKAGE_NAME}

RPM_VERSION=$VERSION
PACKAGE_VERSION=$VERSION
[ -n "$MILESTONE" ] && PACKAGE_VERSION+="_$MILESTONE"
DISPLAY_VERSION=$PACKAGE$VERSION

TARBALL="$PACKAGE_NAME-$PACKAGE_VERSION.tar.gz"

dist() {
  echo "Creating tar archive '$TARBALL' ... "
  sed \
   -e "s|@RPM_VERSION@|$RPM_VERSION|g" \
   -e "s|@RPM_RELEASE@|$RPM_RELEASE|g" \
   -e "s|@PACKAGE_NAME@|$PACKAGE_NAME|g" \
   -e "s|@PACKAGE_VERSION@|$PACKAGE_VERSION|g" \
   < ovirt-ansible-collection.spec.in > ovirt-ansible-collection.spec

  git ls-files | tar --files-from /proc/self/fd/0 -czf "$TARBALL" ovirt-ansible-collection.spec
  echo "tar archive '$TARBALL' created."
}

install() {
  echo "Installing data..."
  mkdir -p $PKG_DATA_DIR
  mkdir -p $PKG_DOC_DIR

  cp -pR plugins/ $PKG_DATA_DIR

  echo "Installation done."
}

rename() {
  echo "Renaming @NAMESPACE@ to $COLLECTION_NAMESPACE and @NAME@ to $COLLECTION_NAME"
  for file in $(git ls-files)
  do
    sed -i -e "s/@NAMESPACE@/$COLLECTION_NAMESPACE/g" -e "s/@NAME@/$COLLECTION_NAME/g" $file
  done
}

build() {
  if [[ -d $BUILD_PATH ]]; then
    echo "The copying files to $BUILD_PATH"
    cp -a ./ $BUILD_PATH
    cd $BUILD_PATH
    rename
    dist
  else
    echo "The BUILD_PATH was not specified!"
  fi
}

$1
