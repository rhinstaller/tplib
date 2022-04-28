Name:           python-tclib
Version:        0.0.0
Release:        0%{?dist}
Summary:        Library for test cases, test plans

License:        BSD
URL:            https://github.com/rhinstaller/tclib
Source:         %{url}/archive/v%{version}/tclib-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  diffutils
BuildRequires:  python3-devel
BuildRequires:  python3-libxml2

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
%doc README.*
%{_bindir}/tclib_greeting


%changelog
