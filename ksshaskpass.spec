%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)

Summary:	SSH-askpass for KDE
Name:		ksshaskpass
Version:	5.2.95
Release:	1
License:	GPLv2+
Group:		Networking/Remote access
Source0:	ftp://ftp.kde.org/pub/kde/%{stable}/plasma/%{version}/ksshaskpass-%{version}.tar.xz
Url:		http://www.kde-apps.org/content/show.php?content=50971
Requires:	openssh-clients
BuildRequires:	extra-cmake-modules5
BuildRequires:	cmake(KF5I18n)
BuildRequires:	cmake(KF5Pty)
BuildRequires:	cmake(KF5Wallet)
BuildRequires:	cmake(KF5CoreAddons)
BuildRequires:	cmake(KF5WidgetsAddons)
BuildRequires:	cmake(KF5DocTools)
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Gui)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	cmake
BuildRequires:	ninja

%description
A KDE version of ssh-askpass with KWallet support.

%prep
%setup -q

%build
%cmake -G Ninja
ninja

%install
DESTDIR="%{buildroot}" ninja install -C build
%find_lang ksshaskpass

%post
update-alternatives --install %{_libdir}/ssh/ssh-askpass ssh-askpass %{_kde_bindir}/%{name} 40
update-alternatives --install %{_bindir}/ssh-askpass bssh-askpass %{_kde_bindir}/%{name} 40

%postun
[ $1 = 0 ] || exit 0
update-alternatives --remove ssh-askpass %{_kde_bindir}/%{name}
update-alternatives --remove bssh-askpass %{_kde_bindir}/%{name}

%triggerin -- ksshaskpass < 0.5
update-alternatives --remove ssh-askpass %{_libdir}/ssh/%{name}
update-alternatives --remove bssh-askpass %{_libdir}/ssh/%{name}

%files -f ksshaskpass.lang
%defattr(-,root,root,-)
%doc ChangeLog COPYING INSTALL README
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_mandir}/man1/*
