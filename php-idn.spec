%define modname idn
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A26_%{modname}.ini

Summary:	Provides a interface to GNU Libidn for PHP
Name:		php-%{modname}
Version:	1.2b
Release:	%mkrel 5
Group:		Development/PHP
URL:		http://php-idn.bayour.com/
License:	PHP License
Source0:	http://php-idn.bayour.com/idn_%{version}.tar.bz2
Patch0:		idn-1.1-lib64.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	idn-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Binding to the GNU libidn for using Internationalized Domain Names.


%prep

%setup -q -n idn-%{version}
%patch0 -p0

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags}"

%if %mdkversion >= 200710
export CFLAGS="$CFLAGS -fstack-protector"
export CXXFLAGS="$CXXFLAGS -fstack-protector"
export FFLAGS="$FFLAGS -fstack-protector"
%endif

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

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc README* entities reference tests CREDITS THANX_TO idn.php
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}