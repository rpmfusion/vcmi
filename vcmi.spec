Name:           vcmi
Summary:        Heroes of Might and Magic 3 game engine
Version:        0.99
Release:        10%{?dist}
License:        GPLv2+
URL:            https://vcmi.eu/

Source:         https://github.com/%{name}/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

# Absolutely disgusting and untested patch for compatibility with Boost 1.66
# Courtesy of Robert-André Mauchin during the review
# Sent upstream via https://github.com/vcmi/vcmi/pull/285#issuecomment-370504722
Patch1:             %{name}-boost-1.66.patch

# Enable extra resolutions
# https://forum.vcmi.eu/t/where-is-the-mod-for-resolutions-other-than-800x600/897/5
# https://www.dropbox.com/sh/fwor43x5xrgzx6q/AABpTFqGK7Q9almbyr3hp9jma/mods/vcmi.zip (not directly downloadable)
Source2:            %{name}.zip
Patch2:             %{name}-mods.patch

# Boost 1.69 failures
# tribool casts + https://github.com/vcmi/vcmi/commit/edcaaf036acb76882df2274f4df2aeef3c84525e
Patch3:             %{name}-boost-1.69.patch

# The Koji builder gets killed here, but I don't expect people to use this there
ExcludeArch:    ppc64le

BuildRequires:  %{_bindir}/desktop-file-validate
BuildRequires:  %{_bindir}/dos2unix
BuildRequires:  cmake
BuildRequires:  gcc-c++ >= 4.7.2
BuildRequires:  SDL2-devel
BuildRequires:  SDL2_image-devel
BuildRequires:  SDL2_ttf-devel
BuildRequires:  SDL2_mixer-devel
BuildRequires:  boost >= 1.51
BuildRequires:  boost-devel >= 1.51
BuildRequires:  boost-filesystem >= 1.51
BuildRequires:  boost-iostreams >= 1.51
BuildRequires:  boost-system >= 1.51
BuildRequires:  boost-thread >= 1.51
BuildRequires:  boost-program-options >= 1.51
BuildRequires:  boost-locale >= 1.51
BuildRequires:  zlib-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  ffmpeg-libs
BuildRequires:  qt5-qtbase-devel

Requires:       hicolor-icon-theme
Requires:       %{name}-data = %{version}-%{release}


%description
The purpose of VCMI project is to rewrite entire Heroes 3.5: WoG engine from
scratch, giving it new and extended possibilities. It will help to support
mods and new towns already made by fans but abandoned because of game code
limitations.

In its current state it already supports maps of any sizes, higher
resolutions and extended engine limits.


%package data
Summary:        Data files for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description data
Data files for the VCMI project, a %{summary}.


%prep
%setup -q -a2

%patch1 -p1

# mods from Source2:
mv vcmi/Mods/* Mods && rm -rf vcmi
%patch2 -p1

%patch3 -p1

dos2unix README.md README.linux license.txt AUTHORS ChangeLog


%build
%cmake -DENABLE_TEST=0 -UCMAKE_INSTALL_LIBDIR

%ifarch %{ix86} x86_64
%make_build
%else
# not enough memory in Koji for parallel build
make
%endif


%install
%make_install


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%ldconfig_scriptlets


%files
%doc README.md README.linux AUTHORS ChangeLog
%license license.txt
%{_bindir}/vcmiclient
%{_bindir}/vcmiserver
%{_bindir}/vcmibuilder
%{_bindir}/vcmilauncher
%{_libdir}/%{name}/

# keep this in the main package, because GNOME Software etc.
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/vcmiclient.png

# don't need devel and static packages until requested
%exclude %{_includedir}/fl
%exclude %{_libdir}/*.a


%files data
%{_datadir}/%{name}/



%changelog
* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.99-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 04 2020 Leigh Scott <leigh123linux@gmail.com> - 0.99-9
- Rebuilt for Boost 1.73

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.99-8
- Rebuild for ffmpeg-4.3 git

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.99-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 0.99-6
- Rebuild for new ffmpeg version

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.99-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.99-4
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.99-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Mar 04 2018 Miro Hrončok <mhroncok@redhat.com> - 0.99-2
- Add mods for extra resolutions
- Add %%check with desktop file checking
- Require hicolor-icon-theme and don't own the hicolor dirs
- Fix dos line ends
- Change description and summary
- Use cmake and make macros
- Exclude files instead of not terminating build on unpackaged files
- Add Patch1 for Boost 1.66 compatibility
- Split noarch data into a subpackage
- Own /usr/share/vcmi/ and /usr/lib64/vcmi/

* Tue Nov 01 2016 VCMI - 0.99-1
- New upstream release
