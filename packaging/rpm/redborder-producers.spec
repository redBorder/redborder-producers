%define _redborder_producers_release 1
Name:     redborder-producers
Version:  %{__version}
Release:  %{__release}%{?dist}
Summary:  RedBorder Producers Package
License:  GNU AGPLv3
Group:   Development/Libraries
URL:  https://github.com/redBorder/%{name}
Source0: %{name}-%{version}.tar.gz

BuildRequires: python3
BuildRequires: python3-pip
BuildRequires: python3-setuptools

%global debug_package %{nil}

%description
%{summary}

%prep
%setup -q -n %{name}-%{version}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/%{name}
mkdir -p %{buildroot}/usr/lib/redborder/bin
mkdir -p %{buildroot}/usr/lib/redborder/producers/py/
mkdir -p %{buildroot}/usr/lib/redborder/producers/json/
mkdir -p target
touch target/%{name}-%{version}-selfcontained.jar
install -D -m 644 target/%{name}-%{version}-selfcontained.jar %{buildroot}/usr/share/%{name}
ln -s /usr/share/%{name}/%{name}-%{version}-selfcontained.jar %{buildroot}/usr/lib/redborder/%{name}.jar
install -D -m 755 rb_start_synthetic_producers.sh %{buildroot}/usr/lib/redborder/bin/rb_start_synthetic_producers.sh
install -D -m 755 producers/py/*.py %{buildroot}/usr/lib/redborder/producers/py/
install -D -m 644 producers/json/*.json %{buildroot}/usr/lib/redborder/producers/json/
pip3 install -r requirements.txt

%clean
rm -rf %{buildroot}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d / -s /sbin/nologin \
    -c "User of %{name} service" %{name}
exit 0

%files
%defattr(755,root,root)
/usr/lib/redborder/bin/rb_start_synthetic_producers.sh
/usr/lib/redborder/producers/py/*.py
%defattr(644,root,root)
/usr/share/%{name}
/usr/lib/redborder/%{name}.jar
/usr/lib/redborder/producers/json/*.json

%changelog
* Thu Jan 16 2025 Luis Blanco <ljblanco@redborder.com> - 0.0.2-1
- renaming the paths. Split python code and json files.
* Tue Dec 17 2024 Luis Blanco <ljblanco@redborder.com> - 0.0.1-1
- first spec version
