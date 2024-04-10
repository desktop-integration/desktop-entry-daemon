# Generated by rust2rpm 26
%bcond_without check

# prevent library files from being installed
%global cargo_install_lib 0

%global crate xdg-temp-daemon

%global ver ###
%global commit ###
%global date ###

Name:           xdg-temp-daemon
Version:        %{ver}~%{date}
Release:        %autorelease
Summary:        A daemon for managing temporary XDG data

SourceLicense:  Apache-2.0
# FIXME: paste output of %%cargo_license_summary here
License:        # FIXME
# LICENSE.dependencies contains a full license breakdown

URL:            https://github.com/ryanabx/xdg-temp-daemon
Source:         xdg-temp-daemon-%{ver}.tar.xz
Source:         xdg-temp-daemon-%{ver}-vendor.tar.xz

BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  rustc
BuildRequires:  cargo
BuildRequires:  just

BuildRequires:  systemd-rpm-macros

Requires:       dbus

%global _description %{expand:
%{summary}.}

%description %{_description}

%prep
%autosetup -n %{crate}-%{ver} -p1 -a1
%cargo_prep -N
cat .vendor/config.toml >> .cargo/config

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}

%install
install -Dm0755 target/release/xdg-temp-daemon %{buildroot}/%{_libexecdir}/xdg-temp-daemon
install -Dm0644 data/xdg-temp-daemon.profile.d.in %{buildroot}/%{_sysconfdir}/profile.d/xdg-temp-daemon.sh
install -Dm0644 data/xdg-temp-daemon.service.in %{buildroot}/%{_userunitdir}/xdg-temp-daemon.service
install -Dm0644 data/xdg-temp-daemon-clean.service.in %{buildroot}/%{_userunitdir}/xdg-temp-daemon-clean.service

%if %{with check}
%check
%cargo_test
%endif

%post
%systemd_post %{name}.service
%systemd_post %{name}-clean.service

%preun
%systemd_preun %{name}.service
%systemd_preun %{name}-clean.service

%postun
%systemd_postun_with_restart %{name}.service
%systemd_postun_with_restart %{name}-clean.service

%files
%license LICENSE
%license LICENSE.dependencies
# %%license cargo-vendor.txt
%doc README.md
%{_libexecdir}/%{name}
%{_userunitdir}/%{name}.service
%{_userunitdir}/%{name}-clean.service
%{_sysconfdir}/profile.d/%{name}.sh

%changelog
%autochangelog
