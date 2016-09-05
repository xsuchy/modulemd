%global _pkgdescription A python library for manipulation of the proposed module metadata format.

Name:           modulemd
Version:        0
Release:        11%{?dist}
Summary:        Module metadata manipulation library
License:        MIT
URL:            https://pagure.io/fm-metadata
# there is no upstream tar file, you can build SRPM directly by running:
# mock -r fedora-rawhide-x86_64 --scm-enable --scm-option method=git --scm-option package=modulemd --scm-option git_get=set --scm-option spec=package/modulemd.spec    --scm-option branch=master --scm-option write_tar=True --scm-option git_get='git clone https://pagure.io/modulemd.git'
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

This is python2 bindings.

%package -n python3-%{name}
Summary:        %{summary}
Requires:       python3-PyYAML

%description -n python3-%{name}
%{_pkgdescription}

This is python3 bindings

%package -n modlint
Summary:        Tool for checking common errors in modulemd files
Requires:       PyYAML
Provides:       python-%{name} = %{version}-%{release}

%description -n modlint
modlint is a tool for checking common errors in modulemd files.

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
%license LICENSE
%{python2_sitelib}/*

%files -n python3-%{name}
%doc README.rst spec.yaml
%license LICENSE
%{python3_sitelib}/*

%files -n modlint
%doc README.rst spec.yaml
%license LICENSE
%{_bindir}/modlint

%changelog
* Wed Aug 03 2016 Jan Kaluza <jkaluza@redhat.com> - 0-11
- Add modlint subpackage

* Tue Jul 19 2016 Petr Šabata <contyk@redhat.com> - 0-10
- Don't fail validation tests
- Use safe_dump() for dumping YAMLs

* Tue Jul 12 2016 Petr Šabata <contyk@redhat.com> - 0-9
- Profiles now support description
- The components section is now truly optional

* Sat Jul 09 2016 Petr Šabata <contyk@redhat.com> - 0-8
- rpms.update_package() now allows updating just one property

* Thu Jun 30 2016 Petr Šabata <contyk@redhat.com> - 0-7
- Adding support for binary package filters

* Tue Jun 21 2016 Petr Šabata <contyk@redhat.com> - 0-6
- New metadata format
   - module use-case profiles are now supported

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
