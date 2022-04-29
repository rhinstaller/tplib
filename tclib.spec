Name:           python-tclib
Version:        1.0.0
Release:        1%{?dist}
Summary:        Library for test cases, test plans

License:        BSD
Source0:        %\{name}-%\{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
BuildRequires:  python3-tox
BuildRequires:  python3-wheel

%global _description %{expand:
A python library for test cases, test plans, and requirements stored
in yaml files.}

%description %_description

%package -n python3-tclib
Summary:        %{summary}

%if 0%{?rhel} < 9
Requires:  python3-jinja2
Requires:  python3-pyyaml
%endif

%description -n python3-tclib %_description

%prep
%autosetup -p1 -n tclib-%{version}

%if 0%{?fedora} > 30 || 0%{?rhel} > 8
# for fedora and potentially epel9
%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files tclib

%check
%tox
%pyproject_check_import tclib

%files -n python3-tclib -f %{pyproject_files}
/usr/bin/*
%doc README.*

%else
# for epel8
%build
%py3_build

%install
%py3_install

%check

%files -n python3-tclib
/usr/bin/*
%{python3_sitelib}/tclib/
%{python3_sitelib}/tclib-*.egg-info/
%doc README.*
%endif

%changelog
* Fri Apr 29 2022 Marta Lewandowska <mlewando@redhat.com> 1.0.0-1
- new package built with tito

