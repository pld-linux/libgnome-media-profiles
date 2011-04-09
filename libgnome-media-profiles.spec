#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	GNOME Media Profiles library
Name:		libgnome-media-profiles
Version:	3.0.0
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libgnome-media-profiles/3.0/%{name}-%{version}.tar.bz2
# Source0-md5:	75a64a4ebffcd76cbc631db95df7a133
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	gnome-doc-utils
BuildRequires:	gstreamer-devel >= 0.10.23
BuildRequires:	gstreamer-plugins-base >= 0.10.23
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.23
Requires(post,preun):	GConf2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The GNOME Media Profiles library provides prebuilt GStreamer pipelines
for applications aiming to support different sound formats.

%package devel
Summary:	Header files for GNOME Media Profiles library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GNOME Media Profiles
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for GNOME Media Profiles library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GNOME Media Profiles.

%package static
Summary:	Static GNOME Media Profiles library
Summary(pl.UTF-8):	Statyczna biblioteka GNOME Media Profiles
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GNOME Media Profiles library.

%description static -l pl.UTF-8
Statyczna biblioteka GNOME Media Profiles.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install \
	--disable-scrollkeeper \
	%{__enable_disable static_libs static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name} --all-name --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%gconf_schema_install gnome-media-profiles.schemas

%preun
%gconf_schema_uninstall gnome-media-profiles.schemas

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gnome-audio-profiles-properties
%attr(755,root,root) %{_libdir}/libgnome-media-profiles-3.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnome-media-profiles-3.0.so.0
%{_sysconfdir}/gconf/schemas/gnome-media-profiles.schemas
%{_datadir}/libgnome-media-profiles

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-media-profiles-3.0.so
%{_includedir}/libgnome-media-profiles-3.0
%{_pkgconfigdir}/libgnome-media-profiles-3.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgnome-media-profiles-3.0.a
%endif
