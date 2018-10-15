#!/usr/bin/python3
import re

# On écrit le script d'installation de bsd, en partant du modèle et en changeant les variables
# Il faut que le script de sortie s'appelle : mac-00:11:22:33:44:aa ( définit dans l'image mfsbsd)

def freebsd(mac, taille_swap, nom, mdp_root, nom_user, mdp_user):
	# On vérifie que l'adresse MAC en soit bien une
	X='([a-fA-F0-9]{2}[" ":\-]?){6}'
	ismac = re.compile(X).match(mac)
	if ismac:
		pass
	else:
		print('Adresse MAC invalide. Quitte le script')
		sys.exit



	# On veut une adresse MAC en majuscule, séparée par ":"
	# On commence par séparer l'adresse MAC dans une list
	listmac = re.findall('[a-fA-F0-9]{2}',mac)
	# Puis on remet en string, séparée par ":"
	mac = ":".join(listmac)
	# On met en minuscule
	mac = mac.lower()

	# Nos 2 fichiers
	modele = 'bsdinstallzfs.txt'
	outfile = '/var/www/html/mac-' + mac

	# On lit le modèle et on écrit dans la sortie
	with open(modele,"r") as in_f, open(outfile,"w") as out_f:
		# On lit, ligne par ligne
		for ligne in in_f.readlines():
			if 'SWAP=1G' in ligne:
				out_f.write('SWAP={}M\n'.format(taille_swap))
			elif 'NAME="CastleIT"' in ligne:
				out_f.write('NAME="{}"\n'.format(nom))
			elif 'MDPROOT="insecure"' in ligne:
				out_f.write('MDPROOT="{}"\n'.format(mdp_root))
			elif 'USER="username"' in ligne:
				out_f.write('USER="{}"\n'.format(nom_user))
			elif 'MDPUSER="insecure"' in ligne:
				out_f.write('MDPUSER="{}"\n'.format(mdp_user))
			else:
				out_f.write(ligne)

				
