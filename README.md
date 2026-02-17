# perlcompat.attr spurious perl-libs dependency

## Summary

On RHEL 10 (and Fedora 38+), customizing `%_bindir` in a spec file causes
`perl-libs` to be silently added as a Requires to packages that have no
relation to Perl.

## Affected packages

- `perl-srpm-macros` (root cause: `%__perl` defined as `%{_bindir}/perl`)
- `perl-generators` (no guard in `perlcompat.attr` for empty macro values)

## Reproduction steps

### almalinux 10.1

```
$ docker run --rm -it almalinux:10.1-20260129 /bin/bash
```

```bash
# Preliminary work
dnf install -y rpm-build make git perl-generators perl-srpm-macros
git clone https://github.com/t2y/issue-perlcompat-attr-macro.git
cd issue-perlcompat-attr-macro/
```

```bash
# 1. Build the reproducer package
make

# 2. Check for perl-related dependencies
rpm -qpR RPMS/x86_64/perlcompat-attr-1.0-1.el10.x86_64.rpm | grep perl

# Expected: (no output)
# Actual:   perl-libs
```

## Root cause chain

```
spec file:        %define _bindir /opt/custom/bin
                        |
macros.perl-srpm: %__perl %{_bindir}/perl
                        |
                  %__perl = /opt/custom/bin/perl  (does not exist)
                        |
macros.perl:      %perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; ...)
                        |
                  command fails -> empty string
                        |
perlcompat.attr:  %__perlcompat_path ^(|||)/.+
                        |
                  regex matches ALL files starting with /
                        |
                  files not ending in .so -> else branch -> prints "perl-libs"
```

## Workarounds

In the affected spec file, add one of the following:

```spec
# Option A: Fix %__perl to point to system perl (recommended)
%define __perl /usr/bin/perl

# Option B: Disable perlcompat dependency generator
%global __perlcompat_requires %{nil}
```
