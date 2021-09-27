#!/bin/bash

VERSION="1.6.4"
MILESTONE=
RPM_RELEASE="1"

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
PKG_DATA_DIR=${PKG_DATA_DIR:-$COLLECTIONS_DATAROOT_DIR}
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

  find ./* -not -name '*.spec' -type f | tar --files-from /proc/self/fd/0 -czf "$TARBALL" ovirt-ansible-collection.spec
  echo "tar archive '$TARBALL' created."
}

install() {
  echo "Installing data..."
  mkdir -p $PKG_DATA_DIR/$COLLECTION_NAMESPACE/$COLLECTION_NAME
  mkdir -p $PKG_DOC_DIR

  cp -pR plugins/ roles/ $PKG_DATA_DIR/$COLLECTION_NAMESPACE/$COLLECTION_NAME

  if [[ $BUILD_TYPE = "rhv" ]]; then
    echo "Creating link to ovirt.ovirt"
    mkdir -p $PKG_DATA_DIR/ovirt
    ln -f -s $PKG_DATA_DIR_ORIG/redhat/rhv $PKG_DATA_DIR/ovirt/ovirt
  fi
  echo "Installation done."
}

rename() {
  echo "Renaming @NAMESPACE@ to $COLLECTION_NAMESPACE and @NAME@ to $COLLECTION_NAME"
  for file in $(find ./* -type f)
  do
    sed -i -e "s/@NAMESPACE@/$COLLECTION_NAMESPACE/g" -e "s/@NAME@/$COLLECTION_NAME/g" $file
  done
}

build() {
  if [[ $BUILD_PATH ]]; then
    BUILD_PATH=$BUILD_PATH/ansible_collections/$COLLECTION_NAMESPACE/$COLLECTION_NAME/
    mkdir -p $BUILD_PATH
    echo "The copying files to $BUILD_PATH"
    cp --parents $(git ls-files) $BUILD_PATH
    cd $BUILD_PATH
    rename
    dist
  fi
}

$1
