%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: iSCSI daemon and utility programs
Name: iscsi-initiator-utils
Version: 6.2.0.872
Release: 10%{?dist}
Source0: http://people.redhat.com/mchristi/iscsi/rhel6.0/source/open-iscsi-2.0-872-rc4-bnx2i.tar.gz
Source1: iscsid.init
Source2: iscsidevs.init
Source3: 04-iscsi
# Add Red Hat specific info to docs.
Patch0: iscsi-initiator-utils-update-initscripts-and-docs.patch
# Upstream uses /etc/iscsi for iscsi db info, but use /var/lib/iscsi.
Patch1: iscsi-initiator-utils-use-var-for-config.patch
# Add redhat.com string to default initiator name.
Patch2: iscsi-initiator-utils-use-red-hat-for-name.patch
# Add a lib for use by anaconda.
Patch3: iscsi-initiator-utils-add-libiscsi.patch
# Add bnx2i support.
Patch4: iscsi-initiator-utils-uip-mgmt.patch
# disable isns for libiscsi (libiscsi does not support isns)
Patch5: iscsi-initiator-utils-disable-isns-for-lib.patch
# fix libiscsi get firmware sysfs init
Patch6: iscsi-initiator-utils-fix-lib-sysfs-init.patch
# fix race between uip and iscsid startup
Patch7: iscsi-initiator-utils-fix-uip-init-race.patch
# Don't compile iscsistart as static
Patch8: iscsi-initiator-utils-dont-use-static.patch
# Fix brcm nic state
Patch9: iscsi-initiator-utils-fix-brcm-nic-state.patch
# Fix iface op return value
Patch10: iscsi-initiator-utils-fix-iface-op-ret-val.patch
# Fix brcm VLAN
Patch11: iscsi-initiator-utils-fix-uip-vlan-support.patch
# Fix brcm 10G wrap
Patch12: iscsi-initiator-utils-fix-uip-10G-wrap.patch
# brcm uIP version Bump
Patch13: iscsi-initiator-utils-fix-uip-rhel-version-bump.patch
# Log message and hint when login failed and using iface binding.
Patch14: iscsi-initiator-utils-log-login-failed.patch

Group: System Environment/Daemons
License: GPLv2+
URL: http://www.open-iscsi.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: openssl-devel flex bison python-devel doxygen

Requires(post): chkconfig
Requires(preun): chkconfig /sbin/service

%description
The iscsi package provides the server daemon for the iSCSI protocol,
as well as the utility programs used to manage it. iSCSI is a protocol
for distributed disk access using SCSI commands sent over Internet
Protocol networks.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n open-iscsi-2.0-872-rc4-bnx2i
%patch0 -p1 -b .update-initscripts-and-docs
%patch1 -p1 -b .use-var-for-config
%patch2 -p1 -b .use-red-hat-for-name
%patch3 -p1 -b .add-libiscsi
%patch4 -p1 -b .uip-mgmt
%patch5 -p1 -b .disable-isns-for-lib
%patch6 -p1 -b .fix-lib-sysfs-init
%patch7 -p1 -b .fix-uip-init-race
%patch8 -p1 -b .dont-use-static
%patch9 -p1 -b .fix-brcm-nic-state
%patch10 -p1 -b .fix-iface-op-ret-val
%patch11 -p1 -b .fix-brcm-vlan
%patch12 -p1 -b .fix-brcm-10G-wrap
%patch13 -p1 -b .fix-brcm-version-bump
%patch14 -p1 -b .log-login-failed

%build
cd utils/open-isns
./configure
make OPTFLAGS="%{optflags}"
cd ../../
make OPTFLAGS="%{optflags}" -C utils/sysdeps
make OPTFLAGS="%{optflags}" -C utils/fwparam_ibft
make OPTFLAGS="%{optflags}" -C usr
make OPTFLAGS="%{optflags}" -C utils
make OPTFLAGS="%{optflags}" -C libiscsi

cd brcm_iscsi_uio
./configure --enable-debug
make OPTFLAGS="%{optflags}"
cd ..

pushd libiscsi
python setup.py build
popd

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT/etc/iscsi
mkdir -p $RPM_BUILD_ROOT/etc/NetworkManager/dispatcher.d
mkdir -p $RPM_BUILD_ROOT/var/lib/iscsi
mkdir -p $RPM_BUILD_ROOT/var/lib/iscsi/nodes
mkdir -p $RPM_BUILD_ROOT/var/lib/iscsi/send_targets
mkdir -p $RPM_BUILD_ROOT/var/lib/iscsi/static
mkdir -p $RPM_BUILD_ROOT/var/lib/iscsi/isns
mkdir -p $RPM_BUILD_ROOT/var/lib/iscsi/slp
mkdir -p $RPM_BUILD_ROOT/var/lib/iscsi/ifaces
mkdir -p $RPM_BUILD_ROOT/var/lock/iscsi
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{python_sitearch}



