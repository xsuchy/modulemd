%global _pkgdescription A python library for manipulation of the proposed module metadata format.

Name:           modulemd
Version:        0
Release:        0%{?dist}
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
%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
%{_pkgdescription}

%package -n python3-%{name}
Summary:        %{summary}
Requires:       python3-PyYAML
%{?python_provide:%python_provide python3-%{name}}

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
%doc README.rst metadata.yaml
%{python2_sitelib}/*

%files -n python3-%{name}
%doc README.rst metadata.yaml
%{python3_sitelib}/*

%changelog
* Mon May 02 2016 Petr Šabata <contyk@redhat.com> - 0-0
- This package was build automatically.
