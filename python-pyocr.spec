# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?__python2: %global __python2 %__python}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global prjname pyocr

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{prjname}
Version:        0.4.2
Release:        1%{?dist}
Summary:        An optical character recognition (OCR) tool wrapper for python

License:        gplv3+
URL:            https://github.com/jflesch/%{prjname}
Source0:        https://github.com/jflesch/%{prjname}/archive/%{version}/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-pillow-devel
BuildRequires:  python-six
BuildRequires:  tesseract-devel
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-pillow-devel
BuildRequires:  python3-six
%endif # with python3

%description
PyOCR is an optical character recognition (OCR) tool wrapper for
python. That is, it helps using OCR tools from a Python program.

It has been tested only on GNU/Linux systems. It should also work on
similar systems (*BSD, etc). It may or may not work on Windows,
MacOSX, etc.

PyOCR can be used as a wrapper for google's Tesseract-OCR or
Cuneiform. It can read all image types supported by Pillow, including
jpeg, png, gif, bmp, tiff, and others. It also support bounding box
data.

%if %{with python3}
%package -n python3-%{prjname}
Summary:        %{summary}

%description -n python3-%{prjname}
%{summary}

%endif # with python3


%prep
%autosetup -c
mv %{prjname}-%{version} python2

%if %{with python3}
cp -a python2 python3
%endif # with python3


%build
pushd python2
%{__python2} setup.py build
popd

%if %{with python3}
pushd python3
%{__python3} setup.py build
popd
%endif # with python3


%install
rm -rf $RPM_BUILD_ROOT
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with python3}
pushd python3
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with python3

pushd python2
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd


# %check
# pushd python2
# %{__python2} setup.py test
# popd

# %if %{with python3}
# pushd python3
# %{__python3} setup.py test
# popd
# %endif


%files
%license python2/COPYING
%doc python2/README.markdown python2/AUTHORS python2/ChangeLog
%{python2_sitelib}/*

%if %{with python3}
%files -n python3-%{prjname}
%license python3/COPYING
%doc python3/README.markdown python3/AUTHORS python3/ChangeLog
%{python3_sitelib}/*
%endif # with python3


%changelog
* Fri Nov 18 2016 James Davidson <james@greycastle.net> - 0.4.2-1
- Update to 0.4.2

* Sun Aug 28 2016 James Davidson <james@greycastle.net>
- Initial packaging
