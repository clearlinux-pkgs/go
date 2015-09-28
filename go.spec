#
# This is still slightly messy in that it installs one monolithic main package
# but then again the upstream is rather messy in this regard
#

Name     : go
Version  : 1.5.1
Release  : 21
URL      : https://storage.googleapis.com/golang/go1.5.1.src.tar.gz
Source0  : https://storage.googleapis.com/golang/go1.5.1.src.tar.gz
Summary  : No detailed summary available
Group    : Development/Tools
License  : BSD-3-Clause
Requires: glibc-staticdev
BuildRequires: netbase
BuildRequires: bison flex gmp-dev pcre-dev glibc-staticdev
BuildRequires: hostname gcc-go

Patch1: stateless-test.patch
Patch2: stateless-cacerts.patch
Patch3: 0001-Fix-os_test-in-stateless.patch
Patch4: stateless-port.patch
Patch5: unshare-permissions.patch
Patch6: skip-gccgo-tests.patch
#Patch5: 655ebde9.diff

# don't strip, these are not ordinary object files
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

# solve meta dependency on libc.so.6
%define _use_internal_dependency_generator 0
%define __find_requires %{nil}
%global __spec_install_post /usr/lib/rpm/check-rpaths   /usr/lib/rpm/check-buildroot  \
  /usr/lib/rpm/brp-compress

%description
This is the source code repository for the Go programming language.
For documentation about how to install and use Go,
visit http://golang.org/ or load doc/install-source.html
in your web browser.

%prep
%setup -q -n go
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
cd src
export GOROOT_FINAL=/usr/lib/golang
export GOROOT_BOOTSTRAP=/usr/libexec/gccgo
bash ./all.bash

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/lib/golang
mkdir -p %{buildroot}/usr/bin
cp -a *  %{buildroot}/usr/lib/golang
ln -s /usr/lib/golang/bin/go %{buildroot}/usr/bin/go
ln -s /usr/lib/golang/bin/gofmt %{buildroot}/usr/bin/gofmt

%files
%defattr(-,root,root,-)
/usr/lib/golang/*
/usr/bin/go
/usr/bin/gofmt
