# Note:  Some tests for this package are disabled by default, as they
# require network access and would thus fail in the buildsys' mock
# environments.  To build locally while enabling tests, either:
#
#   rpmbuild ... --define '_with_network_tests 1' ...
#   rpmbuild ... --with network_tests ...
#   define _with_network_tests 1 in your ~/.rpmmacros
#
# Note that right now, the only way to run tests locally from a cvs sandbox
# "make noarch" type scenario is the third one.
%global real_version   0.81

Name:           perl-DateTime-Format-Builder
# 0.80 in reality, but rpm can't get it
Version:        0.8100
Release:        15%{?dist}
Summary:        Create DateTime parser classes and objects        

Group:          Development/Libraries
# examples/W3CDTF.pm:               GPL+ or Artistic
# lib/DateTime/Format/Builder.pm:   Artistic 2.0
License:        Artistic 2.0 and (GPL+ or Artistic)
URL:            http://search.cpan.org/dist/DateTime-Format-Builder            
Source0:        http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/DateTime-Format-Builder-%{real_version}.tar.gz        

BuildArch: noarch
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

## core
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
## non-core
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Class::ISA)
BuildRequires:  perl(Class::Factory::Util)
BuildRequires:  perl(DateTime)
BuildRequires:  perl(DateTime::Format::Strptime)
BuildRequires:  perl(Params::Validate) >= 0.73
# note -- listed as a BR but _not_ needed with Fedora perl
#BuildRequires:  perl(Task::Weaken)
BuildRequires:  perl(Test::Pod)
## For extended testing
BuildRequires:  perl(DateTime::Format::HTTP)
BuildRequires:  perl(DateTime::Format::Mail)
BuildRequires:  perl(DateTime::Format::IBeat)
Provides:       perl(DateTime::Format::Builder) = %{version}

# for signature checking
%{?_with_network_tests:BuildRequires: perl(Module::Signature) }

%{?perl_default_filter}

%description
DateTime::Format::Builder creates DateTime parsers. Many string formats of
dates and times are simple and just require a basic regular expression to
extract the relevant information. Builder provides a simple way to do this
without writing reams of structural code.

Builder provides a number of methods, most of which you'll never need, or at
least rarely need. They're provided more for exposing of the module's innards
to any subclasses, or for when you need to do something slightly beyond what
is expected.


%prep
%setup -q -n DateTime-Format-Builder-%{real_version}

# digital signature checking.  Not essential, but nice
%{?_with_network_tests: cpansign -v }

# POD doesn't like E<copy> very much...
perl -pi -e 's/E<copy>/(C)/' `find lib/ -type f`

# silence rpmlint
sed -i '1s~^#!.*perl~#!%{__perl}~' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor 
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +

%{_fixperms} %{buildroot}/*


%check
make test


%files
%doc Changes LICENSE README examples/ t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Thu Jul 12 2018 Petr Pisar <ppisar@redhat.com> - 0.8100-15
- Correct license tag (bug #1600504)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8100-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8100-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.8100-12
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8100-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.8100-10
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8100-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8100-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.8100-7
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.8100-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8100-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8100-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 0.8100-3
- Perl 5.18 rebuild

* Fri Apr 05 2013 Iain Arnell <iarnell@gmail.com> 0.8100-2
- license change from "same as perl" to Artistic 2.0

* Fri Apr 05 2013 Iain Arnell <iarnell@gmail.com> 0.8100-1
- update to latest upstream version
- drop dependency filtering

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8000-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8000-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.8000-9
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8000-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.8000-7
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.8000-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8000-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8000-4
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Dec 12 2010 Iain Arnell <iarnell@gmail.com> 0.8000-3
- use perl_default_filter
- clean up spec for modern rpmbuild

* Fri May 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8000-2
- add provides with rpm version for other packages

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8000-1
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.7901-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7901-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7901-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.7901-2
- rebuild for new perl

* Sat Jan 26 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.7901-1
- update to 0.7901
- additional docs
- some spec rework

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.7807-4
- bump for mass rebuild

* Tue Aug 08 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.7807-3
- bump for release & build, not in that order

* Tue Aug 08 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.7807-2
- additional br's

* Fri Aug 04 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.7807-1
- Initial spec file for F-E
