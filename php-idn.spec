%define modname idn
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A26_%{modname}.ini

Summary:	Provides a interface to GNU Libidn for PHP
Name:		php-%{modname}
Version:	1.2b
Release:	%mkrel 29
Group:		Development/PHP
License:	PHP License
URL:		http://php-idn.bayour.com/
Source0:	http://php-idn.bayour.com/idn_%{version}.tar.bz2
Patch0:		idn-1.1-lib64.diff
Patch1:		idn-1.2b-php53.diff
Patch2:		idn_1.2b-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	idn-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Binding to the GNU libidn for using Internationalized Domain Names.


%prep

%setup -q -n idn-%{version}
%patch0 -p0
%patch1 -p1
%patch2 -p0

%build
%serverbuild

phpize --clean; phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .
chrpath -d %{soname}

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}

[idn]

idn.allow_unassigned_chars = "0"
idn.default_charset = "ISO-8859-1"
idn.use_std_3_ascii_rules = "0"

EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc README* entities reference tests CREDITS THANX_TO idn.php
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-29mdv2012.0
+ Revision: 797080
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-28
+ Revision: 761257
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-27
+ Revision: 696433
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-26
+ Revision: 695408
- rebuilt for php-5.3.7

* Wed Apr 27 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-25
+ Revision: 659574
- P1: Catch NULL return from idn() (fixes upstream #330)

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-23mdv2010.1
+ Revision: 514560
- rebuilt for php-5.3.2

* Mon Feb 22 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-22mdv2010.1
+ Revision: 509466
- rebuild
- rebuild

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-20mdv2010.1
+ Revision: 485259
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-19mdv2010.1
+ Revision: 468086
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-18mdv2010.0
+ Revision: 451216
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1:1.2b-17mdv2010.0
+ Revision: 397537
- Rebuild

* Wed May 13 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-16mdv2010.0
+ Revision: 375359
- rebuilt against php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-15mdv2009.1
+ Revision: 346504
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-14mdv2009.1
+ Revision: 341509
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-13mdv2009.1
+ Revision: 321736
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-12mdv2009.1
+ Revision: 310218
- rebuilt against php-5.2.7

* Tue Jul 15 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-11mdv2009.0
+ Revision: 235821
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-10mdv2009.0
+ Revision: 200109
- rebuilt against php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-9mdv2008.1
+ Revision: 161952
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-8mdv2008.1
+ Revision: 107569
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-7mdv2008.0
+ Revision: 77457
- rebuilt against php-5.2.4

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-6mdv2008.0
+ Revision: 64301
- use the new %%serverbuild macro

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-5mdv2008.0
+ Revision: 39383
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-4mdv2008.0
+ Revision: 33778
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-3mdv2008.0
+ Revision: 21027
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.2b-2mdv2007.0
+ Revision: 117667
- rebuilt against new upstream php version (5.2.1)

* Tue Dec 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.2b-1mdv2007.1
+ Revision: 91165
- 1.2b

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1-10mdv2007.0
+ Revision: 78197
- fix deps
- rebuilt for php-5.2.0

* Thu Nov 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1-8mdv2007.1
+ Revision: 75233
- Import php-idn

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1-8
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1-7mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1-6mdk
- rebuilt for php-5.1.4

* Fri May 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1-5mdk
- rebuilt for php-5.1.3

* Thu Feb 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1-4mdk
- new group (Development/PHP) and iurt rebuild

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1-3mdk
- rebuilt against php-5.1.2

* Tue Nov 29 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.1-2mdk
- rebuilt against php-5.1.1

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.1-1mdk
- rebuilt against php-5.1.0
- fix versioning

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_1.1-0.RC1.2mdk
- rebuilt to provide a -debug package too

* Sun Oct 02 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_1.1-0.RC1.1mdk
- rebuilt against php-5.1.0RC1

* Wed Sep 07 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.5_1.1-1mdk
- rebuilt against php-5.0.5 (Major security fixes)

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_1.1-1mdk
- rename the package

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_1.1-1mdk
- 5.0.4

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_1.1-4mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_1.1-3mdk
- rebuilt against a non hardened-php aware php lib

* Sun Jan 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_1.1-2mdk
- rebuild due to hardened-php-0.2.6

* Sun Dec 19 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_1.1-1mdk
- 1.1
- use the source by Turbo Fredriksson and Simon Josefsson instead

* Fri Dec 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_0.1-1mdk
- rebuilt for php-5.0.3

* Sat Sep 25 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.2_0.1-1mdk
- rebuilt for php-5.0.2

* Tue Aug 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.1_0.1-1mdk
- use the pecl source as Turbo Fredriksson and Simon Josefssons 
  code won't compile at all...
- built for php-5.0.1

* Mon Aug 09 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_1.0-4mdk
- rebuilt against latest libidn

* Mon Aug 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_1.0-2mdk
- rebuilt against latest libidn

* Thu Jul 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_1.0-1mdk
- rebuilt for php-4.3.8

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_1.0-2mdk
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7-1mdk
- rebuilt for php-4.3.7

* Thu May 27 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_1.0-1mdk
- 1.0
- drop P0, it's included

* Wed May 26 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_0.9-1mdk
- use the source by Turbo Fredriksson and Simon Josefsson instead
- added P0

* Mon May 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_0.1-2mdk
- use the %%configure2_5x macro
- move scandir to /etc/php.d

* Thu May 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_0.1-1mdk
- initial cooker contrib

