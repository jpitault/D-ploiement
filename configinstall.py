#!/usr/bin/python3
import re
import subprocess
import varconfig

# On écrit le script d'installation de bsd, en partant du modèle et en changeant les variables
# Il faut que le script de sortie s'appelle : mac-00:11:22:33:44:aa ( définit dans l'image mfsbsd)

server = varconfig.ipserveurweb
def freebsd(mac, taille_swap, nom, mdp_root, nom_user, mdp_user):
	# On vérifie que l'adresse MAC en soit bien une
	X='([a-fA-F0-9]{2}[" ":\-]?){6}'
	ismac = re.compile(X).match(mac)
	if ismac:
		pass
	else:
		print('Adresse MAC invalide. Quitte le script')
		sys.exit



	# On veut une adresse MAC en minuscule, séparée par ":"
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
		# On écrit la variable qui contient l'IP du serveur web
		out_f.write('WEBSERVER="{}"\n'.format(server))
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
		fichier.write('#d-i mirror/suite string stable \n')	
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
		fichier.write('d-i grub-installer/bootdev  string /dev/sda /dev/sdb\n')
		fichier.write('d-i finish-install/reboot_in_progress note\n')
		fichier.write('d-i preseed/late_command string in-target wget --output-document=/tmp/postinstall.sh http://{}/postinstall.sh; in-target /bin/sh /tmp/postinstall.sh; \\'.format(server))
		fichier.write('\nin-target wget --output-document=/tmp/postinstallraid.sh http://{}/postinstallraid.sh; in-target /bin/sh /tmp/postinstallraid.sh;\\'.format(server))
		fichier.write('\nin-target wget --output-document=/tmp/bondinterfaces.sh http://{}/bondinterfaces.sh; in-target /bin/bash /tmp/bondinterfaces.sh;'.format(server))


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
		fichier.write('url --url http://mirror.centos.org/centos/7/os/x86_64/ \n')
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
		fichier.write('repo --name=base --baseurl=http://mirror.centos.org/centos/7/os/x86_64/ \n')
		fichier.write('%packages \n')
		fichier.write('@Core \n')
		fichier.write('wget \n')
		fichier.write('-iwl*firmware \n')
		fichier.write('%end \n')
		fichier.write('%post \n')
		fichier.write('echo "Ceci est un test" > /root/test \n')
		fichier.write('wget --output-document=/tmp/agregatcentos.sh http://{}/agregatcentos.sh \n'.format(server))
		fichier.write('bash /tmp/agregatcentos.sh \n')
		fichier.write('grub2-install /dev/sdb \n')
		fichier.write('%end \n')



# Ecrire preseed ubuntu avec variables

