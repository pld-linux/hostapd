%define rel	1

Summary:	HostAP - acts as an access point
Summary(es):	HostAP - actúa como un punto de acceso
Summary(pl):	HostAP - praca jako access point
Name:		hostapd
Version:	0.1.0
Release:	%{rel}
License:	GPL
Group:		Daemons
Source0:	http://hostap.epitest.fi/releases/%{name}-%{version}.tar.gz
# Source0-md5:	6be6bb611ee624c66d94dbca104721e9
Source1:	%{name}.init
Patch0:		%{name}-config.patch
URL:		http://hostap.epitest.fi/
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRequires:	kernel-headers
Requires:	kernel-net-hostap >= 0.1.2
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains utilities and userspace daemon for the Linux
driver for wireless LAN cards based on Intersil's Prism2/2.5/3
chipset. The driver supports a so called Host AP mode, i.e., it takes
care of IEEE 802.11 management functions in the host computer and acts
as an access point. This does not require any special firmware for the
wireless LAN card. In addition to this, it has support for normal
station operations in BSS and possible also in IBSS.

%description -l es
Este paquete contiene unas herramientas y un servidor del espacio de
usuario para tarjetas LAN inalámbricas basadas en el chipset Intersil
Prism2/2.5/3. El driver soporta el llamado modo Host AP, es decir, se
encarga de las funciones administrativas el el host, actuando como
"access point". Ello no requiere ningún firmware especial para la
tarjeta LAN inalámbrica. Además, también hay soporte para operaciones
normales de estación en BSS y posiblemente también en IBSS.

%description -l pl
Ten pakiet zawiera narzêdzia oraz demona dzia³aj±cego w przestrzeni
u¿ytkownika dla linuksowego sterownika kart sieci bezprzewodowych
opartych na uk³adach Intersil Prism2/2.5/3. Sterownik obs³uguje tak
zwany tryb Host AP, czyli dba o funkcje zarz±dzaj±ce IEEE 802.11 na
komputerze i dzia³a jako access point. Nie wymaga to ¿adnego
specjalnego firmware dla karty sieci bezprzewodowej. Ponadto ma
obs³ugê normalnych operacji stacyjnych w BSS, a byæ mo¿e tak¿e IBSS.

%prep
%setup -q
%patch0 -p1
%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/sbin,%{_sysconfdir}/{hostap,pcmcia}}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

#hostapd
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/hostapd
install hostapd $RPM_BUILD_ROOT/sbin

#hostapd configuration
install hostapd.accept $RPM_BUILD_ROOT%{_sysconfdir}/hostap
install hostapd.conf $RPM_BUILD_ROOT%{_sysconfdir}/hostap
install hostapd.deny $RPM_BUILD_ROOT%{_sysconfdir}/hostap

%post
/sbin/chkconfig --add hostapd
if [ -r /var/lock/subsys/hostapd ]; then
	/etc/rc.d/init.d/hostapd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/hostapd start\" to start HostAP daemons."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/hostapd ]; then
		/etc/rc.d/init.d/hostapd stop >&2
	fi
	/sbin/chkconfig --del hostapd
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%dir %{_sysconfdir}/hostap
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/hostap/*
%attr(755,root,root) /sbin/hostapd
%attr(754,root,root) /etc/rc.d/init.d/hostapd
