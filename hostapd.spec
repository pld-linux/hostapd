#
# TODO:		check madwifi-ng-devel and madwifi-devel BR
#
Summary:	HostAP - acts as an access point
Summary(es.UTF-8):   HostAP - actúa como un punto de acceso
Summary(pl.UTF-8):   HostAP - praca jako access point
Name:		hostapd
Version:	0.5.7
Release:	1
License:	GPL v2
Group:		Daemons
Source0:	http://hostap.epitest.fi/releases/%{name}-%{version}.tar.gz
# Source0-md5:	d5113247dc6ee17106e6bc7cb89aa507
Source1:	%{name}.init
Patch0:		%{name}-config.patch
Patch1:		%{name}-build-time-config.patch
URL:		http://hostap.epitest.fi/
BuildRequires:	madwifi-ng-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	kernel-net-hostap >= 0.1.2
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

%build
%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcflags}"

%{__make} nt_password_hash \
	CC="%{__cc}" \
	OPT="%{rpmcflags}"

%{__make} hlr_auc_gw \
	CC="%{__cc}" 
	OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,%{_sysconfdir}/{hostap,pcmcia}}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

#hostapd hostapd_cli nt_password_hash hlr_auc_gw
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/hostapd
install hostapd $RPM_BUILD_ROOT/sbin
install hostapd_cli $RPM_BUILD_ROOT/sbin
install nt_password_hash $RPM_BUILD_ROOT/sbin
install hlr_auc_gw $RPM_BUILD_ROOT/sbin

#hostapd configuration
install hostapd.accept $RPM_BUILD_ROOT%{_sysconfdir}/hostap
install hostapd.conf $RPM_BUILD_ROOT%{_sysconfdir}/hostap
install hostapd.deny $RPM_BUILD_ROOT%{_sysconfdir}/hostap

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add hostapd
%service hostapd restart "HostAP daemons"

%preun
if [ "$1" = "0" ]; then
	%service hostapd stop
	/sbin/chkconfig --del hostapd
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%dir %{_sysconfdir}/hostap
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hostap/*
%attr(755,root,root) /sbin/*
%attr(754,root,root) /etc/rc.d/init.d/hostapd
