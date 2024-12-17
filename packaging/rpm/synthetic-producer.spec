Name:     synthetic-producer
Version:  %{__version}
Release:  %{__release}%{?dist}

License:  GNU AGPLv3
URL:  https://github.com/redBorder/%{name}
Source0: %{name}-%{version}.tar.gz

BuildRequires: python3

%global debug_package %{nil}

Summary: %{name} 

%description
%{summary}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/%{name}
mkdir -p %{buildroot}/etc/%{name}/config

cp -f synthetic-producer.py %{buildroot}/usr/share/%{name}
cp -f config/*.yml %{buildroot}/etc/%{name}/config/

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
%defattr(644,root,root)

%changelog
* Mon Jul 15 2024 Luis Blanco <ljblanco@redborder.com> - 1.5.0-1
- first spec version