%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)
#define git 20240222
%define gitbranch Plasma/6.0
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")

Summary:	SSH-askpass for KDE
Name:		plasma6-ksshaskpass
Version:	6.2.5
Release:	%{?git:0.%{git}.}1
License:	GPLv2+
Group:		Networking/Remote access
%if 0%{?git:1}
Source0:	https://invent.kde.org/plasma/ksshaskpass/-/archive/%{gitbranch}/ksshaskpass-%{gitbranchd}.tar.bz2#/ksshaskpass-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/%{stable}/plasma/%(echo %{version} |cut -d. -f1-3)/ksshaskpass-%{version}.tar.xz
%endif
Url:		https://www.kde-apps.org/content/show.php?content=50971
# (tpg) https://issues.openmandriva.org/show_bug.cgi?id=1459
Source1:	ssh-askpass-gnome.png
BuildRequires:	cmake(KF6I18n)
BuildRequires:	cmake(KF6Pty)
BuildRequires:	cmake(KF6Wallet)
BuildRequires:	cmake(KF6CoreAddons)
BuildRequires:	cmake(KF6WidgetsAddons)
BuildRequires:	cmake(KF6DocTools)
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(ECM)
Requires:	openssh-clients
Requires(post,postun):	chkconfig
Requires(post):	openssh-askpass-common

%description
A KDE version of ssh-askpass with KWallet support.

%prep
%autosetup -p1 -n ksshaskpass-%{?git:%{gitbranchd}}%{?!git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
%find_lang ksshaskpass || touch ksshaskpass.lang

# (tpg) https://issues.openmandriva.org/show_bug.cgi?id=1459
install -m644 -D %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/ssh-askpass-gnome.png

# Setup environment variables
mkdir -p %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/env/
cat > %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/env/ksshaskpass.sh << EOF
SSH_ASKPASS=%{_bindir}/ksshaskpass
export SSH_ASKPASS
EOF

%post
update-alternatives --install %{_libdir}/ssh/ssh-askpass ssh-askpass %{_bindir}/ksshaskpass 60
update-alternatives --install %{_bindir}/ssh-askpass bssh-askpass %{_bindir}/ksshaskpass 60

%postun
[ $1 = 0 ] || exit 0
update-alternatives --remove ssh-askpass %{_bindir}/ksshaskpass
update-alternatives --remove bssh-askpass %{_bindir}/ksshaskpass

%triggerin -- ksshaskpass < 0.5
update-alternatives --remove ssh-askpass %{_libdir}/ssh/ksshaskpass
update-alternatives --remove bssh-askpass %{_libdir}/ssh/ksshaskpass

%files -f ksshaskpass.lang
%doc ChangeLog README
%config(noreplace) %{_sysconfdir}/xdg/plasma-workspace/env/ksshaskpass.sh
%{_bindir}/*
%{_datadir}/pixmaps/ssh-askpass-gnome.png
%{_datadir}/applications/org.kde.ksshaskpass.desktop
%doc %{_mandir}/man1/*
