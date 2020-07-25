# Server-wide NordVPN configuration for Fedora 32, and later

Automates creation of RPM packages that install configuration files for
setting up server-wide (not user-specific) OpenVPN connections.

## Prerequisites

You need to have git, rpm-build, and rpmdevtools packages installed, first:

```
dnf install git rpm-build rpmdevtools
```

Then clone or download this project.

## Building an RPM package with OpenVPN configuration files and scripts

This repository does not include any OpenVPN configuration files, they'll
get downloaded in the next step. In the directory where this project is
downloaded

```
make dist
```

This downloads OpenVPN configuration files into ***ovpn.zip*** and creates
***nordvpn.tar.gz***, which is used to build the installable package:

```
rpmbuild -ta nordvpn.tar.gz
```

This produces the "nordvpn" noarch package. Its version is the current date
and time, install it, as root:

```
rpm -ivh .../RPMS/noarch/nordvpn-YYYMMDDHHMMSS*
```

### Installing an updated package

```
make clean
make dist
rpmbuild -ta nordvpn.tar.gz
rpm -UvhF .../RPMS/noarch/nordvpn-YYYMMDDHHMMSS*
```

"make dist", by itself, uses the previously-downloaded OpenVPN configuration
files, "make clean" removes it first, and "make dist" downloads a new copy.

## Prerequisites for installing a VPN connection

You need to know two things, first:

1) Your server's main connection and router.

This is only needed if you want the OpenVPN connection to come up
automatically when restarting, however the configuration script always
needs it, for simplicity.

If your server has one static IP address and router, the configuration script
will figure it out. If your server has multiple IP addresses or gets a
DHCP-assigned address:

```
$ nmcli connection show
NAME                    UUID                                  TYPE      DEVICE
WAN                     4ca5fc24-7299-3ddc-8760-81522258369c  ethernet  enp6s0
```

If only one connection is listed, this must be it. Otherwise you need to
figure it out.

2) Which VPN server to connect to.

## Configuring a new VPN connection

As root, go to /usr/share/nordvpn and find your server's .ovpn file, then
install it, as root:

```
nmcli connection import type openvpn file <filename>
```

This will show the new connection name, and it now appears in the output
of "nmcli connection show", too.

Important: there's an open SELinux bug, and you must fix the SELinux
context before proceeding any further:

```
restorecon -R /root/.cert
```

This only needs to be done after installing the ovpn file the first time.

Finally, finish setting up the VPN connection by running the "installvpn"
script that this RPM package installs:

```
installvpn [connection] [main]
```

The first parameter is the name of the new VPN connection. The second
parameter is the server's main Internet connection. If the server has
a static IP address the second parameter is optional.

This script asks a few questions, then finishes the configuration:

* Your VPN connection username and password

* Whether to use the VPN-provided DNS servers, or keep your /etc/resolv.conf
as is, when connected to the VPN

* Whether to automatically connect, when the main connection comes up (when
booting).

That's it. To update any of these settings, just run the script again.