def ubuntu(mac, mdp_root, nom_user, mdp_user, taille_swap):

	# variables
	# On veut une adresse MAC en minuscule, séparée par "-"
	# On commence par séparer l'adresse MAC dans une list
	listmac = re.findall('[a-fA-F0-9]{2}',mac)
	# Puis on remet en string, séparée par ":"
	mac = "-".join(listmac)
	# On met en minuscule
	mac = mac.lower()

	nom_preseed = '/var/www/html/' + mac + "ubuntu.cfg"

	with open(nom_preseed, 'w') as fichier:
		fichier.write('d-i debian-installer/locale string en_US \n')
		fichier.write('d-i console-setup/ask_detect false \n')
		fichier.write('d-i keyboard-configuration/layoutcode string fr \n')
		fichier.write('d-i keyboard-configuration/variantcode latin9 \n')
		fichier.write('d-i keyboard-configuration/layout French \n')
		fichier.write('d-i keyboard-configuration/toggle select No toggling \n')
		fichier.write('d-i netcfg/choose_interface select auto \n')
		fichier.write('d-i netcfg/get_hostname string ubuntu2pxe \n')
		fichier.write('d-i netcfg/get_domain string unassigned-domain \n')
		#fichier.write('d-i netcfg/hostname string ubuntu2pxe \n')
		fichier.write('d-i netcfg/wireless_wep string \n')
		fichier.write('d-i mirror/country string manual \n')
		fichier.write('d-i mirror/http/hostname string http://archive.ubuntu.com \n')
		fichier.write('d-i mirror/http/directory string /ubuntu \n')
		fichier.write('d-i mirror/http/proxy string \n')
		fichier.write('#d-i mirror/suite string disco \n')
		fichier.write('d-i passwd/root-login boolean true \n')
		fichier.write('d-i passwd/root-password password {} \n'.format(mdp_root))
		fichier.write('d-i passwd/root-password-again password {} \n'.format(mdp_root))
		fichier.write('d-i passwd/user-fullname string {} \n'.format(nom_user))
		fichier.write('d-i passwd/username string {} \n'.format(nom_user))
		fichier.write('d-i passwd/user-password password {} \n'.format(mdp_user))
		fichier.write('d-i passwd/user-password-again password {} \n'.format(mdp_user))
		fichier.write('d-i clock-setup/utc boolean true \n')
		fichier.write('d-i time/zone string US/Eastern \n')
		fichier.write('d-i clock-setup/ntp boolean true \n')
		# On nettoie les disques de façon à enlever les traces de LVM et soft raid,
		# Car sinon Ubuntu refuse de s'installer sur des disques qui en contenaient (Ubuntu, Debian, CentOS)
		fichier.write('d-i partman/early_command string vgs --separator=: --noheadings | cut -f1 -d: | while read vg ; do vgchange -an $vg ; done ;\\')
		fichier.write('\npvs --separator=: --noheadings | cut -f1 -d: | while read pv ; do pvremove -ff -y $pv ; done ;\\')
		fichier.write('\ncat /proc/mdstat | grep active | cut -f1 -d: | while read md ; do mdadm --stop /dev/$md ; mdadm --remove /dev/$md ; done ;\\')
		fichier.write('\nmdadm --zero-superblock /dev/sda ;\\')
		fichier.write('\nmdadm --zero-superblock /dev/sdb \n')
		fichier.write('d-i partman-auto/disk string /dev/sda /dev/sdb \n')
		fichier.write('d-i partman-auto/method string raid \n')
		fichier.write('d-i partman-auto/purge_lvm_from_device boolean true \n')
		fichier.write('d-i partman-auto-lvm/guided_size string max \n')
		fichier.write('d-i partman-auto-lvm/new_vg_name string volume_group00 \n')
		fichier.write('d-i partman/choose_partition select finish \n')
		fichier.write('d-i partman-partitioning/confirm_write_new_label boolean true \n')
		
		fichier.write('d-i partman-md/device_remove_md boolean true \n')
		fichier.write('d-i partman-md/confirm boolean true \n')
		fichier.write('d-i partman-md/confirm_nooverwrite  boolean true \n')		
		fichier.write('d-i partman-lvm/device_remove_lvm boolean true \n')
		fichier.write('d-i partman-lvm/device_remove_lvm_span boolean true \n')
		fichier.write('d-i partman-lvm/confirm boolean true \n')
		fichier.write('d-i partman-lvm/confirm_nooverwrite boolean true \n')

		fichier.write('d-i partman/confirm_write_new_label boolean true \n')
		fichier.write('d-i partman/confirm boolean true \n')
		fichier.write('d-i partman/confirm_nooverwrite boolean true \n')
		
		fichier.write('\nd-i     partman-auto/expert_recipe string  \\')
		fichier.write('\n           raid-lvm ::                    \\')
		fichier.write('\n             2048 20 -1 raid               \\')
		fichier.write('\n                $primary{ }                \\')
		fichier.write('\n                $lvmignore{ }              \\')
		fichier.write('\n                method{ raid }             \\')
		fichier.write('\n                format{ }                  \\')
		fichier.write('\n             .                             \\')
		fichier.write('\n             {} 1000 {} swap          \\'.format(taille_swap, taille_swap))
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
		fichier.write('\n                .')
		fichier.write('\nd-i partman-auto-raid/recipe string \\')
		fichier.write('\n    1 2 0 lvm -                     \\')
		fichier.write('\n          /dev/sda1#/dev/sdb1       \\')
		fichier.write('\n           .')
		fichier.write('\nd-i mdadm/boot_degraded boolean false \n')

		fichier.write('tasksel tasksel/first multiselect standard \n')
		fichier.write('d-i pkgsel/include string openssh-server build-essential \n')
		fichier.write('d-i grub-installer/only_debian boolean true \n')
		fichier.write('d-i grub-installer/with_other_os boolean true \n')
		fichier.write('d-i grub-installer/bootdev string /dev/sda /dev/sdb \n')
		fichier.write('d-i finish-install/reboot_in_progress note \n')
		fichier.write('d-i preseed/late_command string in-target wget --output-document=/tmp/postinstallraid.sh http://{}/postinstallraid.sh; in-target /bin/sh /tmp/postinstallraid.sh; \\'.format(server))
		fichier.write('\nin-target wget --output-document=/tmp/agregatubuntu.sh http://{}/agregatubuntu.sh; in-target /bin/bash /tmp/agregatubuntu.sh; '.format(server))

		
