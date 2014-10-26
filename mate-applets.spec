Summary:	Small applications which embed themselves in the MATE panel
Name:		mate-applets
Version:	1.8.1
Release:	1
License:	GPL v2, FDL
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	01979ea5f4d453ed0a91d3edc1de0eb0
Patch0:		%{name}-m4_fix.patch
URL:		http://www.mate.org/
BuildRequires:	NetworkManager-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	gdbm-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel
BuildRequires:	intltool
BuildRequires:	libgtop-devel
BuildRequires:	libmatekbd-devel >= 1.8.0
BuildRequires:	libmateweather-devel >= 1.8.0
BuildRequires:	libnotify-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-progs
BuildRequires:	mate-desktop-devel >= 1.8.0
BuildRequires:	mate-panel-devel
BuildRequires:	mate-settings-daemon-devel >= 1.8.0
BuildRequires:	pkg-config
BuildRequires:	yelp-tools
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Requires:	mate-panel >= 1.8.0
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

%package -n mate-applet-invest
Summary:	Invest applet
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n mate-applet-invest
Invest applet.

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

%package -n mate-applet-weather
Summary:	Weather Report applet
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	xdg-desktop-notification-daemon

%description -n mate-applet-weather
Weather Report applet.

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
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-static	\
	--enable-polkit
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT					\
	accessx_status_iconsdir=%{_iconsdir}/hicolor/48x48/apps	\
	pythondir=%{py_scriptdir}					\
	uidir=%{_datadir}/mate-panel/ui

%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/stickynotes-applet.convert
%{__rm} $RPM_BUILD_ROOT%{py_scriptdir}/mate_invest/*.py

%find_lang %{name} --all-name --with-mate
%find_lang mate-accessx-status --with-mate
%find_lang mate-battstat --with-mate
%find_lang mate-char-palette --with-mate
%find_lang mate-cpufreq-applet --with-mate
%find_lang mate-drivemount --with-mate
%find_lang mate-geyes --with-mate
%find_lang mate-multiload --with-mate
%find_lang mate-stickynotes_applet --with-mate
%find_lang mate-trashapplet --with-mate
%find_lang mateweather --with-mate

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_gsettings_cache

%postun
%update_gsettings_cache

%post -n mate-applet-accessx-status
%update_icon_cache hicolor

%postun -n mate-applet-accessx-status
%update_icon_cache hicolor

%post -n mate-applet-battstat
%update_gsettings_cache

%postun -n mate-applet-battstat
%update_gsettings_cache

%post -n mate-applet-charpicker
%update_icon_cache hicolor
%update_gsettings_cache

%postun -n mate-applet-charpicker
%update_icon_cache hicolor
%update_gsettings_cache

%post -n mate-applet-cpufreq
%update_icon_cache hicolor
%update_gsettings_cache

%postun -n mate-applet-cpufreq
%update_icon_cache hicolor
%update_gsettings_cache

%post -n mate-applet-geyes
%update_icon_cache hicolor
%update_gsettings_cache

%postun -n mate-applet-geyes
%update_icon_cache hicolor
%update_gsettings_cache

%post -n mate-applet-invest
%update_icon_cache hicolor
%update_gsettings_cache

%postun -n mate-applet-invest
%update_icon_cache hicolor
%update_gsettings_cache

%post -n mate-applet-multiload
%update_gsettings_cache

%postun -n mate-applet-multiload
%update_gsettings_cache

%post -n mate-applet-stickynotes
%update_icon_cache hicolor
%update_gsettings_cache

%postun -n mate-applet-stickynotes
%update_icon_cache hicolor
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README

%dir %{_libexecdir}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/builder

%attr(755,root,root) %{_libexecdir}/command-applet
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.command.gschema.xml
%{_datadir}/dbus-1/services/org.mate.panel.applet.CommandAppletFactory.service
%{_datadir}/mate-panel/applets/org.mate.applets.CommandApplet.mate-panel-applet

%attr(755,root,root) %{_libexecdir}/timer-applet
%{_datadir}/dbus-1/services/org.mate.panel.applet.TimerAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.timer.gschema.xml
%{_datadir}/mate-panel/applets/org.mate.applets.TimerApplet.mate-panel-applet

%{_datadir}/mate-applets/builder/prefs-dialog.ui

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

%files -n mate-applet-invest
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mate-invest-chart
%dir %{py_scriptdir}/mate_invest
%{py_scriptdir}/mate_invest/*.py[co]
%attr(755,root,root) %{_libexecdir}//invest-applet
%{_datadir}/dbus-1/services/org.mate.panel.applet.InvestAppletFactory.service
%{_iconsdir}/hicolor/*/apps/mate-invest-applet.png
%{_iconsdir}/hicolor/*/apps/mate-invest-applet.svg
%{_datadir}/mate-applets/builder/financialchart.ui
%{_datadir}/mate-applets/invest-applet
%{_datadir}/mate-panel/applets/org.mate.applets.InvestApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/Invest_Applet.xml

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

%files -n mate-applet-weather -f mateweather.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/mateweather-applet-2
%{_datadir}/dbus-1/services/org.mate.panel.applet.MateWeatherAppletFactory.service
%{_datadir}/mate-panel/applets/org.mate.applets.MateWeatherApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/mateweather-applet-menu.xml

