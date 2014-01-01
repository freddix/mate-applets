# TODO: invest-applet not packaged

Summary:	Small applications which embed themselves in the MATE panel
Name:		mate-applets
Version:	1.6.2
Release:	1
License:	GPL v2, FDL
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	7a83557afd1a71940cb623d92788ecc4
Patch0:		%{name}-m4_fix.patch
URL:		http://www.mate.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	mate-settings-daemon-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gdbm-devel
BuildRequires:	gettext-devel
BuildRequires:	mate-desktop-devel
BuildRequires:	mate-doc-utils
BuildRequires:	mate-panel-devel
BuildRequires:	gtk+-devel
BuildRequires:	intltool
BuildRequires:	libmatekbd-devel
BuildRequires:	libgtop-devel
BuildRequires:	libmateweather-devel
BuildRequires:	libnotify-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-progs
BuildRequires:	pkg-config
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	rarian
Requires:	mate-panel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_matehelpdir	%{_datadir}/mate/help
%define		_libexecdir	%{_libdir}/%{name}

%description
The mate-applets package provides panel applets which enhance your
MATE experience.

%package devel
Summary:	Header files for mate-applets
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files for mate-applets.

%package -n mate-applet-accessx-status
Summary:	Keyboard Accessibility Status applet
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n mate-applet-accessx-status
Keyboard Accessibility Status applet.

%package -n mate-applet-battstat
Summary:	Battery Charge Monitor applet
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n mate-applet-battstat
Battery Charge Monitor applet.

%package -n mate-applet-charpicker
Summary:	Character Palette applet
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n mate-applet-charpicker
Character Palette applet.

%package -n mate-applet-cpufreq
Summary:	CPU Frequency Scaling Monitor applet
Group:		X11/Applications
Requires:	polkit
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n mate-applet-cpufreq
CPU Frequency Scaling Monitor applet.

%package -n mate-applet-drivemount
Summary:	Disk Mounter applet
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n mate-applet-drivemount
Disk Mounter applet.

%package -n mate-applet-geyes
Summary:	Geyes applet
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n mate-applet-geyes
Geyes applet.

%package -n mate-applet-weather
Summary:	Weather Report applet
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	xdg-desktop-notification-daemon

%description -n mate-applet-weather
Weather Report applet.

%package -n mate-applet-multiload
Summary:	System Monitor applet
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n mate-applet-multiload
System Monitor applet.

%package -n mate-applet-stickynotes
Summary:	Sticky Notes applet
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n mate-applet-stickynotes
Sticky Notes applet.

%package -n mate-applet-trash
Summary:	Trash applet
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n mate-applet-trash
Trash applet.

%prep
%setup -q
%patch0 -p1

# kill mate common deps
%{__sed} -i -e 's/MATE_COMPILE_WARNINGS.*//g'	\
    -i -e 's/MATE_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/MATE_COMMON_INIT//g'		\
    -i -e 's/MATE_DEBUG_CHECK//g' configure.ac

%build
%{__glib_gettextize}
%{__libtoolize}
%{__intltoolize}
mate-doc-prepare --copy
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-schemas-install	\
	--disable-static		\
	--enable-mixer-applet		\
	--enable-polkit
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT					\
	accessx_status_iconsdir=%{_iconsdir}/hicolor/48x48/apps	\
	pythondir=%{py_sitedir}					\
	uidir=%{_datadir}/mate-panel/ui

%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/stickynotes-applet.convert
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,crh,en@shaw,es_*}

%find_lang %{name} --all-name --with-mate
%find_lang mate-accessx-status --with-mate --with-omf
%find_lang mate-battstat --with-mate --with-omf
%find_lang mate-char-palette --with-mate --with-omf
%find_lang mate-cpufreq-applet --with-mate --with-omf
%find_lang mate-drivemount --with-mate --with-omf
%find_lang mate-geyes --with-mate --with-omf
%find_lang mate-multiload --with-mate --with-omf
%find_lang mate-stickynotes_applet --with-mate --with-omf
%find_lang mate-trashapplet --with-mate --with-omf
%find_lang mateweather --with-mate --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post -n mate-applet-accessx-status
%scrollkeeper_update_post
%update_icon_cache hicolor

%postun -n mate-applet-accessx-status
%scrollkeeper_update_postun
%update_icon_cache hicolor

%post -n mate-applet-battstat
%scrollkeeper_update_post
%update_gsettings_cache

%postun -n mate-applet-battstat
%scrollkeeper_update_postun
%update_gsettings_cache

%post -n mate-applet-charpicker
%scrollkeeper_update_post
%update_icon_cache hicolor
%update_gsettings_cache

%postun -n mate-applet-charpicker
%scrollkeeper_update_postun
%update_icon_cache hicolor
%update_gsettings_cache

%post -n mate-applet-cpufreq
%scrollkeeper_update_post
%update_icon_cache hicolor
%update_gsettings_cache

%postun -n mate-applet-cpufreq
%scrollkeeper_update_postun
%update_icon_cache hicolor
%update_gsettings_cache

%post -n mate-applet-drivemount
%scrollkeeper_update_post

%postun -n mate-applet-drivemount
%scrollkeeper_update_postun

%post -n mate-applet-geyes
%scrollkeeper_update_post
%update_icon_cache hicolor
%update_gsettings_cache

