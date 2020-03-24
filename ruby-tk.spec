# TODO
# - how to pass optflags through rake?
#   (currently it uses flags hardcoded from ruby build)
#
# Conditional build:
%bcond_without	doc	# ri/rdoc documentation

%define pkgname tk
Summary:	Tk interface module using tcltklib
Summary(pl.UTF-8):	Moduł interfejsu Tk wykorzystujący tcltklib
Name:		ruby-tk
Version:	0.2.0
Release:	2
Epoch:		2
License:	BSD or Ruby
#Source0Download: https://github.com/ruby/tk/releases
Source0:	https://github.com/ruby/tk/archive/v%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	bbf9aca2e1954c2bb3b2aa28b227f61c
Group:		Development/Languages
URL:		https://github.com/ruby/tk
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	ruby-bundler
BuildRequires:	ruby-rubygems
BuildRequires:	ruby-rake
BuildRequires:	sed >= 4.0
Requires:	ruby-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tk interface module using tcltklib.

%description -l pl.UTF-8
Moduł interfejsu Tk wykorzystujący tcltklib.

%package examples
Summary:	Examples for Ruby Tk module
Summary(pl.UTF-8):	Przykłady do modułu Ruby Tk
Group:		Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description examples
Examples for Ruby Tk module.

%description examples -l pl.UTF-8
Przykłady do modułu Ruby Tk.

%package rdoc
Summary:	HTML documentation for Ruby Tk module
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla modułu języka Ruby Tk
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for Ruby Tk module.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla modułu języka Ruby Tk.

%package ri
Summary:	ri documentation for Ruby Tk module
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla modułu języka Ruby Tk
Group:		Documentation
Requires:	ruby-doc-ri

%description ri
ri documentation for Ruby Tk module.

%description ri -l pl.UTF-8
Dokumentacja w formacie ri dla modułu języka Ruby Tk.

%prep
%setup -q -n %{pkgname}-%{version}

%{__sed} -i -e '1s,/usr/bin/env *ruby,%{__ruby},' \
	bin/* \
	lib/tkextlib/pkg_checker.rb \
	sample/{safe-tk,tkoptdb-safeTk}.rb

# substitite 
grep -q 'spec\.files.*`git ls-files' tk.gemspec
%{__sed} -i -e '/spec\.files/ { s/git ls-files -z/cat .tk_files/; s/\\x0/\\n/ }' tk.gemspec
find -type f ! -name .tk_files | sed -e 's,^\./,,' > .tk_files

%build
# make gemspec self-contained
ruby -r rubygems -e 'spec = eval(File.read("%{pkgname}.gemspec"))
	File.open("%{pkgname}-%{version}.gemspec", "w") do |file|
	file.puts spec.to_ruby_for_cache
end'
%{__rm} tk.gemspec

rake

%if %{with doc}
rdoc --ri --op ri lib
rdoc --op rdoc lib
%{__rm} ri/Object/cdesc-Object.ri
%{__rm} ri/lib/page-README.ri
%{__rm} ri/created.rid
%{__rm} ri/cache.ri
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{ruby_vendorarchdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorarchdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%{__mv} $RPM_BUILD_ROOT%{ruby_vendorarchdir}/README README.tk
%{__mv} $RPM_BUILD_ROOT%{ruby_vendorarchdir}/tkextlib/tcllib/README README.tcllib
%{__mv} $RPM_BUILD_ROOT%{ruby_vendorarchdir}/tkextlib/tkimg/README README.tkimg

%if %{with doc}
install -d $RPM_BUILD_ROOT{%{ruby_rdocdir}/%{name}-%{version},%{ruby_ridir}}
cp -a rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
%endif

# install examples
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a sample/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BSDL ChangeLog.tkextlib LICENSE.txt MANUAL_tcltklib.eng README.{1st,fork,md,tcllib,tk,tkimg}
%lang(ja) %doc MANUAL_tcltklib.ja
%attr(755,root,root) %{ruby_vendorarchdir}/tcltklib.so
%attr(755,root,root) %{ruby_vendorarchdir}/tkutil.so
%{ruby_vendorarchdir}/multi-tk.rb
%{ruby_vendorarchdir}/remote-tk.rb
%{ruby_vendorarchdir}/tcltk.rb
%{ruby_vendorarchdir}/tk*.rb
%{ruby_vendorarchdir}/tk
%{ruby_vendorarchdir}/tkextlib
%{ruby_specdir}/tk-%{version}.gemspec

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Arc
%{ruby_ridir}/Bitmap
%{ruby_ridir}/BitmapImage
%{ruby_ridir}/Checkbutton
%{ruby_ridir}/CloneMenu
%{ruby_ridir}/Font
%{ruby_ridir}/Grid
%{ruby_ridir}/INTERP
%{ruby_ridir}/Labelframe
%{ruby_ridir}/Line
%{ruby_ridir}/MenuButton
%{ruby_ridir}/MultiTkIp*
%{ruby_ridir}/Object/TkNamedVirtualEvent
%{ruby_ridir}/Object/TkSystemMenu
%{ruby_ridir}/Object/Ttk
%{ruby_ridir}/Object/Tk*.ri
%{ruby_ridir}/Object/Mainloop-i.ri
%{ruby_ridir}/Object/__method_missing_alias_for_MultiTkIp__-i.ri
%{ruby_ridir}/Object/check_pkg-i.ri
%{ruby_ridir}/Object/get_pkg_list-i.ri
%{ruby_ridir}/Object/help_msg-i.ri
%{ruby_ridir}/Object/method_missing-i.ri
%{ruby_ridir}/Object/subdir_check-i.ri
%{ruby_ridir}/OptionMenuButton
%{ruby_ridir}/Oval
%{ruby_ridir}/Pack
%{ruby_ridir}/Panedwindow
%{ruby_ridir}/PhotoImage
%{ruby_ridir}/Place
%{ruby_ridir}/Polygon
%{ruby_ridir}/Radiobutton
%{ruby_ridir}/Rectangle
%{ruby_ridir}/RemoteTkIp
%{ruby_ridir}/Selection
%{ruby_ridir}/Spinbox
%{ruby_ridir}/TclTk*
%{ruby_ridir}/TextItem
%{ruby_ridir}/Tk*
%{ruby_ridir}/Variable
%{ruby_ridir}/VirtualEvent
%{ruby_ridir}/WindowItem
%{ruby_ridir}/Winfo
%{ruby_ridir}/lib/tkextlib
%endif
