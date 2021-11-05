.PHONY: srpm

srpm:
	mkdir -p tmp.repos/SOURCES tmp.build
	./build.sh build ovirt tmp.build
	cp tmp.build/ansible_collections/ovirt/ovirt/*.tar.gz ./tmp.repos/SOURCES/
	rpmbuild \
		-D "_topdir tmp.repos" \
		-bs tmp.build/ansible_collections/ovirt/ovirt/ovirt-ansible-collection.spec
	cp tmp.repos/SRPMS/*.src.rpm $(outdir)