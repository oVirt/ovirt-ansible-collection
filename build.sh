#!/bin/bash -eux

VERSION="3.2.3"
RPM_VERSION=${RPM_VERSION:-${VERSION}}
RPM_RELEASE=${PACKAGE_RPM_RELEASE:-0.master}

BUILD_PATH=$3

COLLECTION_NAMESPACE="ovirt"
COLLECTION_NAME="ovirt"
PACKAGE_NAME="ovirt-ansible-collection"
PREFIX=/usr/local
DATAROOT_DIR=$PREFIX/share
COLLECTIONS_DATAROOT_DIR=$DATAROOT_DIR/ansible/collections/ansible_collections
DOC_DIR=$DATAROOT_DIR/doc
PKG_DATA_DIR=${PKG_DATA_DIR:-$COLLECTIONS_DATAROOT_DIR}
PKG_DATA_DIR_ORIG=${PKG_DATA_DIR_ORIG:-$PKG_DATA_DIR}
PKG_DOC_DIR=${PKG_DOC_DIR:-$DOC_DIR/$PACKAGE_NAME}

PACKAGE_VERSION=$VERSION

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
  mkdir -p "$PKG_DATA_DIR/$COLLECTION_NAMESPACE/$COLLECTION_NAME"
  mkdir -p "$PKG_DOC_DIR"

  cp -pR plugins/ roles/ "$PKG_DATA_DIR/$COLLECTION_NAMESPACE/$COLLECTION_NAME"

  echo "Installation done."
}

build() {
  if [[ $BUILD_PATH ]]; then
    BUILD_PATH="$BUILD_PATH/ansible_collections/$COLLECTION_NAMESPACE/$COLLECTION_NAME/"
    mkdir -p "$BUILD_PATH"
    echo "Copying files to $BUILD_PATH"
    git config --global --add safe.directory "$(pwd)"
    git archive --format=tar HEAD | (cd "$BUILD_PATH" && tar xf -)
    cd "$BUILD_PATH"
    dist
  fi
}

$1
