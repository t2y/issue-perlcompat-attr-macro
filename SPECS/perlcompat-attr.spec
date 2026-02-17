Name:    perlcompat-attr
Version: 1.0
Release: 1%{?dist}
Summary: Reproducer for perlcompat.attr spurious perl-libs dependency
License: Apache-2.0

# This is the trigger: customizing _bindir causes %__perl to resolve
# to /opt/custom/bin/perl (via macros.perl-srpm: %__perl %{_bindir}/perl)
# which does not exist, breaking all perl macro expansions.
%define _bindir /opt/custom/bin

%description
This package demonstrates a bug where customizing %%_bindir causes
perl-libs to be added as a spurious dependency to packages that have
no relation to Perl.

%install
mkdir -p %{buildroot}%{_bindir}
# Create a trivial shell script (not Perl-related at all)
cat > %{buildroot}%{_bindir}/hello <<'EOF'
#!/bin/sh
echo "Hello, world!"
EOF
chmod 755 %{buildroot}%{_bindir}/hello

%files
%{_bindir}/hello
