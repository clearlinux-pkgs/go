#
# This is still slightly messy in that it installs one monolithic main package
# but then again the upstream is rather messy in this regard
#

Name     : go
Version  : 1.6.3
Release  : 28
URL      : https://storage.googleapis.com/golang/go1.6.3.src.tar.gz
Source0  : https://storage.googleapis.com/golang/go1.6.3.src.tar.gz
Summary  : No detailed summary available
Group    : Development/Tools
License  : BSD-3-Clause
Requires: glibc-staticdev
BuildRequires: netbase
BuildRequires: bison flex gmp-dev pcre-dev glibc-staticdev
BuildRequires: hostname go sqlite-autoconf-dev

Requires: /usr/bin/gcc

Patch1: 0001-stateless-fix-etc-services-path.patch
Patch2: 0002-stateless-fix-cacerts-path.patch
Patch3: 0003-Fix-os_test-in-stateless.patch
Patch4: 0004-stateless-fix-etc-services-path-in-net.patch
Patch5: nontq.patch

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

%build
pushd src
export GOROOT_FINAL=/usr/lib/golang
export GOROOT_BOOTSTRAP=/usr/lib/golang
bash ./all.bash
popd

# Shared libraries
GOROOT=$(pwd) PATH=$(pwd)/bin:$PATH go install -buildmode=shared std

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