install -p -m 755 usr/iscsid usr/iscsiadm utils/iscsi-iname usr/iscsistart $RPM_BUILD_ROOT/sbin
install -m 755 brcm_iscsi_uio/src/unix/brcm_iscsiuio $RPM_BUILD_ROOT/sbin
install -p -m 644 doc/iscsiadm.8 $RPM_BUILD_ROOT/%{_mandir}/man8
install -p -m 644 doc/iscsid.8 $RPM_BUILD_ROOT/%{_mandir}/man8
install -p -m 644 doc/iscsistart.8 $RPM_BUILD_ROOT/%{_mandir}/man8
install -p -m 644 doc/iscsi-iname.8 $RPM_BUILD_ROOT/%{_mandir}/man8
install -p -m 644 brcm_iscsi_uio/docs/brcm_iscsiuio.8 $RPM_BUILD_ROOT/%{_mandir}/man8
install -p -m 644 etc/iscsid.conf $RPM_BUILD_ROOT%{_sysconfdir}/iscsi

install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/iscsid
install -p -m 755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/iscsi
install -p -m 755 %{SOURCE3} $RPM_BUILD_ROOT/etc/NetworkManager/dispatcher.d

install -p -m 755 libiscsi/libiscsi.so.0 $RPM_BUILD_ROOT%{_libdir}
ln -s libiscsi.so.0 $RPM_BUILD_ROOT%{_libdir}/libiscsi.so
install -p -m 644 libiscsi/libiscsi.h $RPM_BUILD_ROOT%{_includedir}

install -p -m 755 libiscsi/build/lib.linux-*/libiscsimodule.so \
	$RPM_BUILD_ROOT%{python_sitearch}


%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if [ "$1" -eq "1" ]; then
	if [ ! -f %{_sysconfdir}/iscsi/initiatorname.iscsi ]; then
		echo "InitiatorName=`/sbin/iscsi-iname`" > %{_sysconfdir}/iscsi/initiatorname.iscsi
	fi
	/sbin/chkconfig --add iscsid
	/sbin/chkconfig --add iscsi
fi

%postun -p /sbin/ldconfig

%preun
if [ "$1" = "0" ]; then
	# stop iscsi
	/sbin/service iscsi stop > /dev/null 2>&1
	# delete service
	/sbin/chkconfig --del iscsi
	# stop iscsid
	/sbin/service iscsid stop > /dev/null 2>&1
	# delete service
	/sbin/chkconfig --del iscsid
fi

