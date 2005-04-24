Summary:	A terminal program for displaying Unicode on the console.
Name:		bogl
Version:	0.1.18
Release:	1
License:	GPL
Group:		System Environment/Libraries
Source0:	%{name}_%{version}-1.tar.gz
# Source0-md5:	9658700ed196eb1789c12aca0a095cb5
Source1:	wlite-0.8.1.tar.gz
# Source1-md5:	03a2faa33978e88ea2b9ff4679b8f2df
Source2:	http://www.cl.cam.ac.uk/~mgk25/download/ucs-fonts.tar.gz
# Source2-md5:	cca6a3cb6cfbde5f3ebb24278a9022a4
Source3:	http://www.cl.cam.ac.uk/~mgk25/download/ucs-fonts-asian.tar.gz
# Source3-md5:	d3184f182c6eebfcf156d08a65696496
Source4:	14x14cjk.bdf.gz
# Source4-md5:	c08ab351a43a91632127f509aadc6797
Patch0:		bogl-0.1.18-rh.patch
Patch1:		bogl-0.1.9-fpic.patch
Patch3:		bogl-0.1.9-2.6fbdev.patch
Patch4:		bogl-0.1.18-gcc.patch
Patch5:		bogl-0.1.18-noexecstack.patch
URL:		http://www.msu.edu/user/pfaffben/projects.html
BuildRequires:	gd-devel
BuildRequires:	libpng-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BOGL stands for Ben's Own Graphics Library.  It is a small graphics
library for Linux kernel frame buffers.  It supports only very simple
graphics.

%package devel
Summary:	Development files required to build BOGL applications.
Group:		Development/Libraries
Requires:	bogl = %{epoch}:%{version}-%{release}

%description devel
The bogl-devel package contains the static libraries and header files
for writing BOGL applications.

%package bterm
Summary:	A Unicode capable terminal program for the Linux frame buffer.
Group:		Applications/System
Requires:	bogl = %{epoch}:%{version}-%{release}

%description bterm
The bterm application is a terminal emulator that displays to a Linux
frame buffer.  It is able to display Unicode text on the console.

%prep
%setup -q -n bogl -a 1
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

mkdir -p fonts
cd fonts
tar zxf %{SOURCE2}
tar zxf %{SOURCE3}

%build
make CFLAGS="$RPM_OPT_FLAGS"
#./mergebdf fonts/9x18.bdf fonts/18x18ja.bdf > font.bdf
gunzip -c %{SOURCE4} > font.bdf
./bdftobogl -b font.bdf > font.bgf

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT libdir=%{_libdir} install
make -C wlite prefix=$RPM_BUILD_ROOT/%{_prefix} libdir=$RPM_BUILD_ROOT/%{_libdir} install
if [ -f wlite/libwlitediet.a ]; then
    install -m 644 wlite/libwlitediet.a $RPM_BUILD_ROOT/%{_libdir}
fi
mkdir -p $RPM_BUILD_ROOT/usr/lib/bogl/
cp font.bgf $RPM_BUILD_ROOT/usr/lib/bogl/
cp font.bdf $RPM_BUILD_ROOT/usr/lib/bogl/
gzip -9 $RPM_BUILD_ROOT/usr/lib/bogl/font.bdf
gzip -9 $RPM_BUILD_ROOT/usr/lib/bogl/font.bgf

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bdftobogl
%attr(755,root,root) %{_bindir}/mergebdf
%attr(755,root,root) %{_bindir}/pngtobogl
%attr(755,root,root) %{_bindir}/reduce-font
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/bogl
%{_includedir}/wlite*

%files bterm
%defattr(644,root,root,755)
%doc README.BOGL-bterm
%attr(755,root,root) %{_bindir}/bterm
%dir %{_datadir}/terminfo/b
%{_datadir}/terminfo/b/bterm
%{_libdir}/bogl

%changelog
