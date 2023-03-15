# zig neither sets build-id nor allows to override the linker flags
# ziglang/zig#3047
%undefine  _missing_build_ids_terminate_build

Name:           river
Version:        0.2.4
Release:        1%{?dist}
Summary:        Dynamic tiling Wayland compositor

# river: GPLv3+
# protocols: ISC, MIT
License:        GPLv3+ and ISC and MIT
URL:            https://github.com/riverwm/river
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz.sig
# Isaac Freund <mail@isaacfreund.com>
Source2:        https://isaacfreund.com/public_key.txt#/gpgkey-86DED400DDFD7A11.gpg

Source3:        https://raw.githubusercontent.com/nani8ot/river-copr/main/river.desktop
Source4:        https://raw.githubusercontent.com/nani8ot/river-copr/main/river-run.sh

BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  scdoc
BuildRequires:  zig >= 0.10
BuildRequires:  zig-rpm-macros

BuildRequires:  libevdev-devel
BuildRequires:  libinput
BuildRequires:  pixman-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  wayland-devel
BuildRequires:  wlroots >= 0.16.0
BuildRequires:  wlroots-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  pkgconf-pkg-config

# bundled sources
Provides:       bundled(zig-pixman)
Provides:       bundled(zig-wayland)
Provides:       bundled(zig-wlroots)
Provides:       bundled(zig-xkbcommon)

# Lack of graphical drivers may hurt the common use case
Recommends:     mesa-dri-drivers
# Logind needs polkit to create a graphical session
Recommends:     polkit
# Compatibility layer for X11 applications
Recommends:     xorg-x11-server-Xwayland

%description
river is a dynamic tiling wayland compositor that takes inspiration
from dwm and bspwm.

Design goals:
 * Simplicity and minimalism, river should not overstep the bounds
   of a window manager.
 * Window management based on a stack of views and tags.
 * Dynamic layouts generated by external, user-written executables.
   (A default rivertile layout generator is provided.)
 * Scriptable configuration and control through a custom wayland
   protocol and separate riverctl binary implementing it.

%package        protocols-devel
Summary:        Protocol files for the river wayland compositor
License:        MIT

%description    protocols-devel
%{summary}.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup


%build
%zig_build \
   -Dxwayland


%install
%zig_install \
   -Dxwayland
install -D -m755 -pv example/init %{buildroot}%{_datadir}/%{name}/init.example
install -D -m644 -pv %{SOURCE3} %{buildroot}%{_datadir}/wayland-sessions/%{name}.desktop
install -D -m755 -pv %{SOURCE4} %{buildroot}%{_bindir}/%{name}-run.sh


%check
%zig_test


%files
%license LICENSE
%doc README.md
%{_bindir}/river
%{_bindir}/riverctl
%{_bindir}/rivertile
%{_bindir}/%{name}-run.sh
%{_mandir}/man1/river.1*
%{_mandir}/man1/riverctl.1*
%{_mandir}/man1/rivertile.1*
%{_datadir}/%{name}/init.example
%{_datadir}/wayland-sessions/%{name}.desktop
# shell completions
%{_datadir}/bash-completion/completions/riverctl
%dir %{_datadir}/fish
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/riverctl.fish
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_riverctl

%files protocols-devel
%{_datadir}/pkgconfig/river-protocols.pc
%dir %{_datadir}/river-protocols
%{_datadir}/river-protocols/*.xml

%changelog
* Sat Feb 05 2022 Aleksei Bavshin <alebastr@fedoraproject.org> 0.1.3-1
- Update to 0.1.3

* Wed Feb 02 2022 Aleksei Bavshin <alebastr@fedoraproject.org> 0.1.2-2
- Preparing for package review

* Fri Dec 31 2021 Aleksei Bavshin <alebastr@fedoraproject.org> 0.1.2-1
- Update to 0.1.2

* Thu Dec 23 2021 Aleksei Bavshin <alebastr@fedoraproject.org> 0.1.1-1
- Update to 0.1.1

* Wed Nov 03 2021 Aleksei Bavshin <alebastr@fedoraproject.org> 0.1.0-2
- Verify source signature

* Wed Nov 03 2021 Aleksei Bavshin <alebastr@fedoraproject.org> 0.1.0-1
- Update to 0.1.0 release 🎉

* Fri Jun 25 2021 Aleksei Bavshin <alebastr89@gmail.com> 0~20210624git5056394-1
- Initial package
