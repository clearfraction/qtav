%global debug_package %{nil}
%global commit0 df5bf45926c15960e2a75822bf051c8431d91385
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

%define ffmpeg_include -I%(pkg-config --variable=includedir libavutil)

Name:           qtav
Version:        1.13.0
Release:        1
Summary:        Qt multimedia framework
License:        LGPLv2 AND GPLv3
Group:          Applications/Multimedia
URL:            http://qtav.org/
Source0:	https://github.com/wang-bin/QtAV/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:	qtav.appdata.xml

BuildRequires:  ImageMagick-dev
BuildRequires:  dos2unix
BuildRequires:  hicolor-icon-theme
BuildRequires:  appstream-glib-dev
BuildRequires:	desktop-file-utils
BuildRequires:  qtbase-dev
BuildRequires:  portaudio-dev
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5OpenGL)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavdevice)
BuildRequires:  pkgconfig(libavfilter)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavresample)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libpulse) >= 1.0
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(xv)
BuildRequires:	ffmpeg-dev 

%description
QtAV is a multimedia playback library based on Qt and FFmpeg. It can help
facilitate writing a player application.


%package        devel
Summary:        Development package for %{name}
Requires:       %{name} = %{version}-%{release}

%description  devel
QtAV is a multimedia playback library based on Qt and FFmpeg.

This package contains the header development files for building some QtAV
applications using QtAV headers.

%prep
%setup -n QtAV-%{commit0}

# We need put the path of our ffmpeg
find . -type f -name \*.pro | while read FILE; do
echo "QMAKE_CXXFLAGS_RELEASE += %{ffmpeg_include}" >> "$FILE"; done

# Fix incorrect sRGB profile
for f in $(find . -type f -name \*.png); do
convert $f -strip $f
done

%build
qmake "CONFIG+=no_rpath recheck" QMAKE_CXXFLAGS+=-fno-lto
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}


find %{buildroot} -name \*.a -exec rm {} \;


# duplicate files
rm -rf  %{buildroot}/usr/share/doc

# Appdata
mkdir -p %{buildroot}/%{_datadir}/{applications,metainfo}
install -Dm 0644 %{SOURCE1} %{buildroot}/usr/share/metainfo/%{name}.appdata.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/Player.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/QMLPlayer.desktop
appstream-util validate-relax --nonet %{buildroot}/usr/share/metainfo/*.appdata.xml

%files
%license gpl-3.0* lgpl-2.1*
%doc Changelog README*
/usr/bin/Player
/usr/bin/QMLPlayer
/usr/share/applications/Player.desktop
/usr/share/applications/QMLPlayer.desktop
/usr/share/icons/hicolor/scalable/apps/QtAV.svg
/usr/lib64/libQtAV.so.*
/usr/lib64/libQtAVWidgets.prl
/usr/lib64/libQtAVWidgets.so.*
/usr/lib64/qt5/mkspecs/
/usr/lib64/qt5/qml/QtAV/
/usr/share/metainfo/qtav.appdata.xml

%files devel
/usr/include/qt5/QtAV/
/usr/include/qt5/QtAVWidgets/
/usr/lib64/libQtAV.so
/usr/lib64/libQtAVWidgets.so
/usr/lib64/qt5/mkspecs/
/usr/lib64/libQtAVWidgets.prl
/usr/lib64/libQtAV.prl


%changelog
* Tue Jan 28 2020 David Va <davidva AT tuta DOT io> 1.13.0-1
- Spec file adapted of URPMs for CF
