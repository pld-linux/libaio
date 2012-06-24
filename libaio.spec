Summary:	Linux-native asynchronous I/O access library
Summary(pl):	Biblioteka natywnego dla Linuksa asynchronicznego dost�pu do wej�cia/wyj�cia
Name:		libaio
Version:	0.3.104
Release:	1
License:	LGPL v2+
Group:		Libraries
# http://download.fedora.redhat.com/pub/fedora/linux/core/development/SRPMS/
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	2a4a17ed8f95d08b52cc72a41a6f5c60
# syscall*.h implemented for:
ExclusiveArch:	%{ix86} %{x8664} alpha ia64 ppc ppc64 s390 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has
a richer API and capability set than the simple POSIX async I/O
facility. This library, libaio, provides the Linux-native API for
async I/O. The POSIX async I/O facility requires this library in order
to provide kernel-accelerated async I/O capabilities, as do
applications which require the Linux-native async I/O API.

%description -l pl
Natywna dla Linuksa obs�uga asynchronicznego wej�cia/wyj�cia ("async
I/O" lub "aio") ma bogatsze API i zestaw mo�liwo�ci ni� proste
asynchroniczne wej�cie/wyj�cie zgodne z POSIX. Ta biblioteka - libaio
- udost�pnia natywne Linuksowe API dla asynchronicznego we/wy. Zgodne
z POSIX asynchroniczne we/wy wymaga tej biblioteki do udost�pnienia
przyspieszanych przez j�dro mo�liwo�ci asynchronicznego we/wy,
podobnie jak aplikacje wymagaj�ce natywnego dla Linuksa API
asynchronicznego we/wy.

%package devel
Summary:	Header files for libaio library
Summary(pl):	Pliki nag��wkowe biblioteki libaio
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libaio library.

%description devel -l pl
Pliki nag��wkowe biblioteki libaio.

%package static
Summary:	Static libaio library
Summary(pl):	Statyczna biblioteka libaio
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libaio library.

%description static -l pl
Statyczna biblioteka libaio.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fomit-frame-pointer -fPIC -Wall -I. -nostdlib -nostartfiles"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

install -d $RPM_BUILD_ROOT%{_mandir}/man{2,3}
install man/*.3 $RPM_BUILD_ROOT%{_mandir}/man3
for f in man/*.1 ; do
	install $f $RPM_BUILD_ROOT%{_mandir}/man2/`basename $f .1`.2
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog TODO
%attr(755,root,root) %{_libdir}/libaio.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaio.so
%{_includedir}/libaio.h
%{_mandir}/man2/io_*.2*
%{_mandir}/man3/*io*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libaio.a
