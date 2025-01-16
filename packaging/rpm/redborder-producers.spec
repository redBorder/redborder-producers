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
Requires: python3-setuptools
Requires: jq
Requires: coreutils

%define debug_package %{nil}

%description
%{summary}

%prep
%setup -qn %{name}-%{version}

%build

%install
# Directorios base
mkdir -p %{buildroot}/usr/lib/redborder/bin
mkdir -p %{buildroot}/usr/lib/redborder/producers/py
mkdir -p %{buildroot}/usr/lib/redborder/producers/json
mkdir -p %{buildroot}/usr/share/%{name}

install -m 755 resources/bin/rb_start_synthetic_producers.sh %{buildroot}/usr/lib/redborder/bin/
install -m 755 resources/producers/py/*.py %{buildroot}/usr/lib/redborder/producers/py/
install -m 644 resources/json/*.json %{buildroot}/usr/lib/redborder/producers/json/

%files
%defattr(755,root,root)
/usr/lib/redborder/bin/rb_start_synthetic_producers.sh
/usr/lib/redborder/producers/py/*.py

%defattr(644,root,root)
/usr/share/%{name}
/usr/lib/redborder/producers/json/*.json

%changelog
* Thu Jan 16 2025 Luis Blanco <ljblanco@redborder.com> - 0.0.2-1
- Improved file permissions and added missing dependencies.
- Corrected installation paths for Python and JSON files.
- Removed unnecessary %clean section.
* Tue Dec 17 2024 Luis Blanco <ljblanco@redborder.com> - 0.0.1-1
- Initial spec file version.
