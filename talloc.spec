%define tallocmajor 2
%define libtalloc %mklibname talloc %tallocmajor
%define tallocdevel %mklibname -d talloc
%define  epoch 1

Name: talloc
Version: 2.0.1
Release: %mkrel 2
URL: http://talloc.samba.org
Source: http://talloc.samba.org/ftp/talloc/talloc-%{version}.tar.gz
#Source1: http://talloc.samba.org/ftp/talloc/talloc-%{version}.tar.gz.asc
License: GPLv3
# tallocversion was not used when in samba4, so it was 4.0.0
Epoch: %epoch
Summary: Library implementing Samba's memory allocator
Group: System/Libraries
BuildRequires: acl-devel xsltproc docbook-style-xsl
BuildRoot: %{_tmppath}/%{name}-root

%description
Library implementing Samba's memory allocator

%package -n %libtalloc
Group: System/Libraries
Summary: Library implementing Samba's memory allocator

%description -n %libtalloc
Library implementing Samba's memory allocator

%package -n %tallocdevel
Group: Development/C
Summary: Library implementing Samba's memory allocator
Provides: talloc-devel = %epoch:%{version}-%{release}
Requires: %libtalloc = %epoch:%{version}-%{release}
BuildRequires: swig

%description -n %tallocdevel
Library implementing Samba's memory allocator

%prep
%setup -q
perl -pi -e 's,http://docbook.sourceforge.net/release/xsl/current/,/usr/share/sgml/docbook/xsl-stylesheets/,g' rules.mk

%build
%configure
%make

%install
rm -Rf %{buildroot}
%makeinstall_std
ln -s libtalloc.so.%{tallocmajor} %{buildroot}/%{_libdir}/libtalloc.so

%files -n %libtalloc
%defattr(-,root,root)
%{_libdir}/libtalloc.so.%{tallocmajor}*

%files -n %tallocdevel
%defattr(-,root,root)
%{_libdir}/libtalloc.so
%{_libdir}/libtalloc.a
%{_includedir}/talloc.h
%{_libdir}/pkgconfig/talloc.pc
%{_mandir}/man3/talloc*
%{_datadir}/swig/*/talloc.i
