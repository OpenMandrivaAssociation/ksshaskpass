Summary:	SSH-askpass for KDE
Name:		ksshaskpass
Version:	0.4.1
Release:	%mkrel 2
License:	GPLv2+
Group:		Networking/Remote access
Source0:	http://www.kde-apps.org/CONTENT/content-files/50971-ksshaskpass-%{version}.tar.gz
Patch0:		ksshaskpass-0.4-mdv-fix_exit.patch
Url:		http://www.kde-apps.org/content/show.php?content=50971
BuildRequires:	kdelibs-devel
BuildRequires:	cmake
Requires:	openssh-clients
Requires:	ksshagent
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
A KDE version of ssh-askpass with KWallet support.

%prep
%setup -qn %{name}-%{version}

%build
%cmake
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
install -D -m0755 build/src/%{name} %{buildroot}%{_libdir}/ssh/%name
install -D src/%name.1 %buildroot%_mandir/man1/%name.1

%post
update-alternatives --install %{_libdir}/ssh/ssh-askpass ssh-askpass %{_libdir}/ssh/%{name} 40
update-alternatives --install %{_bindir}/ssh-askpass bssh-askpass %{_libdir}/ssh/%{name} 40

%postun
[ $1 = 0 ] || exit 0
update-alternatives --remove ssh-askpass %{_libdir}/ssh/%{name}
update-alternatives --remove bssh-askpass %{_libdir}/ssh/%{name}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc TODO ChangeLog
%attr(755,root,root)%{_libdir}/ssh/%{name}
%{_mandir}/man1/*