%files
%defattr(-,root,root)
%doc README
%dir /etc/iscsi
%dir %{_var}/lib/iscsi
%dir %{_var}/lib/iscsi/nodes
%dir %{_var}/lib/iscsi/isns
%dir %{_var}/lib/iscsi/static
%dir %{_var}/lib/iscsi/slp
%dir %{_var}/lib/iscsi/ifaces
%dir %{_var}/lib/iscsi/send_targets
%dir %{_var}/lock/iscsi
%{_initrddir}/iscsi
%{_initrddir}/iscsid
%{_sysconfdir}/NetworkManager
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/iscsi/iscsid.conf
/sbin/*
%{_libdir}/libiscsi.so.0
%{python_sitearch}/libiscsimodule.so
%{_mandir}/man8/*

%files devel
%defattr(-,root,root,-)
%doc libiscsi/html
%{_libdir}/libiscsi.so
%{_includedir}/libiscsi.h

%changelog
* Wed Aug 18 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.10
- 605663 Log message when iface binding, and doc rp_filter settings
  needed for iface binding.

* Mon Aug 5 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.9
- 614035 Make iscsi status print session info.
- Fix uip vlan and 10 gig bugs.

* Mon Jul 26 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.8
- 589256 Re-fix iface update/delete return value.

* Mon Jul 12 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.7
- 595591 Fix nic state bug in brcm_iscsiuio.

* Thu Jul 8 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.6
- 602899 Add discovery db support.
- 595591 Sync brcm_iscsiuio to 0.5.15.
- 589256 Do not log success message and return ENODEV
- 601434 Fix iscsiadm handling of non-default port

* Fri Jun 18 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.5
- 602286 No need to compile iscsistart as static. This also fixes
  the segfault when hostnames are passed in for the portal ip.

* Tue May 18 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.4
- 590580 libiscsi get_firmware_foo does not work without first creating a
  libiscsi context
- 588931 Fix uip and iscsid initialization race
- 570664 Add basic vlan support for bnx2i's brcm uip daemon
- 589761 Fix multiple init script bugs: rh_status does not detect offload,
  start/stop does not work due to iscsiadm output being directed to stderr,
  discovery daemon does not get auto started/stopped, iscsid restart does
  not restart daemon if force-start was used.
- 585649 Fix iscsid "-eq: unary operator expected" bug.

* Wed May 5 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.3
- 578455 Fix initial R2T=0 handling for be2iscsi

* Wed Mar 31 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.2
- 578455 Fix handling of MaxXmitDataSegmentLength=0 for be2iscsi

* Wed Mar 31 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.1
- 578455 Fix handling of MaxXmitDataSegmentLength=0

* Wed Mar 24 2010 Mike Christie <mchristi@redhat.com> 6.2.0.872.0
- 516444 Add iSNS SCN handling (rebased to open-iscsi-2.0-872-rc1-)
- Update brcm to 0.5.7

* Mon Feb 8 2010 Mike Christie <mchristi@redhat.com> 6.2.0.871.1.1-3
- Add spec patch comments.

* Thu Jan 21 2010 Mike Christie <mchristi@redhat.com> 6.2.0.871.1.1-2
- 556985 Fix up init.d iscsid script to remove offload modules and
  load be2iscsi.
- Enable s390/s390x

* Fri Jan 15 2010 Mike Christie <mchristi@redhat.com> 6.2.0.871.1.1-1
- Sync to upstream
- 529324 Add iscsi-iname and iscsistart man page
- 463582 OF/iBFT support

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0.870-10.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Dan Horak <dan[at]danny.cz> 6.2.0.870-9.1
- drop the s390/s390x ExcludeArch

* Mon Apr 27 2009 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-9
- Don't crash when asked to parse the ppc firmware table more then
  once (which can be done from libiscsi) (#491363)

* Fri Apr  3 2009 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-8
- Stop the NM script from exiting with an error status when it
  didn't do anything (#493411)

* Fri Mar 20 2009 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-7
- libiscsi: use fwparam_ibft_sysfs() instead of fw_get_entry(), as
  the latter causes stack corruption (workaround #490515)

* Sat Mar 14 2009 Terje Rosten <terje.rosten@ntnu.no> - 6.2.0.870-6
- Add glibc-static to buildreq to build in F11

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0.870-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-4
- Fix libiscsi.discover_sendtargets python method to accept None as valid
  authinfo argument (#485217)

* Wed Jan 28 2009 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-3
- Fix reading of iBFT firmware with newer kernels

* Wed Jan 28 2009 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-2
- Add libiscsi iscsi administration library and -devel subpackage

* Tue Nov  25 2008 Mike Christie <mchristie@redhat.com> 6.2.0.870-1.0
- Rebase to upstream

* Thu Nov  6 2008 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-0.2.rc1
- Add force-start iscsid initscript option and use that in "patch to make
  iscsiadm start iscsid when needed" so that iscsid will actual be started
  even if there are no iscsi disks configured yet (rh 470437)
- Do not start iscsid when not running when iscsiadm -k 0 gets executed
  (rh 470438)

* Tue Sep 30 2008 Hans de Goede <hdegoede@redhat.com> 6.2.0.870-0.1.rc1
- Rewrite SysV initscripts, fixes rh 441290, 246960, 282001, 436175, 430791
- Add patch to make iscsiadm complain and exit when run as user instead
  of hang spinning for the database lock
- Add patch to make iscsiadm start iscsid when needed (rh 436175 related)
- Don't start iscsi service when network not yet up (in case of using NM)
  add NM dispatcher script to start iscsi service once network is up

* Mon Jun 30 2008 Mike Christie <mchristie@redhat.com> - 6.2.0.870
- Rebase to open-iscsi-2-870
- 453282 Handle sysfs changes.

* Fri Apr 25 2008 Mike Christie <mchristie@redhat.com> - 6.2.0.868-0.7
- 437522 log out sessions that are not used for root during "iscsi stop".

* Fri Apr 4 2008 Mike Christie <mchristie@redhat.com> - 6.2.0.868-0.6
- Rebase to RHEL5 to bring in bug fixes.
- 437522 iscsi startup does not need to modify with network startup.
- 436175 Check for running sessions when stopping service.

* Wed Feb 5 2008 Mike Christie <mchristie@redhat.com> - 6.2.0.868-0.3
- Rebase to upstream and RHEL5.
- 246960 LSB init script changes.

* Fri Oct 5 2007 Mike Christie <mchristie@redhat.com> - 6.2.0.865-0.2
- Rebase to upstream's bug fix release.
- Revert init script startup changes from 225915 which reviewers did
 not like.

* Mon Jun 20 2007 Mike Christie <mchristie@redhat.com> - 6.2.0.754-0.1
- 225915 From Adrian Reber - Fix up spec and init files for rpmlint.

* Tue Feb 6 2007 Mike Christie <mchristie@redhat.com> - 6.2.0.754-0.0
- Rebase to upstream.
- Add back --map functionality but in session mode to match RHEL5 fixes
- Break up iscsi init script into two, so iscsid can be started early for root

* Tue Nov 28 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.747-0.0
- Fix several bugs in actor.c (iscsi scheduling). This should result
- in better dm-multipath intergation and fix bugs where time outs
- or requests were missed or dropped.
- Set default noop timeout correctly.

* Sat Nov 25 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.742-0.0
- Don't flood targets with nop-outs.

* Fri Nov 24 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.737-0.0
- Add commands missing from RHEL4/RHEL3 and document iscsid.conf.
- Fixup README.

* Mon Nov 7 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.695-0.8
- Rebase to upstream open-iscsi-2.0-730.

* Tue Oct 17 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.695-0.7
- Change period to colon in default name

* Thu Oct 5 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.695-0.6
- BZ 209523 make sure the network is not going to get shutdown so
iscsi devices (include iscsi root and dm/md over iscsi) get syncd.
- BZ 209415 have package create iscsi var dirs

* Tue Oct 3 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.695-0.5
- BZ 208864 move /etc/iscsi/nodes and send_targets to /var/lib/iscsi

* Mon Oct 1 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.695-0.4
- BZ 208548 move /etc/iscsi/lock to /var/lock/iscsi/lock

* Wed Sep 27 2006 Jeremy Katz <katzj@redhat.com> - 6.2.0.695-0.3
- Add fix for initscript with pid file moved

* Tue Sep 26 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.695-0.2
- BZ 208050 - change default initiator name to reflect redhat
- Move pid from /etc/iscsi to /var/run/iscsid.pid

* Fri Sep 15 2006 Mike Christie <mchristie@redhat.com> - 6.2.0.695-0.1
- Add compat with FC kernel so iscsid will pass startup checks and run.
- Fix bug when using hw iscsi and software iscsi and iscsid is restarted.
- Fix session matching bug when hw and software iscsi is both running

* Tue Sep  5 2006 Jeremy Katz <katzj@redhat.com> - 6.1.1.685-0.1
- Fix service startup
- Fix another case where cflags weren't being used

* Mon Aug 28 2006 Mike Christie <mchristie@redhat.com> - 6.1.1.685
- Rebase to upstream to bring in many bug fixes and rm db.
- iscsi uses /etc/iscsi instead of just etc now

* Fri Jul 21 2006 Jeremy Katz <katzj@redhat.com> - 6.1.1.645-1
- fix shutdown with root on iscsi

* Thu Jul 13 2006 Mike Christie <mchristie@redhat.com> - 6.1.1.645
- update to upstream 1.1.645
- Note DB and interface changed so you must update kernel, tools and DB

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.0.5.595-2.1.1
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.0.5.595-2.1
- rebuild

* Wed Jun 21 2006 Mike Christie <mchristi@redhat.com> - 6.0.5.595-2
- add PatM's statics.c file. This is needed for boot since 
  there is no getpwuid static available at that time.
* Tue Jun 20 2006 Jeremy Katz <katzj@redhat.com> - 6.0.5.595-1
- ensure that we respect %%{optflags}
- cleaned up initscript to make use of standard functions, return right 
  values and start by default
- build iscsistart as a static binary for use in initrds

* Tue May 30 2006 Mike Christie <mchristi@redhat.com>
- rebase package to svn rev 595 to fix several bugs
  NOTE!!!!!!!! This is not compatible with the older open-iscsi modules
  and tools. You must upgrade.

* Thu May 18 2006 Mike Christie <mchristi@redhat.com>
- update package to open-iscsi svn rev 571
  NOTE!!!!!!!! This is not compatible with the older open-iscsi modules
  and tools. You must upgrade.

* Fri Apr 7 2006 Mike Christie <mchristi@redhat.com>
- From Andy Henson <andy@zexia.co.uk>:
  Autogenerate /etc/initiatorname.iscsi during install if not already present
- Remove code to autogenerate /etc/initiatorname.iscsi from initscript
- From dan.y.roche@gmail.com:
  add touch and rm lock code
- update README
- update default iscsid.conf. "cnx" was not supported. The correct
  id was "conn".

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.0.5.476-0.1
- bump again for double-long bug on ppc(64)

* Mon Jan 23 2006 Mike Christie <mchristi@redhat.com>
- rebase package to bring in ppc64 unsigned long vs unsigned
  long long fix and iscsadm return value fix. Also drop rdma patch
  becuase it is now upstream.
* Wed Dec 14 2005 Mike Christie <mchristi@redhat.com>
- initial packaging

