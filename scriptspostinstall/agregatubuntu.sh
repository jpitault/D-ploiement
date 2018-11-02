#!/bin/bash

# Créer un lien LACP sur 2 interfaces / Ubuntu

# On récupère le nom des 2 premières interfaces réseaux sans lo
# On les mets dans var[0] et var[1]
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

# On prend la MAC de la première carte
macaddr=$(cat /sys/class/net/${var[0]}/address)

# On écrit le fichier qui contient la configuration des 2 cartes physiques
cat <<EOF > /etc/netplan/01-netcfg.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ${var[0]}:
      dhcp4: false
      optional: true
    ${var[1]}:
      dhcp4: false
      optional: true
EOF

# On écrit le fichier de configuration pour le bond
cat <<EOF > /etc/netplan/bonding.yaml
network:
  version: 2
  renderer: networkd
  bonds:
    bond0:
      dhcp4: true
      interfaces:
        - ${var[0]}
        - ${var[1]}
      parameters:
        mode: 802.3ad
        mii-monitor-interval: 100
      macaddress: $macaddr
EOF

# Maintenant on dit à netplan d'activer la conf
netplan generate
netplan apply
