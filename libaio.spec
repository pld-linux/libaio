%bcond_without	tests
Summary:	Linux-native asynchronous I/O access library
Summary(pl.UTF-8):	Biblioteka natywnego dla Linuksa asynchronicznego dostępu do wejścia/wyjścia
Name:		libaio
Version:	0.3.109
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	ftp://ftp.kernel.org/pub/linux/libs/aio/%{name}-%{version}.tar.gz
# Source0-md5:	435a5b16ca6198eaf01155263d855756
Patch0:		%{name}-DESTDIR.patch
BuildRequires:	rpm-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has
a richer API and capability set than the simple POSIX async I/O
facility.

This library, libaio, provides the Linux-native API for async I/O. The
POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

%description -l pl.UTF-8
Natywna dla Linuksa obsługa asynchronicznego wejścia/wyjścia ("async
I/O" lub "aio") ma bogatsze API i zestaw możliwości niż proste
asynchroniczne wejście/wyjście zgodne z POSIX.

Ta biblioteka - libaio - udostępnia natywne Linuksowe API dla
asynchronicznego we/wy. Zgodne z POSIX asynchroniczne we/wy wymaga tej
biblioteki do udostępnienia przyspieszanych przez jądro możliwości
asynchronicznego we/wy, podobnie jak aplikacje wymagające natywnego
dla Linuksa API asynchronicznego we/wy.

%package devel
Summary:	Header files for libaio library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libaio
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libaio library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libaio.

%package static
Summary:	Static libaio library
Summary(pl.UTF-8):	Statyczna biblioteka libaio
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libaio library.

%description static -l pl.UTF-8
Statyczna biblioteka libaio.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags} -fomit-frame-pointer -fPIC -Wall -I. -nostdlib -nostartfiles"

%{?with_tests:%{__make} CC="%{__cc}" partcheck}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_lib}

%{__make} install \
	libdir=/%{_lib} \
	usrlibdir=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

# omit some manuals:
# man2/io_* already included in man-pages
# some man3/aio_* already included in glibc-devel-doc (from man-pages)
install -d $RPM_BUILD_ROOT%{_mandir}/man3
cp -a man/aio{,_cancel64,_error64,_fsync64,_init,_read64,_return64,_suspend64,_write64}.3 $RPM_BUILD_ROOT%{_mandir}/man3
cp -a man/io*.3 $RPM_BUILD_ROOT%{_mandir}/man3
cp -a man/lio*.3 $RPM_BUILD_ROOT%{_mandir}/man3

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog TODO
%attr(755,root,root) /%{_lib}/libaio.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libaio.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaio.so
%{_includedir}/libaio.h
%{_mandir}/man3/aio*.3*
%{_mandir}/man3/io*.3*
%{_mandir}/man3/lio_*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libaio.a
