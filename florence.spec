Name:           florence
Version:        0.3.0
Release:        2%{?dist}
Summary:        Extensible scalable on-screen virtual keyboard for GNOME 

Group:          User Interface/X Hardware Support
License:        GPLv2+ and GFDL
URL:            http://florence.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:         %{name}-desktop.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    libxml2-devel
BuildRequires:    libglade2-devel
BuildRequires:    at-spi-devel
BuildRequires:    librsvg2-devel
BuildRequires:    cairo-devel
BuildRequires:    libgnome-devel
BuildRequires:    gtk2-devel
BuildRequires:    GConf2-devel
BuildRequires:    desktop-file-utils
BuildRequires:    scrollkeeper
Requires(pre):    GConf2
Requires(preun):  GConf2
Requires(post):   scrollkeeper
Requires(post):   GConf2
Requires(postun): scrollkeeper


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


%prep
%setup -q
%patch0 -p1 -b .desktop

rm -f gconf-refresh
ln -sf /bin/true gconf-refresh


%build
export CFLAGS
%configure

make %{?_smp_mflags} \
     CFLAGS="${RPM_OPT_FLAGS} -Werror-implicit-function-declaration"


%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

desktop-file-install \
        --delete-original \
        --remove-category="Application; X-GNOME-PersonalSettings" \
        --add-category="Utility" \
        --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
        $RPM_BUILD_ROOT/%{_datadir}/applications/%{name}.desktop

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps 

install -p -m 0644 data/%{name}.svg \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg


%pre
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=$(gconftool-2 --get-default-source)
    gconftool-2 --makefile-uninstall-rule \
    %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :
fi


%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=$(gconftool-2 --get-default-source)
    gconftool-2 --makefile-uninstall-rule \
    %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :
fi


%post
scrollkeeper-update -q -o %{_datadir}/omf/%{name} || :

export GCONF_CONFIG_SOURCE=$(gconftool-2 --get-default-source)
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
scrollkeeper-update -q || :

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi 


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README AUTHORS ChangeLog COPYING-DOCS NEWS
%{_datadir}/%{name}/
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/%{name}.svg
%{_datadir}/icons/hicolor/*/apps/%{name}.svg
%{_datadir}/gnome/help/%{name}/
%{_datadir}/omf/%{name}/
%{_sysconfdir}/gconf/schemas/%{name}.schemas



%changelog
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
