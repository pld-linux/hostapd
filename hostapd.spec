Summary:	HostAP - acts as an access point
Summary(es.UTF-8):	HostAP - actúa como un punto de acceso
Summary(pl.UTF-8):	HostAP - praca jako access point
Name:		hostapd
Version:	2.9
Release:	1
License:	BSD
Group:		Daemons
Source0:	http://w1.fi/releases/%{name}-%{version}.tar.gz
# Source0-md5:	f188fc53a495fe7af3b6d77d3c31dee8
Source1:	%{name}.init
Patch0:		%{name}-config.patch
Patch1:		%{name}-build-time-config.patch
URL:		http://w1.fi/hostapd/
BuildRequires:	libnl-devel >= 1:3.2
BuildRequires:	openssl-devel >= 1.0.2
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3
Requires(post,preun):	/sbin/chkconfig
Requires:	openssl >= 1.0.2
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains utilities and userspace daemon for the Linux
driver for wireless LAN cards based on Intersil's Prism2/2.5/3,
Intersil/Conexant Prism GT/Duette/Indigo (Prism54), Atheros ar521x
(madwifi) chipsets. The driver supports a so called Host AP mode,
i.e., it takes care of IEEE 802.11 management functions in the host
computer and acts as an access point. This does not require any
special firmware for the wireless LAN card. In addition to this, it
has support for normal station operations in BSS and possible also in
IBSS.

%description -l es.UTF-8
Este paquete contiene unas herramientas y un servidor del espacio de
usuario para tarjetas LAN inalámbricas basadas en el chipset Intersil
Prism2/2.5/3, Intersil/Conexant Prism GT/Duette/Indigo (Prism54),
Atheros ar521x (madwifi). El driver soporta el llamado modo Host AP,
es decir, se encarga de las funciones administrativas el el host,
actuando como "access point". Ello no requiere ningún firmware
especial para la tarjeta LAN inalámbrica. Además, también hay soporte
para operaciones normales de estación en BSS y posiblemente también en
IBSS.

%description -l pl.UTF-8
Ten pakiet zawiera narzędzia oraz demona działającego w przestrzeni
użytkownika dla linuksowego sterownika kart sieci bezprzewodowych
opartych na układach Intersil Prism2/2.5/3, Intersil/Conexant Prism
GT/Duette/Indigo (Prism54), Atheros ar521x (madwifi). Sterownik
obsługuje tak zwany tryb Host AP, czyli dba o funkcje zarządzające
IEEE 802.11 na komputerze i działa jako access point. Nie wymaga to
żadnego specjalnego firmware dla karty sieci bezprzewodowej. Ponadto
ma obsługę normalnych operacji stacyjnych w BSS, a być może także
IBSS.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{__sed} '/CFLAGS =/{s/-g//; s/-O2/$(OPTCFLAGS)/}' -i hostapd/Makefile

%build
%{__make} -C hostapd all nt_password_hash hlr_auc_gw \
	V=1 \
	CC="%{__cc}" \
	OPTCFLAGS="%{rpmcflags} %{rpmcppflags}" \
	LDFLAGS="%{rpmcflags} %{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,%{_sysconfdir}/{hostap,pcmcia},%{_mandir}/man{1,8}}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

# hostapd hostapd_cli nt_password_hash hlr_auc_gw
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/hostapd
install -p hostapd/hostapd $RPM_BUILD_ROOT/sbin
install -p hostapd/hostapd_cli $RPM_BUILD_ROOT/sbin
install -p hostapd/nt_password_hash $RPM_BUILD_ROOT/sbin
install -p hostapd/hlr_auc_gw $RPM_BUILD_ROOT/sbin
cp -p hostapd/hostapd.8 $RPM_BUILD_ROOT%{_mandir}/man8
cp -p hostapd/hostapd_cli.1 $RPM_BUILD_ROOT%{_mandir}/man1

# hostapd configuration
cp -a hostapd/hostapd.accept $RPM_BUILD_ROOT%{_sysconfdir}/hostap
cp -a hostapd/hostapd.conf $RPM_BUILD_ROOT%{_sysconfdir}/hostap
cp -a hostapd/hostapd.deny $RPM_BUILD_ROOT%{_sysconfdir}/hostap

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add hostapd
%service hostapd restart "HostAP Daemon"

%preun
if [ "$1" = "0" ]; then
	%service hostapd stop
	/sbin/chkconfig --del hostapd
fi

%files
%defattr(644,root,root,755)
%doc COPYING hostapd/{ChangeLog,README,README-WPS}
%dir %{_sysconfdir}/hostap
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hostap/hostapd.accept
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hostap/hostapd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hostap/hostapd.deny
%attr(755,root,root) /sbin/hlr_auc_gw
%attr(755,root,root) /sbin/hostapd
%attr(755,root,root) /sbin/hostapd_cli
%attr(755,root,root) /sbin/nt_password_hash
%attr(754,root,root) /etc/rc.d/init.d/hostapd
%{_mandir}/man1/hostapd_cli.1*
%{_mandir}/man8/hostapd.8*
