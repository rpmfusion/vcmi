Name:           vcmi
Summary:        Heroes of Might and Magic 3 game engine
URL:            https://vcmi.eu/

%global fuzzylite_commit  7aee562d6ca17f3cf42588ffb5116e03017c3c50
%global fuzzylite_scommit %(c=%{fuzzylite_commit}; echo ${c:0:7})
%global fuzzylite_version 6.0


Version:        1.3.1
Release:        2%{?dist}

# vcmi is GPLv2+, fyzzylight is GPLv3
License:        GPLv2+ and GPLv3

Source0:        https://github.com/vcmi/vcmi/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/fuzzylite/fuzzylite/archive/%{fuzzylite_commit}/fuzzylite-%{fuzzylite_scommit}.tar.gz

Patch0:         fix_ffmpeg_suffix.patch

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
BuildRequires:  libappstream-glib
%ifnarch ppc64le
# luajit does not support ppc64le
BuildRequires:  luajit-devel
%endif
BuildRequires:  minizip-ng-devel
BuildRequires:  tbb-devel
BuildRequires:  zlib-devel
BuildRequires:  ffmpeg-devel
%if 0%{?fedora} >= 39
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  qt6-linguist
%else
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-linguist
%endif

Requires:       hicolor-icon-theme
Requires:       %{name}-data = %{version}-%{release}
Provides:       bundled(fuzzylight) = %{fuzzylite_version}

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
%autosetup -p1
# fuzzyight from Source1:
tar -xf %{SOURCE1} -C AI/FuzzyLite --strip-components=1

dos2unix README.md license.txt AUTHORS ChangeLog.md

# Don't show GITDIR-NOTFOUND in the window title
sed -i 's/GITDIR-NOTFOUND/%{version}/' cmake_modules/*

%build

%cmake -Wno-dev \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DENABLE_TEST=0 \
  -UCMAKE_INSTALL_LIBDIR \
  -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON \
  -DCMAKE_INSTALL_RPATH=%{_libdir}/%{name}

%ifnarch %{ix86} x86_64 aarch64
# not enough memory in Koji for parallel build
%global _smp_mflags -j1
%endif
%cmake_build


%install
%cmake_install


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/eu.vcmi.VCMI.metainfo.xml

%ldconfig_scriptlets


%files
%doc README.md AUTHORS ChangeLog.md
%license license.txt AI/FuzzyLite/LICENSE.FuzzyLite
%{_bindir}/vcmieditor
%{_bindir}/vcmiclient
%{_bindir}/vcmiserver
%{_bindir}/vcmibuilder
%{_bindir}/vcmilauncher
%{_libdir}/%{name}/

# keep this in the main package, because GNOME Software etc.
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/vcmiclient.png
%{_datadir}/icons/hicolor/*/apps/vcmiclient.svg
%{_datadir}/icons/hicolor/*/apps/vcmieditor.png
%{_metainfodir}/eu.vcmi.VCMI.metainfo.xml


%files data
%{_datadir}/%{name}/



%changelog
* Thu Aug 31 2023 Trung Lê <8@tle.id.au> - 1.3.1-2
- Rebuilt with Qt6 for Fedora 39

* Sat Aug 19 2023 Trung Lê <8@tle.id.au> - 1.3.1-1
- New upstream release
- Re-enable support for ppc64le

* Mon Aug 14 2023 Trung Lê <8@tle.id.au> - 1.3.0-1
- New upstream release
- Clean up defunct codes

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 02 2023 Leigh Scott <leigh123linux@gmail.com> - 1.0.0-3
- Rebuild for new boost

* Wed Feb 08 2023 Leigh Scott <leigh123linux@gmail.com> - 1.0.0-2
- rebuilt

* Wed Sep 14 2022 Leigh Scott <leigh123linux@gmail.com> - 1.0.0-1
- New upstream release

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.99^20190113gitf06c8a8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.99^20190113gitf06c8a8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.99^20190113gitf06c8a8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 18 2021 Leigh Scott <leigh123linux@gmail.com> - 0.99^20190113gitf06c8a8-4
- Rebuild for new libminizip

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.99^20190113gitf06c8a8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan  1 2021 Leigh Scott <leigh123linux@gmail.com> - 0.99^20190113gitf06c8a8-2
- Rebuilt for new ffmpeg snapshot

* Tue Sep 29 2020 Miro Hrončok <mhroncok@redhat.com> - 0.99^20190113gitf06c8a8-1
- Update to a git snapshot to support new Boost
- Use RPATH to make it launch :/
- Declare the bundled FuzzyLite
- Rebuilt for Boost 1.73
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

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
