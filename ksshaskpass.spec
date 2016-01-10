%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)

Summary:	SSH-askpass for KDE
Name:		ksshaskpass
Version:	5.5.3
Release:	2
License:	GPLv2+
Group:		Networking/Remote access
Source0:	http://download.kde.org/%{stable}/plasma/%{version}/ksshaskpass-%{version}.tar.xz
Url:		http://www.kde-apps.org/content/show.php?content=50971
Requires:	openssh-clients
# (tpg) https://issues.openmandriva.org/show_bug.cgi?id=1459
Requires:	openssh-askpass-gnome
BuildRequires:	cmake(KF5I18n)
BuildRequires:	cmake(KF5Pty)
BuildRequires:	cmake(KF5Wallet)
BuildRequires:	cmake(KF5CoreAddons)
BuildRequires:	cmake(KF5WidgetsAddons)
BuildRequires:	cmake(KF5DocTools)
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Gui)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	cmake(ECM)

%description
A KDE version of ssh-askpass with KWallet support.

%prep
%setup -q
%cmake_kde5

%build
%ninja -C build

%install
%ninja_install -C build
%find_lang ksshaskpass

%post
update-alternatives --install %{_libdir}/ssh/ssh-askpass ssh-askpass %{_bindir}/%{name} 40
update-alternatives --install %{_bindir}/ssh-askpass bssh-askpass %{_bindir}/%{name} 40

%postun
[ $1 = 0 ] || exit 0
update-alternatives --remove ssh-askpass %{_bindir}/%{name}
update-alternatives --remove bssh-askpass %{_bindir}/%{name}

%triggerin -- ksshaskpass < 0.5
update-alternatives --remove ssh-askpass %{_libdir}/ssh/%{name}
update-alternatives --remove bssh-askpass %{_libdir}/ssh/%{name}

%files -f ksshaskpass.lang
%doc ChangeLog COPYING INSTALL README
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_mandir}/man1/*
