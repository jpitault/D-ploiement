#!/usr/bin/python3
import re

# Ecrire le kickstart avec des variables

def centosks(mac, mdp_root, nom_user, mdp_user, taille_swap):
	# variables
	# On veut une adresse MAC en minuscule, séparée par "-"
	# On commence par séparer l'adresse MAC dans une list
	listmac = re.findall('[a-fA-F0-9]{2}',mac)
	# Puis on remet en string, séparée par ":"
	mac = "-".join(listmac)
	# On met en minuscule
	mac = mac.lower()

	nom_preseed = '/var/www/html/' + mac + "centos.cfg"


	# On écrit le fichier
	with open(nom_preseed,'w') as fichier:
		fichier.write('install \n')
		fichier.write('url --url http://mirror.centos.org/centos/7.5.1804/os/x86_64/ \n')
		fichier.write('lang en_US.UTF-8 \n')
		fichier.write('keyboard --vckeymap=fr \n')
		fichier.write('unsupported_hardware \n')
		fichier.write('network --bootproto=dhcp \n')
		fichier.write('rootpw {} \n'.format(mdp_root))
		fichier.write('firewall --disabled \n')
		fichier.write('selinux --permissive \n')
		fichier.write('timezone Europe/Paris \n')
		fichier.write('bootloader --location=mbr \n')
		fichier.write('text \n')
		fichier.write('skipx \n')
		fichier.write('zerombr \n')
		fichier.write('clearpart --all --initlabel \n')
		fichier.write('part raid.11 --size=1024 --ondisk=sda \n')
		fichier.write('part raid.12 --size=1024 --ondisk=sdb \n')
		fichier.write('part raid.01 --size=1 --grow --ondisk=sda \n')
		fichier.write('part raid.02 --size=1 --grow --ondisk=sdb \n')
		fichier.write('raid /boot --device=boot --fstype=ext4 --level=1 --label=boot raid.11 raid.12 \n')
		fichier.write('raid pv.01 --level=1 --device=cos7-root --fstype=ext4 --label=cos7-root raid.01 raid.02 \n')
		fichier.write('volgroup centos pv.01 \n')
		fichier.write('logvol swap --fstype=swap --size={} --name=swap --vgname=centos \n'.format(taille_swap))
		fichier.write('logvol / --size=1 --grow --name=root --vgname=centos \n')
		fichier.write('firstboot --disabled \n')
		fichier.write('eula --agreed \n')
		fichier.write('services --enabled=NetworkManager,sshd \n')
		fichier.write('reboot \n')
		fichier.write('user --name={} --plaintext --password {} \n'.format(nom_user, mdp_user))
		fichier.write('repo --name=base --baseurl=http://mirror.centos.org/centos/7.5.1804/os/x86_64/ \n')
		fichier.write('%packages \n')
		fichier.write('@Core \n')
		fichier.write('wget \n')
		fichier.write('-iwl*firmware \n')
		fichier.write('%end \n')
		fichier.write('%post \n')
		fichier.write('echo "Ceci est un test" > /root/test \n')
		fichier.write('wget --output-document=/tmp/agregatcentos.sh http://192.168.0.254/agregatcentos.sh \n')
		fichier.write('bash /tmp/agregatcentos.sh \n')
		fichier.write('grub2-install /dev/sdb \n')
		fichier.write('%end \n')
