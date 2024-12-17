%global _redborder-producers_release 1
Name:     redborder-producers
Version:  %{__version}
Release:  %{__release}%{?dist}
License:  GNU AGPLv3
Group:   Development/Libraries
URL:  https://github.com/redBorder/%{name}
Source0: %{name}-%{version}.tar.gz

BuildRequires: python3

%global debug_package %{nil}

%description
%{summary}

%prep
%setup -q -n %{name}-%{version}

%install
rm -rf %{buildroot}
# mkdir -p %{buildroot}/usr/share/%{name}
# mkdir -p %{buildroot}/usr/lib/redborder
# install -D -m 644 target/%{name}-%{version}-selfcontained.jar %{buildroot}/usr/share/%{name}
# ln -s /usr/share/%{name}/%{name}-%{version}-selfcontained.jar %{buildroot}/usr/lib/redborder/%{name}.jar


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
# /usr/share/%{name}
# /usr/lib/redborder/%{name}.jar

%changelog
* Tue Dec 17 2024 Luis Blanco <ljblanco@redborder.com> - 0.0.1-1
- first spec version