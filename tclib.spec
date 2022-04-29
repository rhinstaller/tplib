Name:           python-tclib
Version:        1.0.0
Release:        1%{?dist}
Summary:        Library for test cases, test plans

License:        BSD
URL:            https://github.com/rhinstaller/tclib
Source:         %{url}/archive/v%{version}/tclib-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  diffutils
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-libxml2
BuildRequires:  python3-pylint
BuildRequires:  python3-sphinx
BuildRequires:  python3-tox
BuildRequires:  python3-wheel

%global _description %{expand:
A python library for test cases, test plans, and requirements stored
in yaml files.}

%description %_description

%package -n python3-tclib
Summary:        %{summary}

%description -n python3-tclib %_description


%prep
%autosetup -p1 -n tclib-%{version}


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


%changelog
* Fri Apr 29 2022 Marta Lewandowska <mlewando@redhat.com> 1.0.0-1
- new package built with tito