%postun -n mate-applet-geyes
%scrollkeeper_update_postun
%update_icon_cache hicolor
%update_gsettings_cache

%post -n mate-applet-weather
%scrollkeeper_update_post

%postun -n mate-applet-weather
%scrollkeeper_update_postun

%post -n mate-applet-multiload
%scrollkeeper_update_post
%update_gsettings_cache

%postun -n mate-applet-multiload
%scrollkeeper_update_postun
%update_gsettings_cache

%post -n mate-applet-stickynotes
%scrollkeeper_update_post
%update_icon_cache hicolor
%update_gsettings_cache

%postun -n mate-applet-stickynotes
%scrollkeeper_update_postun
%update_icon_cache hicolor
%update_gsettings_cache

%post -n mate-applet-trash
%scrollkeeper_update_post

%postun -n mate-applet-trash
%scrollkeeper_update_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README

%dir %{_libexecdir}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/builder

%files -n mate-applet-accessx-status -f mate-accessx-status.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/accessx-status-applet
%{_datadir}/dbus-1/services/org.mate.panel.applet.AccessxStatusAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.battstat.gschema.xml
%{_datadir}/mate-panel/applets/org.mate.applets.AccessxStatusApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/accessx-status-applet-menu.xml
%{_iconsdir}/hicolor/*/apps/ax-applet.png
%{_pixmapsdir}/mate-accessx-status-applet

%files -n mate-applet-battstat -f mate-battstat.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/battstat-applet-2
%{_datadir}/%{name}/builder/battstat_applet.ui
%{_datadir}/dbus-1/services/org.mate.panel.applet.BattstatAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.battstat.gschema.xml
%{_datadir}/mate-panel/applets/org.mate.applets.BattstatApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/battstat-applet-menu.xml
%{_sysconfdir}/sound/events/mate-battstat_applet.soundlist

%files -n mate-applet-charpicker -f mate-char-palette.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/charpick_applet2
%{_datadir}/dbus-1/services/org.mate.panel.applet.CharpickerAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.charpick.gschema.xml
%{_datadir}/mate-panel/applets/org.mate.applets.CharpickerApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/charpick-applet-menu.xml

%files -n mate-applet-cpufreq -f mate-cpufreq-applet.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mate-cpufreq-selector
%attr(755,root,root) %{_libexecdir}/mate-cpufreq-applet
%{_datadir}/%{name}/builder/cpufreq-preferences.ui
%{_datadir}/dbus-1/services/org.mate.panel.applet.CPUFreqAppletFactory.service
%{_datadir}/dbus-1/system-services/org.mate.CPUFreqSelector.service
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.cpufreq.gschema.xml
%{_datadir}/mate-panel/applets/org.mate.applets.CPUFreqApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/cpufreq-applet-menu.xml
%{_datadir}/polkit-1/actions/org.mate.cpufreqselector.policy
%{_iconsdir}/hicolor/*/apps/mate-cpu-frequency-applet.*
%{_pixmapsdir}/mate-cpufreq-applet
%{_sysconfdir}/dbus-1/system.d/org.mate.CPUFreqSelector.conf

%files -n mate-applet-drivemount -f mate-drivemount.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/drivemount_applet2
%{_datadir}/dbus-1/services/org.mate.panel.applet.DriveMountAppletFactory.service
%{_datadir}/mate-panel/applets/org.mate.applets.DriveMountApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/drivemount-applet-menu.xml

%files -n mate-applet-geyes -f mate-geyes.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/geyes_applet2
%{_datadir}/%{name}/geyes
%{_datadir}/dbus-1/services/org.mate.panel.applet.GeyesAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.geyes.gschema.xml
%{_datadir}/mate-panel/applets/org.mate.applets.GeyesApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/geyes-applet-menu.xml
%{_iconsdir}/hicolor/*/apps/mate-eyes-applet.*

%files -n mate-applet-weather -f mateweather.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/mateweather-applet-2
%{_datadir}/dbus-1/services/org.mate.panel.applet.MateWeatherAppletFactory.service
%{_datadir}/mate-panel/applets/org.mate.applets.MateWeatherApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/mateweather-applet-menu.xml

%files -n mate-applet-multiload -f mate-multiload.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/multiload-applet-2
%{_datadir}/dbus-1/services/org.mate.panel.applet.MultiLoadAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.multiload.gschema.xml
%{_datadir}/mate-panel/applets/org.mate.applets.MultiLoadApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/multiload-applet-menu.xml

%files -n mate-applet-stickynotes -f mate-stickynotes_applet.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/stickynotes_applet
%{_datadir}/%{name}/builder/stickynotes.ui
%{_datadir}/dbus-1/services/org.mate.panel.applet.StickyNotesAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.stickynotes.gschema.xml
%{_datadir}/mate-panel/applets/org.mate.applets.StickyNotesApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/stickynotes-applet-menu.xml
%{_iconsdir}/hicolor/*/apps/mate-sticky-notes-applet.*
%{_pixmapsdir}/mate-stickynotes

%files -n mate-applet-trash -f mate-trashapplet.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/trashapplet
%{_datadir}/%{name}/builder/trashapplet-empty-progress.ui
%{_datadir}/dbus-1/services/org.mate.panel.applet.TrashAppletFactory.service
%{_datadir}/mate-panel/applets/org.mate.applets.TrashApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/trashapplet-menu.xml

