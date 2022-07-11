# For python module
%global _disable_ld_no_undefined 1

%define tallocmajor 2
%define libtalloc %mklibname talloc %{tallocmajor}
%define tallocdev %mklibname -d talloc
%define libpytallocdev %mklibname -d pytalloc-util
%define beta %nil
%define check_sig() export GNUPGHOME=%{_tmppath}/rpm-gpghome \
if [ -d "$GNUPGHOME" ] \
then echo "Error, GNUPGHOME $GNUPGHOME exists, remove it and try again"; exit 1 \
fi \
install -d -m700 $GNUPGHOME \
gpg --import %{1} \
gpg --trust-model always --verify %{2} \
rm -Rf $GNUPGHOME \

# beta versions are extracted from the samba4 source using
# mkdir -p talloc-2.0.8/lib
# cp -a lib/talloc/* talloc-2.0.8/
# cp -a lib/replace talloc-2.0.8/lib/
# cp -a buildtools talloc-2.0.8/
# tar cf talloc-2.0.8.tar talloc-2.0.8

Name:		talloc
Version:	2.3.4
URL:		https://talloc.samba.org
Source0:	https://talloc.samba.org/ftp/talloc/talloc-%{version}.tar.gz
%if "%beta" != ""
Release:	1
%else
Release:	1
Source1:	https://talloc.samba.org/ftp/talloc/talloc-%{version}.tar.asc
Source2:	samba-bugs.asc
%endif
License:	GPLv3
Summary:	Library implementing Samba's memory allocator
Group:		System/Libraries
Patch0: 0001-add-mock-disable-static-option.patch
BuildRequires:	pkgconfig(libacl)
BuildRequires:	pkgconfig(libattr)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(libnsl)
BuildRequires:	pkgconfig(libcrypt)
BuildRequires:	libaio-devel
BuildRequires:	xsltproc
BuildRequires:	docbook-style-xsl
BuildRequires:	pkgconfig(python)
BuildRequires:	python3dist(setuptools)

%description
Library implementing Samba's memory allocator.

%package -n %{libtalloc}
Group:		System/Libraries
Summary:	Library implementing Samba's memory allocator

%description -n %{libtalloc}
Library implementing Samba's memory allocator.

%package -n %{tallocdev}
Group:		Development/C
Summary:	Library implementing Samba's memory allocator
Provides:	talloc-devel = %{EVRD}
Requires:	%{libtalloc} = %{EVRD}
BuildRequires:	swig

%description -n %{tallocdev}
Library implementing Samba's memory allocator.

%package -n python-talloc
Group:		Development/Python
Summary:	Python module for Samba's talloc memory allocator
Obsoletes:	python2-talloc < %{EVRD}

%description -n python-talloc
Python module for Samba's talloc memory allocator.

%package -n %{libpytallocdev}
Group:		Development/C
Summary:	Utility functions for using talloc objects with Python
Requires:	python-talloc = %{EVRD}
Requires:	%{tallocdev} = %{EVRD}
Provides:	pytalloc-util-devel = %{version}-%{release}

%description -n %{libpytallocdev}
Utility functions for using talloc objects with Python.

%prep
%if "%beta" == ""
#Try and validate signatures on source:
VERIFYSOURCE=%{SOURCE0}
VERIFYSOURCE=${VERIFYSOURCE%%.gz}
gzip -dc %{SOURCE0} > $VERIFYSOURCE

%check_sig %{SOURCE2} %{SOURCE1} $VERIFYSOURCE

rm -f $VERIFYSOURCE
%endif

%autosetup -p1
chmod +r -R .

%build
%setup_compile_flags
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --disable-rpath \
    --disable-rpath-install \
    --bundled-libraries=NONE \
    --builtin-libraries=replace \
    --disable-silent-rules

%make_build V=1

%install
%make_install
chmod +x %{buildroot}%{_libdir}/lib*.so.%{tallocmajor}*

%files -n %{libtalloc}
%{_libdir}/libtalloc.so.%{tallocmajor}*

%files -n %{tallocdev}
%{_libdir}/libtalloc.so
#{_libdir}/libtalloc.a
%{_includedir}/talloc.h
%{_libdir}/pkgconfig/talloc.pc
%{_mandir}/man3/talloc*
#{_datadir}/swig/*/talloc.i

%files -n python-talloc
%{_libdir}/libpytalloc*python*.so*
%{py3_platsitedir}/talloc.cpython*.so

%files -n %{libpytallocdev}
%{_includedir}/pytalloc.h
%{_libdir}/libpytalloc-util.cpython*.so
%{_libdir}/pkgconfig/pytalloc-util.cpython-*.pc
