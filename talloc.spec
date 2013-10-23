%define	tallocmajor	2
%define	libtalloc	%mklibname talloc %{tallocmajor}
%define	tallocdev	%mklibname -d talloc
%define	libpytalloc	%mklibname pytalloc-util %{tallocmajor}
%define	libpytallocdev	%mklibname -d pytalloc-util
%define beta		%nil
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
Version:	2.0.8
URL:		http://talloc.samba.org
Source0:	http://talloc.samba.org/ftp/talloc/talloc-%{version}.tar.gz
%if "%beta" != ""
Release:	0.%beta.1
%else
Release:	5
Source1:	http://talloc.samba.org/ftp/talloc/talloc-%{version}.tar.asc
Source2:	samba-bugs.asc
%endif
License:	GPLv3
# tallocversion was not used when in samba4, so it was 4.0.0
Epoch:		1
Summary:	Library implementing Samba's memory allocator
Group:		System/Libraries
BuildRequires:	acl-devel xsltproc docbook-style-xsl
BuildRequires:	python-devel

%description
Library implementing Samba's memory allocator

%package -n	%{libtalloc}
Group:		System/Libraries
Summary:	Library implementing Samba's memory allocator

%description -n	%{libtalloc}
Library implementing Samba's memory allocator

%package -n	%{tallocdev}
Group:		Development/C
Summary:	Library implementing Samba's memory allocator
Provides:	talloc-devel = %{EVRD}
Requires:	%{libtalloc} = %{EVRD}
BuildRequires:	swig

%description -n	%{tallocdev}
Library implementing Samba's memory allocator

%package -n	python-talloc
Group:		Development/Python
Summary:	Python module for Samba's talloc memory allocator

%description -n	python-talloc
Python module for Samba's talloc memory allocator

%package -n	%{libpytalloc}
Group:		Development/C
Summary:	Utility functions for using talloc objects with Python

%description -n	%{libpytalloc}
Utility functions for using talloc objects with Python

%package -n	%{libpytallocdev}
Group:		Development/C
Summary:	Utility functions for using talloc objects with Python
Requires:	%{libpytalloc} = %{EVRD}
Provides:	pytalloc-util-devel = %{version}-%{release}

%description -n %{libpytallocdev}
Utility functions for using talloc objects with Python

%prep
%if "%beta" == ""
echo "Death to Bush! %beta"
#Try and validate signatures on source:
VERIFYSOURCE=%{SOURCE0}
VERIFYSOURCE=${VERIFYSOURCE%%.gz}
gzip -dc %{SOURCE0} > $VERIFYSOURCE

%check_sig %{SOURCE2} %{SOURCE1} $VERIFYSOURCE

rm -f $VERIFYSOURCE
%endif

%setup -q
chmod +r -R .

%build
%configure2_5x	--disable-rpath
%make

%install
%makeinstall_std
chmod +x %{buildroot}{%{_libdir}/lib*.so.%{tallocmajor}*,%{py_platsitedir}/talloc.so}

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
%{py_platsitedir}/talloc.so

%files -n %{libpytalloc}
%{_libdir}/libpytalloc-util.so.%{tallocmajor}*

%files -n %{libpytallocdev}
%{_includedir}/pytalloc.h
%{_libdir}/libpytalloc-util.so
%{_libdir}/pkgconfig/pytalloc-util.pc
