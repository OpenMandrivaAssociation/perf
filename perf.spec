# for sure, one of the ugliest packages ever made:

# q: why not just depend on kernel-source-latest?
# a: we would never know exactly what version of perf we are using
# (--version does not work so far)

%define kver 2.6.33-1mnb

%define pver %(echo %kver | tr - .)

Name: perf
Version: %pver
Release: %mkrel 2
License: GPLv2
Summary: Performance monitor for the Linux kernel
URL: http://www.kernel.org/
Group: Monitoring
Buildrequires: gcc
Buildrequires: libelfutils-devel
Buildrequires: kernel-source-%kver
Buildrequires: asciidoc
Buildrequires: xmlto
Buildrequires: docbook-dtd45-xml
BuildRoot: %_tmppath/%name-%version-root

%description
Performance counters for Linux are are a new kernel-based subsystem that
provide a framework for all things performance analysis. It covers hardware
level (CPU/PMU, Performance Monitoring Unit) features and software features
(software counters, tracepoints) as well.

This package provides the "perf" tool, distributed with the Linux kernel
source.

%clean
rm -rf $RPM_BUILD_ROOT

%prep
rm -rf %name-%version-%release
mkdir %name-%version-%release
cd %name-%version-%release
# TODO: patch perf to use paths at /usr/src/linux directly?
cp -af %_usrsrc/linux/ .

%build
cd %name-%version-%release
cd linux/tools/perf
make
pushd Documentation
make man
popd

%install
rm -rf %buildroot
cd %name-%version-%release
install -d %buildroot/%_bindir
install -m 755 linux/tools/perf/perf %buildroot/%_bindir/perf
# doc
install -d %buildroot/%_mandir/man1
install linux/tools/perf/Documentation/*.1 %buildroot/%_mandir/man1/
install -d %buildroot/%_datadir/doc/%name
install linux/tools/perf/Documentation/examples.txt %buildroot/%_datadir/doc/%name

%files
%defattr(-,root,root)
%_bindir/perf
%_mandir/man1/*
%_datadir/doc/%name/*.txt