def proxmox(mac, mdp_root, nom_user, mdp_user, taille_swap):

	# On prend le fichier debian
	debian(mac, mdp_root, nom_user, mdp_user, taille_swap)
	
	# Et on y ajoute le script proxmox en postinstall qui est sur notre serveur web
	script = 'proxmoxinstall.sh'
	
	# variables
	# On veut une adresse MAC en minuscule, séparée par "-"
	# On commence par séparer l'adresse MAC dans une list
	listmac = re.findall('[a-fA-F0-9]{2}',mac)
	# Puis on remet en string, séparée par ":"
	mac = "-".join(listmac)
	# On met en minuscule
	mac = mac.lower()

	nom_preseed = '/var/www/html/' + mac + "debian.cfg"
	
	with open(nom_preseed,'a') as fichier:
		fichier.write('\\\nin-target wget --output-document=/tmp/{0} http://{1}/{0}; in-target /bin/bash /tmp/{0} ;'.format(script, server))
		
		
# Ecrire fichier qui répond aux questions de l'installateur OpenBSD, le fichier disklabel et le set agrégat

def openbsd(mac, nom, mdp_root, nom_user, mdp_user, taille_swap):
	# Variables
	#mac = '001122334455'
	#nom = 'openbsdtest'
	#mdp_root = 'password'
	#nom_user = 'julian'
	#mdp_user = 'password'
	#taille_swap = '1024'

	# La version de openbsd
	version = '6.2'
	versionSansPoint = version.replace(".", "")

	# On vérifie que l'adresse MAC en soit bien une
	X='([a-fA-F0-9]{2}[" ":\-]?){6}'
	ismac = re.compile(X).match(mac)
	if ismac:
		pass
	else:
		print('Adresse MAC invalide. Quitte le script')
		sys.exit

	# on veut que la mac soit séparé par des : et en minuscules
	# On commence par séparer l'adresse MAC dans une list
	listmac = re.findall('[a-fA-F0-9]{2}',mac)
	# Puis on remet en string, séparée par ":"
	mac = ":".join(listmac)
	# On met en minuscule
	mac = mac.lower()

	# Le nom du fichier qui sera créé
	file = '/var/www/html/openbsd/' + mac + '-install.conf'

	# Le nom du fichier disklabel
	disklabel = mac + '-disklabel'
	disklabelfile = '/var/www/html/openbsd/' + disklabel
	


	# Puis on écrit le fichier réponse
	with open(file, 'w') as fichier:
		fichier.write('Choose your keyboard layout=fr\n')
		fichier.write('System hostname = {}\n'.format(nom))
		fichier.write('Do you expect to run the X window System = no\n')
		fichier.write('Password for root = {}\n'.format(mdp_root))
		fichier.write('Network interfaces = em0\n')
		fichier.write('IPv4 address for em0 = dhcp\n')
		fichier.write('Setup a user = {}\n'.format(nom_user))
		fichier.write('Password for user = {}\n'.format(mdp_user))
		fichier.write('What timezone are you in = Europe/Paris\n')
		fichier.write('Location of sets = http\n')
		fichier.write('HTTP Server = {}\n'.format(server))
		fichier.write('Use http instead = yes\n')
		fichier.write('Set name(s) = -x* -g* done\n')
		fichier.write('Checksum test for site{}-{}.tgz failed. Continue anyway = yes\n'.format(versionSansPoint, nom))
		fichier.write('Unverified sets: site{}-{}.tgz. Continue without verification = yes\n'.format(versionSansPoint, nom))
		fichier.write('URL to autopartitioning template for disklabel = http://{}/openbsd/{}\n'.format(server, disklabel))
		
		
	# On écrit le fichier Disklabel
	with open(disklabelfile, 'w') as fichier:
		fichier.write('/	500M\n')
		fichier.write('swap	{}M\n'.format(taille_swap))
		fichier.write('/tmp	1G-*	25%\n')
		fichier.write('/var	1G-*	25%\n')
		fichier.write('/usr	1G-*	25%\n')
		fichier.write('/home	1G-*	25%\n')
		
		
	# Pour la conf agrégat on a besoin d'utiliser un set
	# Pour l'instant on ne fait que copier, en renommant, un set déjà créer
	nouv_set = 'site' + versionSansPoint + '-' + nom + '.tgz'
	subprocess.run(['cp', 'site62.tgz'.format(versionSansPoint), '/var/www/html/pub/OpenBSD/{}/amd64/{}'.format(version, nouv_set)])
	
	# Il faut mettre à jour le fichier index
	cheminSet = '/var/www/html/pub/OpenBSD/{}/amd64/'.format(version)
	index = cheminSet + 'index.txt'
	proc = subprocess.Popen(['ls', '-l', cheminSet], stdout=subprocess.PIPE)
	list = proc.stdout.read().decode("utf-8")
	
	with open(index, 'w') as fichier:
		fichier.write(list)
		
		
