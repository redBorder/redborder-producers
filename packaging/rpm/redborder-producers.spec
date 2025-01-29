%define _redborder_producers_release 1

Name:    redborder-producers
Version: %{__version}
Release: %{_redborder_producers_release}%{?dist}
Summary: This project is a collection of producers for the redborder platform.

Group: Development/Libraries
License: GNU AGPLv3
URL:  https://github.com/redBorder/%{name}
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gcc, make
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-pip
BuildRequires: python3-setuptools
BuildRequires: jq
BuildRequires: coreutils
BuildRequires: rpm-build

Requires: bash
Requires: python3
Requires: pip
Requires: python3-setuptools
Requires: jq
Requires: coreutils

%define debug_package %{nil}

%description
%{summary}

%prep
%setup -qn %{name}-%{version}

%install
# Directorios base
mkdir -p %{buildroot}/usr/lib/redborder/bin
mkdir -p %{buildroot}/usr/lib/redborder/producers/py
mkdir -p %{buildroot}/usr/lib/redborder/producers/json
mkdir -p %{buildroot}/usr/share/%{name}

install -m 755 resources/bin/rb_producer_simulator.sh %{buildroot}/usr/lib/redborder/bin/
install -m 755 resources/bin/rb_producer_simulator.rb %{buildroot}/usr/lib/redborder/bin/

install -m 755 resources/producers/py/at1_reconocimiento_scan.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/at2_resource_development_ssl.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/at3.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/at5_persistence_backdoor.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/at6.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/at7_defense_evasion.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/at8_credential_access.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/at9_discovery.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/at10_lateral_movement.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/at11_collection_screen.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/at12_cnc.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/at13_exfiltration_dropbox.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/at14_impact_ransom.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/mitre_wide_attack.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/monitor.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/producer_traffic.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/scanner.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/traffic.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 755 resources/producers/py/vault.py %{buildroot}/usr/lib/redborder/producers/py/

install -m 644 resources/producers/py/vulnerability.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 644 resources/producers/py/assets.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 644 resources/producers/py/device.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 644 resources/producers/py/producer.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 644 resources/producers/py/weight.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 644 resources/producers/py/sensors.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 644 resources/producers/py/monitor_event.py %{buildroot}/usr/lib/redborder/producers/py/


install -m 644 resources/json/*.json %{buildroot}/usr/lib/redborder/producers/json/

install -m 644 requirements.txt %{buildroot}/usr/lib/redborder/producers/

%files
%defattr(755,root,root)
/usr/lib/redborder/bin/rb_producer_simulator.sh
/usr/lib/redborder/bin/rb_producer_simulator.rb

/usr/lib/redborder/producers/py/at1_reconocimiento_scan.py
/usr/lib/redborder/producers/py/at2_resource_development_ssl.py
/usr/lib/redborder/producers/py/at3.py
/usr/lib/redborder/producers/py/at5_persistence_backdoor.py
/usr/lib/redborder/producers/py/at6.py
/usr/lib/redborder/producers/py/at7_defense_evasion.py
/usr/lib/redborder/producers/py/at8_credential_access.py
/usr/lib/redborder/producers/py/at9_discovery.py
/usr/lib/redborder/producers/py/at10_lateral_movement.py
/usr/lib/redborder/producers/py/at11_collection_screen.py
/usr/lib/redborder/producers/py/at12_cnc.py
/usr/lib/redborder/producers/py/at13_exfiltration_dropbox.py
/usr/lib/redborder/producers/py/at14_impact_ransom.py
/usr/lib/redborder/producers/py/mitre_wide_attack.py
/usr/lib/redborder/producers/py/monitor.py
/usr/lib/redborder/producers/py/producer_traffic.py
/usr/lib/redborder/producers/py/scanner.py
/usr/lib/redborder/producers/py/traffic.py
/usr/lib/redborder/producers/py/vault.py

%defattr(644,root,root)
/usr/share/%{name}
/usr/lib/redborder/producers/json/*.json
/usr/lib/redborder/producers/py/vulnerability.py
/usr/lib/redborder/producers/py/assets.py
/usr/lib/redborder/producers/py/device.py
/usr/lib/redborder/producers/py/weight.py
/usr/lib/redborder/producers/py/producer.py
/usr/lib/redborder/producers/py/sensors.py
/usr/lib/redborder/producers/py/monitor_event.py

/usr/lib/redborder/producers/requirements.txt

%post
pip install -r /usr/lib/redborder/producers/requirements.txt

%changelog
* Thu Jan 16 2025 Luis Blanco <ljblanco@redborder.com> - 0.0.2-1
- Improved file permissions and added missing dependencies.
- Corrected installation paths for Python and JSON files.
- Removed unnecessary %clean section.
* Tue Dec 17 2024 Luis Blanco <ljblanco@redborder.com> - 0.0.1-1
- Initial spec file version.
