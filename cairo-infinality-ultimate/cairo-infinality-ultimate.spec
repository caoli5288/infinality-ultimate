%define pixman_version 0.30.0
%define freetype_version 2.1.9
%define fontconfig_version 2.2.95

Summary:	A 2D graphics library
Name:		cairo-infinality-ultimate
Version:	1.14.6
Release:	2%{?dist}
URL:		http://cairographics.org
Source0:	http://cairographics.org/releases/cairo-%{version}.tar.xz
License:	LGPLv2 or MPLv1.1

Patch0:         cairo-multilib.patch
Patch1:         cairo-respect-fontconfig_pb.patch
Patch2:         cairo-server-side-gradients.patch
Patch3:         cairo-webkit-html5-fix.patch
Patch4:         cairo-make-lcdfilter-default.patch
Patch5:         0001-xlib-Fix-double-free-in-_get_image_surface.patch

BuildRequires: pkgconfig
BuildRequires: libXrender-devel
BuildRequires: libX11-devel
BuildRequires: libpng-devel
BuildRequires: libxml2-devel
BuildRequires: pixman-devel >= %{pixman_version}
BuildRequires: freetype-devel >= %{freetype_version}
BuildRequires: fontconfig-devel >= %{fontconfig_version}
BuildRequires: glib2-devel
BuildRequires: librsvg2-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libEGL-devel

Provides: cairo = %{version}-%{release}
Provides: cairo%{?_isa} = %{version}-%{release}
Conflicts: cairo%{?_isa}

%description
Cairo is a 2D graphics library designed to provide high-quality display
and print output. Currently supported output targets include the X Window
System, OpenGL (via glitz), in-memory image buffers, and image files (PDF,
PostScript, and SVG).

Cairo is designed to produce consistent output on all output media while
taking advantage of display hardware acceleration when available (e.g.
through the X Render Extension or OpenGL).

%package devel
Summary: Development files for cairo
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: cairo-devel = %{version}-%{release}
Provides: cairo-devel%{?_isa} = %{version}-%{release}
Conflicts: cairo-devel%{?_isa}

%description devel
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains libraries, header files and developer documentation
needed for developing software which uses the cairo graphics library.

%package gobject
Summary: GObject bindings for cairo
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: cairo-gobject = %{version}-%{release}
Provides: cairo-gobject%{?_isa} = %{version}-%{release}
Conflicts: cairo-gobject%{?_isa}

%description gobject
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains functionality to make cairo graphics library
integrate well with the GObject object system used by GNOME.

%package gobject-devel
Summary: Development files for cairo-gobject
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-gobject%{?_isa} = %{version}-%{release}
Provides: cairo-gobject-devel = %{version}-%{release}
Provides: cairo-gobject-devel%{?_isa} = %{version}-%{release}
Conflicts: cairo-gobject-devel%{?_isa}

%description gobject-devel
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains libraries, header files and developer documentation
needed for developing software which uses the cairo Gobject library.

%package tools
Summary: Development tools for cairo
Provides: cairo-tools = %{version}-%{release}
Provides: cairo-tools%{?_isa} = %{version}-%{release}
Conflicts: cairo-tools%{?_isa}

%description tools
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains tools for working with the cairo graphics library.
 * cairo-trace: Record cairo library calls for later playback

%prep
%setup -q -n cairo-%{version}
%patch5 -p1
%patch0 -p1 -b .multilib
%patch4 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1


%build
%configure --disable-static	\
	--enable-xlib		\
	--enable-ft		\
	--enable-ps		\
	--enable-pdf		\
	--enable-svg		\
	--enable-tee		\
	--enable-gl		\
	--enable-gobject	\
	--disable-gtk-doc
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make V=1 %{?_smp_mflags}

%install
%make_install
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post gobject -p /sbin/ldconfig
%postun gobject -p /sbin/ldconfig

%files
%license COPYING COPYING-LGPL-2.1 COPYING-MPL-1.1
%doc AUTHORS BIBLIOGRAPHY BUGS NEWS README
%{_libdir}/libcairo.so.*
%{_libdir}/libcairo-script-interpreter.so.*
%{_bindir}/cairo-sphinx

%files devel
%doc ChangeLog PORTING_GUIDE
%dir %{_includedir}/cairo/
%{_includedir}/cairo/cairo-deprecated.h
%{_includedir}/cairo/cairo-features.h
%{_includedir}/cairo/cairo-ft.h
%{_includedir}/cairo/cairo.h
%{_includedir}/cairo/cairo-pdf.h
%{_includedir}/cairo/cairo-ps.h
%{_includedir}/cairo/cairo-script-interpreter.h
%{_includedir}/cairo/cairo-svg.h
%{_includedir}/cairo/cairo-tee.h
%{_includedir}/cairo/cairo-version.h
%{_includedir}/cairo/cairo-xlib-xrender.h
%{_includedir}/cairo/cairo-xlib.h
%{_includedir}/cairo/cairo-gl.h
%{_includedir}/cairo/cairo-script.h
%{_includedir}/cairo/cairo-xcb.h
%{_libdir}/libcairo.so
%{_libdir}/libcairo-script-interpreter.so
%{_libdir}/pkgconfig/cairo-fc.pc
%{_libdir}/pkgconfig/cairo-ft.pc
%{_libdir}/pkgconfig/cairo.pc
%{_libdir}/pkgconfig/cairo-pdf.pc
%{_libdir}/pkgconfig/cairo-png.pc
%{_libdir}/pkgconfig/cairo-ps.pc
%{_libdir}/pkgconfig/cairo-svg.pc
%{_libdir}/pkgconfig/cairo-tee.pc
%{_libdir}/pkgconfig/cairo-xlib.pc
%{_libdir}/pkgconfig/cairo-xlib-xrender.pc
%{_libdir}/pkgconfig/cairo-egl.pc
%{_libdir}/pkgconfig/cairo-gl.pc
%{_libdir}/pkgconfig/cairo-glx.pc
%{_libdir}/pkgconfig/cairo-script.pc
%{_libdir}/pkgconfig/cairo-xcb-shm.pc
%{_libdir}/pkgconfig/cairo-xcb.pc
%{_datadir}/gtk-doc/html/cairo

%files gobject
%{_libdir}/libcairo-gobject.so.*

%files gobject-devel
%{_includedir}/cairo/cairo-gobject.h
%{_libdir}/libcairo-gobject.so
%{_libdir}/pkgconfig/cairo-gobject.pc

%files tools
%{_bindir}/cairo-trace
%{_libdir}/cairo/

%changelog
* Fri Nov 11 2016 caoli5288 <caoli5288@gmail.com> 1.14.6-2
- new package built with tito

* Tue Aug 09 2016 Daniel Renninghoff <daniel.renninghoff@gmail.com> - 1.14.6-2
- spec file cleanups.

* Wed Mar 30 2016 Daniel Renninghoff <daniel.renninghoff@gmail.com> - 1.14.6-1
- updated to 1.14.6.

* Mon Nov 23 2015 Daniel Renninghoff <daniel.renninghoff@gmail.com> - 1.14.4-3
- fixed a multilib bug.

* Sun Nov 22 2015 Daniel Renninghoff <daniel.renninghoff@gmail.com> - 1.14.4-2
- fixed a small bug.

* Fri Nov 20 2015 Daniel Renninghoff <daniel.renninghoff@gmail.com> - 1.14.4-1
- Based on cairo-1.14.2-2
