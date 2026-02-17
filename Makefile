all: build
build:
	rpmbuild -bb --define "_topdir $(shell pwd)" SPECS/perlcompat-attr.spec

clean:
	rm -rf BUILD/* RPMS/* SRPMS/*
