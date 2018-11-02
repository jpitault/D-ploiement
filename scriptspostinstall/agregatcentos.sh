#!/bin/bash

# Activer un agrégat de lien (LACP) sur 2 cartes réseaux sur centOS


# Maintenant on récupère le nom des 2 premières interfaces réseau
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

# On supprime les lignes qui peuvent exister dans les fichiers de conf
# des interfaces, pour pouvoir les réécrire.
# Ce sont les lignes qui contiennet BOOTPROTO et ONBOOT qui nous intéresse
grep -v "BOOTPROTO" /etc/sysconfig/network-scripts/ifcfg-${var[0]} > temp && mv temp /etc/sysconfig/network-scripts/ifcfg-${var[0]}
grep -v "ONBOOT" /etc/sysconfig/network-scripts/ifcfg-${var[0]} > temp && mv temp /etc/sysconfig/network-scripts/ifcfg-${var[0]}

grep -v "BOOTPROTO" /etc/sysconfig/network-scripts/ifcfg-${var[1]} > temp && mv temp /etc/sysconfig/network-scripts/ifcfg-${var[1]}
grep -v "ONBOOT" /etc/sysconfig/network-scripts/ifcfg-${var[1]} > temp && mv temp /etc/sysconfig/network-scripts/ifcfg-${var[1]}


# On rajoute 4 lignes dans chaque fichier

echo 'BOOTPROTO="none"' >> /etc/sysconfig/network-scripts/ifcfg-${var[0]}
echo 'ONBOOT="yes"' >> /etc/sysconfig/network-scripts/ifcfg-${var[0]}
echo 'MASTER=bond0' >> /etc/sysconfig/network-scripts/ifcfg-${var[0]}
echo 'SLAVE=yes' >> /etc/sysconfig/network-scripts/ifcfg-${var[0]}
echo 'MTU=9142' >> /etc/sysconfig/network-scripts/ifcfg-${var[0]}

echo 'BOOTPROTO="none"' >> /etc/sysconfig/network-scripts/ifcfg-${var[1]}
echo 'ONBOOT="yes"' >> /etc/sysconfig/network-scripts/ifcfg-${var[1]}
echo 'MASTER=bond0' >> /etc/sysconfig/network-scripts/ifcfg-${var[1]}
echo 'SLAVE=yes' >> /etc/sysconfig/network-scripts/ifcfg-${var[1]}
echo 'MTU=9142' >> /etc/sysconfig/network-scripts/ifcfg-${var[1]}

# On active le module bonding
modprobe --first-time bonding


# On créer le fichier de configuration de l'interface bond0
# le mode 4 correspond à 802.3ad
cat <<EOF > /etc/sysconfig/network-scripts/ifcfg-bond0
DEVICE=bond0
NAME=bond0
TYPE=Bond
BONDING_MASTER=yes
ONBOOT=yes
BOOTPROTO=dhcp
BONDING_OPTS="mode=4 miimon=100
EOF

# Maintenant on indique à Network Manager de recharger les fichiers
nmcli con reload

# Pour terminer on redémarre le service Network
systemctl restart network
