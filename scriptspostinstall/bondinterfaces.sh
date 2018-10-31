#!/bin/bash

apt update
apt install -y ifenslave

# On va chercher le nom des interfaces du système, en oubliant lo
output=$(ls /sys/class/net/)

c=0

for interface in $output
do
	if [ "$interface" != "lo" ]
	then
		var[$c]="$interface"
		c=$(( c +1))
	fi
done

# On utilise var[0] et var[1] pour faire le bond

cat <<EOF > /etc/network/interfaces
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# Interfaces utilisés pour le bond
auto ${var[0]}
iface ${var[0]} inet manual
        mtu 9142

auto ${var[1]}
iface ${var[1]} inet manual
        mtu 9142

auto bond0
iface bond0 inet dhcp
        slaves ${var[0]} ${var[1]}
        bond-mode 802.3ad
        bond-miimon 100

EOF