# Ecrire le fichier preseed pour debian				
def debian(mac, mdp_root, nom_user, mdp_user, taille_swap):
	# variables
	# On veut une adresse MAC en minuscule, séparée par "-"
	# On commence par séparer l'adresse MAC dans une list
	listmac = re.findall('[a-fA-F0-9]{2}',mac)
	# Puis on remet en string, séparée par ":"
	mac = "-".join(listmac)
	# On met en minuscule
	mac = mac.lower()

	nom_preseed = '/var/www/html/' + mac + "debian.cfg"


	# On écrit le fichier
	with open(nom_preseed,'w') as fichier:
		fichier.write('d-i debian-installer/locale string en_US\n')
		fichier.write('d-i keyboard-configuration/xkb-keymap select fr(latin9)\n')
		fichier.write('d-i netcfg/choose_interface select auto\n')
		fichier.write('d-i netcfg/get_hostname string deb2pxe\n')
		fichier.write('d-i netcfg/get_domain string unassigned-domain\n')
		fichier.write('d-i netcfg/wireless_wep string\n')
		fichier.write('d-i mirror/country string manual\n')
		fichier.write('d-i mirror/http/hostname string ftp.fr.debian.org\n')
		fichier.write('d-i mirror/http/directory string /debian\n')
		fichier.write('d-i mirror/http/proxy string\n')
		fichier.write('d-i passwd/root-password password {}\n'.format(mdp_root))
		fichier.write('d-i passwd/root-password-again password {}\n'.format(mdp_root))
	#	fichier.write('d-i passwd/root-password-crypted password {}\n'.format(mdp_root))
		fichier.write('d-i passwd/user-fullname string {}\n'.format(nom_user))
		fichier.write('d-i passwd/username string {}\n'.format(nom_user))
		fichier.write('d-i passwd/user-password password {}\n'.format(mdp_user))
		fichier.write('d-i passwd/user-password-again password {}\n'.format(mdp_user))
		fichier.write('d-i clock-setup/utc boolean true\n')
		fichier.write('d-i time/zone string US/Eastern\n')
		fichier.write('d-i clock-setup/ntp boolean true\n')
		fichier.write('d-i partman-md/device_remove_md boolean true\n')
		fichier.write('d-i partman-lvm/device_remove_lvm boolean true\n')
		fichier.write('d-i partman/confirm_nooverwrite boolean true\n')
		fichier.write('d-i     partman-auto/disk string /dev/sda /dev/sdb\n')
		fichier.write('d-i     partman-auto/method string raid\n')
		fichier.write('d-i     partman-md/confirm boolean true\n')
		fichier.write('d-i     partman-lvm/confirm boolean true\n')
		fichier.write('d-i     partman-auto-lvm/guided_size string max\n')
		fichier.write('d-i     partman-auto-lvm/new_vg_name string volume_group00\n')
		fichier.write('d-i     partman-auto/expert_recipe string  \\')
		fichier.write('\n           raid-lvm ::                    \\')
		fichier.write('\n             2048 20 -1 raid               \\')
		fichier.write('\n                $primary{ }                \\')
		fichier.write('\n                $lvmignore{ }              \\')
		fichier.write('\n                method{ raid }             \\')
		fichier.write('\n                format{ }                  \\')
		fichier.write('\n             .                             \\')
		fichier.write('\n             {} 1000 {} swap          \\'.format(taille_swap,taille_swap))
		fichier.write('\n                $defaultignore{ }          \\')
		fichier.write('\n                $lvmok{ }                  \\')
		fichier.write('\n                lv_name{ swap }            \\')
		fichier.write('\n                method{ swap }             \\')
		fichier.write('\n                format{ }                  \\')
		fichier.write('\n            .                              \\')
		fichier.write('\n             2048 5000 6000 ext4             \\')
		fichier.write('\n                $defaultignore{ }          \\')
		fichier.write('\n                $lvmok{ }                  \\')
		fichier.write('\n                lv_name{ root }            \\')
		fichier.write('\n                method{ format }           \\')
		fichier.write('\n                format{ }                  \\')
		fichier.write('\n                use_filesystem{ }          \\')
		fichier.write('\n                filesystem{ ext4 }         \\')
		fichier.write('\n                mountpoint{ / }            \\')
		fichier.write('\n             .\n')
		fichier.write('d-i partman-auto-raid/recipe string \\')
		fichier.write('\n    1 2 0 lvm -                     \\')
		fichier.write('\n          /dev/sda1#/dev/sdb1       \\')
		fichier.write('\n    .\n')
		fichier.write('d-i     mdadm/boot_degraded boolean false\n')
		fichier.write('d-i     partman-md/confirm boolean true\n')
		fichier.write('d-i     partman-partitioning/confirm_write_new_label boolean true\n')
		fichier.write('d-i     partman/choose_partition select Finish partitioning and write changes to disk\n')
		fichier.write('d-i     partman/confirm boolean true\n')
		fichier.write('d-i     partman-md/confirm_nooverwrite  boolean true\n')
		fichier.write('d-i     partman/confirm_nooverwrite boolean true\n')
		fichier.write('tasksel tasksel/first multiselect standard, ssh-server\n')
		fichier.write('d-i grub-installer/only_debian boolean true\n')
		fichier.write('d-i grub-installer/with_other_os boolean true\n')
		fichier.write('d-i grub-installer/bootdev  string /dev/sda\n')
		fichier.write('d-i finish-install/reboot_in_progress note\n')
		fichier.write('d-i preseed/late_command string in-target wget --output-document=/tmp/postinstall.sh http://192.168.0.254/postinstall.sh; in-target /bin/sh /tmp/postinstall.sh\n')
		fichier.write('d-i preseed/late_command string in-target wget --output-document=/tmp/postinstallraid.sh http://192.168.0.254/postinstallraid.sh; in-target /bin/sh /tmp/postinstallraid.sh\n')
		fichier.write('d-i preseed/late_command string in-target wget --output-document=/tmp/bondinterfaces.sh http://192.168.0.254/bondinterfaces.sh; in-target /bin/bash /tmp/bondinterfaces.sh\n')

		
# Ecrire le kickstart avec des variables

def centos(mac, mdp_root, nom_user, mdp_user, taille_swap):
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