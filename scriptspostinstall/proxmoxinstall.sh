#!/bin/sh

# Installer Proxmox sur un Debian

# Modifie le fichier /etc/hosts

adrip=$(hostname -I)
nom=$(hostname)
nomcomplet=$(hostname -f)

cat <<EOF > /etc/hosts
127.0.0.1	localhost
$adrip	$nomcomplet	$nom

# The following lines are desirable for IPv6 capable hosts
::1	localhost ip6-localhost ip6-loopback
ff02::1	ip6-allnodes
ff02::2	ip6-allrouters
EOF


# Ajoute le proxmox VE dépôt :
echo "deb http://download.proxmox.com/debian/pve stretch pve-no-subscription" > /etc/apt/sources.list.d/pve-install-repo.list

#Ajoute la clé pour le dépôt :
wget http://download.proxmox.com/debian/proxmox-ve-release-5.x.gpg -O /etc/apt/trusted.gpg.d/proxmox-ve-release-5.x.gpg

# On met à jour les dépôts et le système :
apt update -y
apt dist-upgrade -y

# On installe proxmox VE
debconf-set-selections <<< "postfix postfix/mailname string $nomcomplet"
debconf-set-selections <<< "postfix postfix/main_mailer_type string 'Local Only'"

apt install -y proxmox-ve postfix open-iscsi


# On enlève os-prober
apt remove -y os-prober

