Summary:	SSH-askpass for KDE
Name:		ksshaskpass
Version:	0.5.1
Release:	%mkrel 2
License:	GPLv2+
Group:		Networking/Remote access
Source0:	http://www.kde-apps.org/CONTENT/content-files/50971-%name-%version.tar.gz
Url:		http://www.kde-apps.org/content/show.php?content=50971
BuildRequires:	kdelibs4-devel
Requires:	openssh-clients
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
A KDE version of ssh-askpass with KWallet support.

%prep
%setup -qn %{name}-%{version}

%build
%cmake_kde4
%make

%install
rm -fr %buildroot
%makeinstall_std -C build

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog
%_kde_bindir/*
%_kde_applicationsdir/*.desktop
%_mandir/man1/*