# fichier unattend windows server 2016
def winunattend(mac, computername, mdp_admin, raid, productkey, ip):
	# On nettoie les disques 0 et 1 dans WinPE avec diskpart


	# On utilise soit l'adresse IP soit l'adresse MAC pour différencier le fichier unattend.xml
	fileip = '/samba/winserv2016/' + ip + '.xml'
	
	# L'adresse MAC doit être en majuscule et séparée par des "-"
	# On commence par séparer l'adresse MAC dans une list
	listmac = re.findall('[a-fA-F0-9]{2}',mac)
	# Puis on remet en string, séparée par "-"
	mac = "-".join(listmac)
	# On met en majuscule
	mac = mac.upper()
	# fichier de sortie
	filemac = '/samba/winserv2016/' + mac + '.xml'
	
	serversamba = '10.10.75.2'
	
	# variables ?
	#productkey = 'WC2BQ-8NRM3-FDDYY-2BFGV-KHKQY'
	#computername = 'TestComputerName'
	#mdp_admin = 'password'
	regorg = 'castleit'
	regown = 'castleit'
	

	with open(fileip , 'w') as fichier:	
		fichier.write('<?xml version="1.0" encoding="utf-8"?> \n')
		fichier.write('<unattend xmlns="urn:schemas-microsoft-com:unattend"> \n')
		fichier.write('    <settings pass="specialize"> \n')
		fichier.write('        <component name="Microsoft-Windows-Shell-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> \n')
		fichier.write('            <AutoLogon> \n')
		fichier.write('                <Password> \n')
		fichier.write('                    <Value>{}</Value> \n'.format(mdp_admin))
		fichier.write('                    <PlainText>true</PlainText> \n')
		fichier.write('                </Password> \n')
		fichier.write('                <Enabled>true</Enabled> \n')
		fichier.write('                <Username>Administrateur</Username> \n')
		fichier.write('                <LogonCount>1</LogonCount> \n')
		fichier.write('            </AutoLogon> \n')
		fichier.write('            <ComputerName>{}</ComputerName> \n'.format(computername))
		fichier.write('            <RegisteredOrganization>{}</RegisteredOrganization> \n'.format(regorg))
		fichier.write('            <RegisteredOwner>{}</RegisteredOwner> \n'.format(regown))
		fichier.write('            <TimeZone>Romance Standard Time</TimeZone> \n')
		fichier.write('        </component>		 \n')
		fichier.write('    </settings> \n')
		fichier.write('    <settings pass="oobeSystem"> \n')
		fichier.write('        <component name="Microsoft-Windows-Shell-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> \n')
		fichier.write('            <FirstLogonCommands> \n')
		fichier.write('                <SynchronousCommand wcm:action="add"> \n')
		fichier.write('                    <CommandLine>PowerShell -Command "New-NetLbfoTeam -Name \'bond0\' -TeamMembers \'Ethernet\',\'Ethernet 2\' -TeamingMode SwitchIndependent -LoadBalancingAlgorithm TransportPorts -Confirm:$false"</CommandLine> \n')
		fichier.write('                    <Description>Active le teaming</Description> \n')
		fichier.write('                    <Order>9</Order> \n')
		fichier.write('                </SynchronousCommand> \n')
		
		# Si l'option raid est présente on crée un software RAID1
		if raid == 'raid':
			fichier.write('                <SynchronousCommand wcm:action="add"> \n')
			fichier.write('                    <CommandLine>net use N: \\{}\public /user:user pass</CommandLine> \n'.format(serversamba))
			fichier.write('                    <Description>Mappe le lecteur</Description> \n')
			fichier.write('                    <Order>1</Order> \n')
			fichier.write('                </SynchronousCommand> \n')
			fichier.write('                <SynchronousCommand wcm:action="add"> \n')
			# Le fichier MirrorDiskpart.txt est hebergé sur le partage samba
			# Il contient les commandes qui permettent de créer un RAID1 avec diskpart.exe:
			# MirrorDiskpart.txt --->
			# 	select disk 1
			# 	convert dynamic
			# 	select disk 0
			# 	convert dynamic
			# 	select volume 1
			# 	add disk 1
			# 	select volume 0
			# 	add disk 1
			fichier.write('                    <CommandLine>diskpart.exe /s N:\winserv2016\MirrorDiskpart.txt</CommandLine> \n')
			fichier.write('                    <Description>Crée un miroir</Description> \n')
			fichier.write('                    <Order>2</Order> \n')
			fichier.write('                </SynchronousCommand> \n')
			fichier.write('                <SynchronousCommand wcm:action="add"> \n')
			fichier.write('                    <CommandLine>net use N: /delete</CommandLine> \n')
			fichier.write('                    <Description>Supprimer le mappage</Description> \n')
			fichier.write('                    <Order>3</Order> \n')
			fichier.write('                </SynchronousCommand>				 \n')
			
		fichier.write('            </FirstLogonCommands>             \n')
		fichier.write('			<OOBE> \n')
		fichier.write('                <HideEULAPage>true</HideEULAPage> \n')
		fichier.write('                <HideLocalAccountScreen>true</HideLocalAccountScreen> \n')
		fichier.write('                <HideOnlineAccountScreens>true</HideOnlineAccountScreens> \n')
		fichier.write('				<NetworkLocation>Work</NetworkLocation> \n')
		fichier.write('                <ProtectYourPC>1</ProtectYourPC> \n')
		fichier.write('				<SkipMachineOOBE>true</SkipMachineOOBE> \n')
		fichier.write('                <SkipUserOOBE>true</SkipUserOOBE> \n')
		fichier.write('            </OOBE> \n')
		fichier.write('            <UserAccounts> \n')
		fichier.write('                <AdministratorPassword> \n')
		fichier.write('                    <Value>{}</Value> \n'.format(mdp_admin))
		fichier.write('                    <PlainText>true</PlainText> \n')
		fichier.write('                </AdministratorPassword> \n')
		fichier.write('            </UserAccounts> \n')
		fichier.write('        </component> \n')
		fichier.write('    </settings> \n')
		fichier.write('    <settings pass="windowsPE"> \n')
		fichier.write('        <component name="Microsoft-Windows-International-Core-WinPE" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> \n')
		fichier.write('            <SetupUILanguage> \n')
		fichier.write('                <UILanguage>fr-FR</UILanguage> \n')
		fichier.write('            </SetupUILanguage> \n')
		fichier.write('            <InputLocale>fr-FR</InputLocale> \n')
		fichier.write('            <SystemLocale>fr-FR</SystemLocale> \n')
		fichier.write('            <UILanguage>fr-FR</UILanguage> \n')
		fichier.write('            <UILanguageFallback>fr-FR</UILanguageFallback> \n')
		fichier.write('            <UserLocale>fr-FR</UserLocale> \n')
		fichier.write('        </component>	 \n')
		fichier.write('        <component name="Microsoft-Windows-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> \n')
		fichier.write('            <DiskConfiguration> \n')
		fichier.write('			  <Disk wcm:action="add"> \n')
		fichier.write('				<DiskID>0</DiskID>  \n')
		fichier.write('				<WillWipeDisk>true</WillWipeDisk>  \n')
		fichier.write('				<CreatePartitions> \n')
		fichier.write('				  <!-- System partition --> \n')
		fichier.write('				  <CreatePartition wcm:action="add"> \n')
		fichier.write('					<Order>1</Order>  \n')
		fichier.write('					<Type>Primary</Type>  \n')
		fichier.write('					<Size>350</Size>  \n')
		fichier.write('				  </CreatePartition> \n')
		fichier.write('				  <!-- Windows partition --> \n')
		fichier.write('				  <CreatePartition wcm:action="add"> \n')
		fichier.write('					<Order>2</Order>  \n')
		fichier.write('					<Type>Primary</Type>  \n')
		fichier.write('					<Extend>true</Extend>  \n')
		fichier.write('				  </CreatePartition> \n')
		fichier.write('				</CreatePartitions> \n')
		fichier.write('				<ModifyPartitions> \n')
		fichier.write('				  <!-- System partition --> \n')
		fichier.write('				  <ModifyPartition wcm:action="add"> \n')
		fichier.write('					<Order>1</Order>  \n')
		fichier.write('					<PartitionID>1</PartitionID>  \n')
		fichier.write('					<Label>System</Label>  \n')
		fichier.write('					<Letter>S</Letter>  \n')
		fichier.write('					<Format>NTFS</Format>  \n')
		fichier.write('					<Active>true</Active>  \n')
		fichier.write('				  </ModifyPartition> \n')
		fichier.write('				  <!-- Windows partition --> \n')
		fichier.write('				  <ModifyPartition wcm:action="add"> \n')
		fichier.write('					<Order>2</Order>  \n')
		fichier.write('					<PartitionID>2</PartitionID>  \n')
		fichier.write('					<Label>Windows</Label>  \n')
		fichier.write('					<Letter>C</Letter>  \n')
		fichier.write('					<Format>NTFS</Format>  \n')
		fichier.write('				  </ModifyPartition> \n')
		fichier.write('				</ModifyPartitions> \n')
		fichier.write('			  </Disk> \n')
		fichier.write('			  <WillShowUI>OnError</WillShowUI>  \n')
		fichier.write('			</DiskConfiguration> \n')
		fichier.write('			<ImageInstall> \n')
		fichier.write('                <OSImage> \n')
		fichier.write('                    <InstallFrom> \n')
		fichier.write('                        <MetaData wcm:action="add"> \n')
		fichier.write('                            <Key>/IMAGE/NAME</Key> \n')
		fichier.write('                            <Value>Windows Server 2016 SERVERSTANDARD</Value> \n')
		fichier.write('                        </MetaData> \n')
		fichier.write('                    </InstallFrom>				 \n')
		fichier.write('                    <InstallTo> \n')
		fichier.write('                        <DiskID>0</DiskID> \n')
		fichier.write('                        <PartitionID>2</PartitionID> \n')
		fichier.write('                    </InstallTo> \n')
		fichier.write('                </OSImage> \n')
		fichier.write('            </ImageInstall> \n')
		fichier.write('            <UserData> \n')
		fichier.write('                <ProductKey> \n')
		fichier.write('                    <Key>{}</Key> \n'.format(productkey))
		fichier.write('                    <WillShowUI>OnError</WillShowUI> \n')
		fichier.write('                </ProductKey> \n')
		fichier.write('                <AcceptEula>true</AcceptEula> \n')
		fichier.write('            </UserData>			 \n')
		fichier.write('        </component> \n')
		fichier.write('    </settings> \n')
		fichier.write('    <cpi:offlineImage cpi:source="wim:c:/iso/install.wim#Windows Server 2016 SERVERSTANDARD" xmlns:cpi="urn:schemas-microsoft-com:cpi" /> \n')
		fichier.write('</unattend> \n')

		
