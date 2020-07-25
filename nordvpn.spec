Name:		nordvpn
Version:	%(date '+%%Y%%m%%d%%H%%M%%S')
Release:	1%{?dist}
Summary:	NordVPN configuration
Source0:	https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip
Source1:        nordvpn.tar.gz
License:        Distributable
BuildArch:      noarch

%description
NordVPN configuration files and setup script

%prep
%setup -c
%{__tar} xzvf %SOURCE1

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/nordvpn
%{__mkdir_p} $RPM_BUILD_ROOT%{_sbindir}
%{__cp} -pr ovpn_tcp ovpn_udp $RPM_BUILD_ROOT%{_datadir}/nordvpn
%{__cp} -p installvpn $RPM_BUILD_ROOT%{_sbindir}
%{__chmod} 555 $RPM_BUILD_ROOT%{_sbindir}/installvpn

%files
%{_datadir}/nordvpn
%{_sbindir}/*

%changelog
* Wed Jul 22 2020 Sam Varshavchik <mrsam@courier-mta.com>
- Initial
