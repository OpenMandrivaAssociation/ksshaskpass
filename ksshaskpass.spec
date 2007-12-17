Summary:	SSH-askpass for KDE
Name:		ksshaskpass
Version:	0.3
Release:	%mkrel 3
License:	GPL
Group:		Networking/Remote access
Source:		http://hanz.nl/download/ksshaskpass-%{version}.tar.gz
Url:		http://hanz.nl/
Patch0:		ksshaskpass-desktop.patch
BuildRequires:	kdelibs-devel
Requires:	openssh-clients
Requires:	ksshagent

%description
A KDE version of ssh-askpass with KWallet support.

%prep
%setup -qn %{name}-%{version}
%patch0 -p0 -b .desktop

%build

%configure2_5x \
    --enable-final \
    --enable-nmcheck \
    --enable-pch \
    --disable-rpath \
    --with-qt-libraries=%{_prefix}/lib/qt3/%{_lib}

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

%find_lang %{name}

%post
%{update_menus}
%if %mdkversion >= 200700
%{update_desktop_database}
%update_icon_cache hicolor
%endif

%postun
%{clean_menus}
%if %mdkversion >= 200700
%{clean_desktop_database}
%clean_icon_cache hicolor
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING
%attr(755,root,root)%{_bindir}/%{name}
%dir %{_datadir}/doc/HTML/en/%{name}
%{_datadir}/applnk/Utilities/%{name}.desktop
%{_datadir}/doc/HTML/en/%{name}/*
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png


