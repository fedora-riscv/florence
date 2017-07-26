%bcond_without  doc
%bcond_without  xtst
%bcond_without  notification

Name:           florence
Version:        0.6.3
Release:        5%{?dist}
Summary:        Extensible scalable on-screen virtual keyboard for GNOME 
License:        GPLv2+ and GFDL
URL:            http://florence.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRequires:  desktop-file-utils
BuildRequires:  GConf2-devel
BuildRequires:  glib2-devel
%if %{with doc}
BuildRequires:  gnome-doc-utils
%endif
BuildRequires:  gstreamer1-devel
BuildRequires:  gtk3-devel
BuildRequires:  intltool
#BuildRequires:  libgnome-devel
%if %{with notification}
BuildRequires:  libnotify-devel
%endif
BuildRequires:  librsvg2-devel
BuildRequires:  libXext-devel
BuildRequires:  libxml2-devel
%if %{with xtst}
BuildRequires:  libXtst-devel
%endif
BuildRequires:  scrollkeeper
Requires(pre):  GConf2
Requires(preun):GConf2
Requires(post): GConf2
Requires:       control-center

%description
Florence is an extensible scalable virtual keyboard for GNOME. 
You need it if you can't use a real hardware keyboard, for 
example because you are disabled, your keyboard is broken or 
because you use a tablet PC, but you must be able to use a pointing 
device (as a mouse, a trackball or a touchscreen).

Florence stays out of your way when you don't need it: 
it appears on the screen only when you need it. 
A Timer-based auto-click functionality is available 
to help disabled people having difficulties to click.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
sed -i -e 's|Icon=.*|Icon=%{name}|g' -e '/Encoding/d' data/%{name}.desktop.in.in

%build
%configure  \
%if %{without doc}
            --without-docs \
%endif
%if %{without notification}
            --without-notification \
%endif
%if %{without xtst}
            --without-xtst \
%endif
%if %{without doc}
            --without-docs \
%endif
            --with-panelapplet \
            --without-at-spi \
            --disable-static
make

%install
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%make_install

find %{buildroot} -name '*.*a' -delete -print

desktop-file-install \
        --delete-original \
        --remove-category="Application" \
        --add-category="Utility" \
        --dir=%{buildroot}%{_datadir}/applications \
        %{buildroot}%{_datadir}/applications/%{name}.desktop

install -pDm0644 data/%{name}.svg %{buildroot}%{_datadir}/pixmaps/%{name}.svg

%find_lang %{name}

%post -p /sbin/ldconfig

%postun
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
/sbin/ldconfig

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%doc AUTHORS ChangeLog README
%license COPYING COPYING-DOCS
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.*
%if %{with doc}
%{_datadir}/gnome/help/%{name}/
%{_datadir}/omf/%{name}/
%{_mandir}/man1/%{name}.*
%{_mandir}/man1/%{name}_applet.*
%endif
%{_datadir}/pixmaps/%{name}.svg
%{_datadir}/glib-2.0/schemas/org.%{name}.gschema.xml
%{_libdir}/libflorence-1.0.so.*

%files devel
%{_includedir}/%{name}-1.0/
%{_libdir}/libflorence-1.0.so
%{_libdir}/pkgconfig/%{name}-1.0.pc

%changelog
* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 04 2015 Christopher Meng <rpm@cicku.me> - 0.6.3-1
- Update to 0.6.3
- Temporarily disable at-spi support since it's broken here.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 17 2014 Christopher Meng <rpm@cicku.me> - 0.6.2-1
- Update to 0.6.2

* Tue May 13 2014 Christopher Meng <rpm@cicku.me> - 0.6.1-1
- Update to 0.6.1
- Switch to GTK3 and at-spi2.
- SPEC cleanup, remove obsoleted scrollkeeper actions.

* Sat Aug 10 2013 Simon Dietz <cassmodiah@fedoraproject.org> - 0.6.0-1
- New upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.5.0-3
- Rebuild for new libpng

* Tue Aug 02 2011 Simon Wesp <cassmodiah@fedoraproject.org> - 0.5.0-2
- Fixing RHBZ#690475

* Fri Jan 28 2011 Simon Wesp <cassmodiah@fedoraproject.org> - 0.5.0-1
- New upstream release

* Fri Nov 12 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 0.4.7-2
- Build without libnotify

* Wed Jun 23 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 0.4.7-1
- New Upstream Release

* Sat Mar 27 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 0.4.6-2
- Patch DSO

* Thu Jan 28 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 0.4.6-1
- New upstream release
- Fixed RHBZ #550165

* Fri Dec 11 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.4.5-1
- New upstream release

* Thu Oct 22 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.4.4-1
- New upstream release

* Thu Aug 20 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.4.3-1
- New upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.4.2-1
- New upstream release

* Sat Jun 13 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.4.2-0.1
- Update to an unofficial prerelease (upstream sent it via email)

* Tue Jun 02 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.4.1-1
- New upstream release

* Mon Mar 23 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.4.0-1
- New upstream release

* Sun Feb 22 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.3.3-1
- New upstream release

* Mon Jan 26 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.3.2-1
- New upstream release

* Thu Dec 18 2008 Simon Wesp <cassmodiah@fedoraproject.org> - 0.3.1-1
- New upstream release
- Move installation of icon from highcolortheme to DATADIR/pixmaps

* Wed Nov 19 2008 Simon Wesp <cassmodiah@fedoraproject.org> - 0.3.0-2
- Correct URL
- Correct categories of desktop-file (Bug #472174)

* Tue Sep 16 2008 Simon Wesp <cassmodiah@fedoraproject.org> - 0.3.0-1
- New upstream release 

* Wed Jul 30 2008 Simon Wesp <cassmodiah@fedoraproject.org> - 0.2.3-2
- Create and add patch0 

* Tue Jul 29 2008 Simon Wesp <cassmodiah@fedoraproject.org> - 0.2.3-1
- New upstream release
- Delete warning-patch by Robert Scheck - included in new release
- Delete sed command to edit schemas file - included in new release
- Add sed command to delete file-extension in .desktop-file

* Sun Jul 27 2008 Simon Wesp <cassmodiah@fedoraproject.org> - 0.2.2-5
- Edit specfile bug #454208 C14 C15

* Sun Jul 27 2008 Simon Wesp <cassmodiah@fedoraproject.org> - 0.2.2-4
- Edit specfile bug #454208 C8
- Edit files section
- Add warning-patch by Robert Scheck

* Thu Jul 24 2008 Simon Wesp <cassmodiah@fedoraproject.org> - 0.2.2-3
- Edit specfile bug #454208 C4 C5 C6
- Add scrollkeeper 

* Fri Jul 11 2008 Simon Wesp <cassmodiah@fedoraproject.org> - 0.2.2-2
- Add .desktop file
- Add script to correct dirty gconf-settings

* Sun Jul 06 2008 Simon Wesp <cassmodiah@fedoraproject.org> - 0.2.2-1
- Initial Release
