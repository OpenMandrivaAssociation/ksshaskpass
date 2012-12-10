Summary:	SSH-askpass for KDE
Name:		ksshaskpass
Version:	0.5.3
Release:	%mkrel 4
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
rm -fr %{buildroot}
%makeinstall_std -C build

# fix .desktop file
# old icon doesn't exist any more
sed -i s,Icon=.*,Icon=dialog-password,g %{buildroot}%{_kde_applicationsdir}/ksshaskpass.desktop

desktop-file-install --vendor=mandriva \
		--remove-key="Encoding" \
		--delete-original \
		--dir=%{buildroot}%{_kde_applicationsdir} %{buildroot}%{_kde_applicationsdir}/ksshaskpass.desktop

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
%doc ChangeLog COPYING INSTALL README
%{_kde_bindir}/*
%{_kde_applicationsdir}/*.desktop
%{_mandir}/man1/*


%changelog
* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.3-4mdv2011.0
+ Revision: 612673
- the mass rebuild of 2010.1 packages

* Wed Apr 21 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.5.3-3mdv2010.1
+ Revision: 537698
- fix icon in the .desktop file

* Tue Jan 05 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.5.3-2mdv2010.1
+ Revision: 486467
- add docs in the package (notably the new README)

* Tue Jan 05 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.5.3-1mdv2010.1
+ Revision: 486465
- update to 0.5.3

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.5.1-2mdv2010.0
+ Revision: 438168
- rebuild

* Sun Nov 30 2008 Funda Wang <fwang@mandriva.org> 0.5.1-1mdv2009.1
+ Revision: 308553
- new version 0.5.1

* Mon Nov 24 2008 Funda Wang <fwang@mandriva.org> 0.5-2mdv2009.1
+ Revision: 306298
- should be triggerin

* Mon Nov 24 2008 Funda Wang <fwang@mandriva.org> 0.5-1mdv2009.1
+ Revision: 306280
- New version 0.5

* Mon Aug 18 2008 Funda Wang <fwang@mandriva.org> 0.4.1-2mdv2009.0
+ Revision: 273372
- patch merged upstream
- add man page

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - update to new version 0.4.1

* Mon May 19 2008 Gustavo De Nardin <gustavodn@mandriva.com> 0.4-1mdv2009.0
+ Revision: 208873
- easier to install the binary in %%install than fixing the Cmake rules
- now buildrequires cmake
- updated to version 0.4
- updated upstream in Url and Source0
- don't package useless desktop file and icons, the app is not run by the user
- don't package unwritten documentation
- no need to update menus
- build with cmake
- P1: put binary in the same place as the other askpass binaries
- P0: fix exit status: must be >0 when the user cancels
- use update alternatives like the other askpass utilities
- updated to current license policy

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0.3-3mdv2008.1
+ Revision: 140918
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Tue Jan 16 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.3-3mdv2007.0
+ Revision: 109508
- fix xdg menu entry
- spec file clean
- add requires

* Wed Jan 03 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.3-2mdv2007.1
+ Revision: 103906
- fix build on x86_64
- Import ksshaskpass

