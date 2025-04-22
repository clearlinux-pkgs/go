#
# This is still slightly messy in that it installs one monolithic main package
# but then again the upstream is rather messy in this regard
#

Name     : go
Version  : 1.24.2
Release  : 91
URL      : https://go.dev/dl/go1.24.2.src.tar.gz
Source0  : https://go.dev/dl/go1.24.2.src.tar.gz
Summary  : No detailed summary available
Group    : Development/Tools
License  : BSD-3-Clause
Requires: glibc-staticdev
BuildRequires: netbase
BuildRequires: bison flex gmp-dev pcre-dev glibc-staticdev
BuildRequires: hostname go sqlite-autoconf-dev tiff-dev

Patch1: 0001-stateless-services-file-path-fix.patch
Patch2: 0002-Fix-os_test-in-stateless.patch
Patch3: 0003-golang-stateless-fix-etc-services-path-in-net.patch
Patch4: 0004-Don-t-use-ntq.patch
Patch5: 0005-Prepend-Clear-Linux-trust-store-location.patch

# don't strip, these are not ordinary object files
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

# solve meta dependency on libc.so.6
%define _use_internal_dependency_generator 0
%define __find_requires %{nil}
%global __spec_install_post /usr/lib/rpm/check-rpaths   /usr/lib/rpm/check-buildroot  \
  /usr/lib/rpm/brp-compress

# workaround to not generate go-abi package since we don't generate abifiles.list.
%define abi_package %{nil}

%description
This is the source code repository for the Go programming language.
For documentation about how to install and use Go,
visit http://golang.org/ or load doc/install-source.html
in your web browser.

%prep
%setup -q -n go
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%patch -P 4 -p1
%patch -P 5 -p1

%build
unset CLEAR_DEBUG_TERSE
export CFLAGS="$CFLAGS -g2"
pushd src
export GOROOT_FINAL=/usr/lib/golang
export GOROOT_BOOTSTRAP=/usr/lib/golang
export GO_LDFLAGS="-buildmode=pie"
./make.bash
popd

# Shared libraries
GOROOT=$(pwd) PATH=$(pwd)/bin:$PATH go install -buildmode=shared std

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/lib/golang
mkdir -p %{buildroot}/usr/bin
cp -a *  %{buildroot}/usr/lib/golang
ln -s ../lib/golang/bin/go %{buildroot}/usr/bin/go
ln -s ../lib/golang/bin/gofmt %{buildroot}/usr/bin/gofmt
rm -f %{buildroot}/usr/lib/golang/src/debug/elf/testdata/libtiffxx.so_

%files
%defattr(-,root,root,-)
/usr/lib/golang/*
/usr/bin/go
/usr/bin/gofmt