# fichier kickstart pour ESXi
def esxi(mac, MDP_ROOT, NOM_USER, MDP_USER, LICENSE_KEY):
	# On veut une adresse MAC en minuscule, séparée par "-"
	# On commence par séparer l'adresse MAC dans une list
	listmac = re.findall('[a-fA-F0-9]{2}',mac)
	# Puis on remet en string, séparée par ":"
	mac = "-".join(listmac)
	# On met en minuscule
	mac = mac.lower()

	nom_preseed = '/var/www/html/' + mac + "esxi.cfg"
	

	# On écrit le fichier
	with open(nom_preseed,'w') as fichier:
		fichier.write('#\n')
		fichier.write('# Sample scripted installation file\n')
		fichier.write('#\n')
		fichier.write('\n')
		fichier.write('# Accept the VMware End User License Agreement\n')
		fichier.write('vmaccepteula\n')
		fichier.write('\n')
		fichier.write('# Set the root password for the DCUI and Tech Support Mode chiffré ou password\n')
		fichier.write('#rootpw --iscrypted <mdpchiffré>\n')
		fichier.write('rootpw {}\n'.format(MDP_ROOT))
		fichier.write('\n')
		fichier.write('# Installe sur le premier disque trouvé, cherche en premier local, puis sur le network et enfin USB.\n')
		fichier.write('# overwritevmfs Supprime un VMFS datastore si il y en a un présent sur le disque.\n')
		fichier.write('install --firstdisk --overwritevmfs\n')
		fichier.write('\n')
		fichier.write('# On met le clavier en français\n')
		fichier.write("keyboard 'French'\n")
		fichier.write('\n')
		if LICENSE_KEY != '':
			fichier.write('# Configure la licence, si non-inclus ESXi installe en mode évaluation\n')
			fichier.write('#vmserialnum --esx={}\n'.format(LICENSE_KEY))
			fichier.write('\n')
		fichier.write('# Set the network to DHCP on the first network adapter\n')
		fichier.write('network --bootproto=dhcp --device=vmnic0\n')
		fichier.write('#network --bootproto=static --addvmportgroup=0 --device=vmnic0 --ip=${IPADDR} --netmask=${NETMASK} --gateway=${GATEWAY} --nameserver=${DNS} --hostname=${HOSTNAME}\n')
		fichier.write('\n')
		fichier.write("# On indique à la machine si elle doit redémarrer après l'installation\n")
		fichier.write('reboot\n')
		fichier.write('\n')
		fichier.write("# On peut spécifier un autre script d'installation\n")
		fichier.write('#%include /tmp/networking.cfg\n')
		fichier.write('\n')
		fichier.write('\n')
		fichier.write("# On peut avoir un script qui s'exécute avant le fichier kickstart. Par exemple, on peut l'utiliser pour générer des fichiers\n")
		fichier.write('# que le kickstart utilisera\n')
		fichier.write('# 2 interpreteurs possibles : busybox ou python (par défaut busybox)\n')
		fichier.write('#%pre --interpreter=busybox\n')
		fichier.write(' \n')
		fichier.write('## extract network info from bootup\n')
		fichier.write('#VMK_INT="vmk0"\n')
		fichier.write('#VMK_LINE=$(localcli network ip interface ipv4 get | grep "${VMK_INT}")\n')
		fichier.write('#IPADDR=$(echo "${VMK_LINE}" | awk \'{print $2}\')\n')
		fichier.write('#NETMASK=$(echo "${VMK_LINE}" | awk \'{print $3}\')\n')
		fichier.write('#GATEWAY=$(localcli network ip route ipv4 list | grep default | awk \'{print $3}\')\n')
		fichier.write('#DNS="172.30.0.100,172.30.0.200"\n')
		fichier.write('#HOSTNAME=$(nslookup "${IPADDR}" "${DNS}" | grep Address | grep "${IPADDR}" | awk \'{print $4}\')\n')
		fichier.write(' \n')
		fichier.write('#echo "network --bootproto=static --addvmportgroup=false --device=vmnic0 --ip=${IPADDR} --netmask=${NETMASK} --gateway=${GATEWAY} --nameserver=${DNS} --hostname=${HOSTNAME}" > /tmp/networking.cfg\n')
		fichier.write(' \n')
		fichier.write('\n')
		fichier.write("# On peut exécuter de la même manière un script après l'installation des packages\n")
		fichier.write('#%post --interpreter=python --ignorefailure=true\n')
		fichier.write('#import time\n')
		fichier.write("#stampFile = open('/finished.stamp', mode='w')\n")
		fichier.write('#stampFile.write( time.asctime() )\n')
		fichier.write('\n')
		fichier.write('\n')
		fichier.write("# On peut créer un script qui s'exécutera seulement au premier boot\n")
		fichier.write('%firstboot --interpreter=busybox\n')
		fichier.write('# active et démarre le service ssh\n')
		fichier.write('vim-cmd hostsvc/enable_ssh\n')
		fichier.write('vim-cmd hostsvc/start_ssh\n')
		fichier.write('\n')
		fichier.write('# active et démarre la console ESXi\n')
		fichier.write('vim-cmd hostsvc/enable_esx_shell\n')
		fichier.write('vim-cmd hostsvc/start_esx_shell\n')
		fichier.write('\n')
		fichier.write('%firstboot --interpreter=busybox\n')
		fichier.write("esxcli system account add -d 'description du compte' -i {0} -p {1} -c {1}\n".format(NOM_USER, MDP_USER))
		fichier.write('esxcli system permission set -i {} -r Admin\n'.format(NOM_USER))
		fichier.write('# assign license')
		fichier.write('#vim-cmd vimsvc/license --set AAAAA-BBBBB-CCCCC-DDDDD-EEEEE')
		fichier.write('##vSwitch configuration\n')
		fichier.write('# Attacher vmnic1 à vSwitch0\n')
		fichier.write('esxcli network vswitch standard uplink add --uplink-name vmnic1 --vswitch-name vSwitch0\n')