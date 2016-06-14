%global _pkgdescription A python library for manipulation of the proposed module metadata format.

Name:           modulemd
Version:        0
Release:        5%{?dist}
Summary:        Module metadata manipulation library
License:        MIT
URL:            https://pagure.io/fm-metadata
Source0:        modulemd.tar
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python3-devel
BuildRequires:  PyYAML
BuildRequires:  python3-PyYAML

%description
%{_pkgdescription}

%package -n python2-%{name}
Summary:        %{summary}
Requires:       PyYAML
Provides:       python-%{name} = %{version}-%{release}

%description -n python2-%{name}
%{_pkgdescription}

%package -n python3-%{name}
Summary:        %{summary}
Requires:       python3-PyYAML

%description -n python3-%{name}
%{_pkgdescription}

%prep
%setup -q

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%check
%{__python2} setup.py test
%{__python3} setup.py test

%files -n python2-%{name}
%doc README.rst spec.yaml
%{python2_sitelib}/*

%files -n python3-%{name}
%doc README.rst spec.yaml
%{python3_sitelib}/*

%changelog
* Tue Jun 14 2016 Petr Šabata <contyk@redhat.com> - 0-5
- Rename metadata.yaml to spec.yaml

* Tue Jun 14 2016 Petr Šabata <contyk@redhat.com> - 0-4
- New metadata format
   - rpms/api now holds the module RPM-defined API

* Fri Jun 10 2016 Petr Šabata <contyk@redhat.com> - 0-3
- New metadata format
  - rpms/dependencies defaults to False
  - rpms/fulltree was removed

* Thu May 12 2016 Petr Šabata <contyk@redhat.com> - 0-2
- New metadata format, rationale is now required

* Fri May 06 2016 Petr Šabata <contyk@redhat.com> - 0-1
- New metadata format

* Mon May 02 2016 Petr Šabata <contyk@redhat.com> - 0-0
- This package was build automatically.
