#!/usr/bin/python3
import re

# Ecrire preseed ubuntu avec variables

def ubuntupreseed(mac, mdp_root, nom_user, mdp_user, taille_swap):

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
		fichier.write('d-i partman-md/device_remove_md boolean true \n')
		fichier.write('d-i partman-lvm/device_remove_lvm boolean true \n')
		fichier.write('d-i partman/confirm_nooverwrite boolean true \n')
		fichier.write('d-i     partman-auto/disk string /dev/sda /dev/sdb \n')
		fichier.write('d-i     partman-auto/method string raid \n')
		fichier.write('d-i     partman-md/confirm boolean true \n')
		fichier.write('d-i     partman-lvm/confirm boolean true \n')
		fichier.write('d-i     partman-auto-lvm/guided_size string max \n')
		fichier.write('d-i     partman-auto-lvm/new_vg_name string volume_group00 \n')
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
		fichier.write('\nd-i     mdadm/boot_degraded boolean false \n')
		fichier.write('d-i     partman-md/confirm boolean true \n')
		fichier.write('d-i     partman-partitioning/confirm_write_new_label boolean true \n')
		fichier.write('d-i     partman/choose_partition select Finish partitioning and write changes to disk \n')
		fichier.write('d-i     partman/confirm boolean true \n')
		fichier.write('d-i     partman-md/confirm_nooverwrite  boolean true \n')
		fichier.write('d-i     partman/confirm_nooverwrite boolean true \n')
		fichier.write('tasksel tasksel/first multiselect standard, ssh-server \n')
		fichier.write('d-i grub-installer/only_debian boolean true \n')
		fichier.write('d-i grub-installer/with_other_os boolean true \n')
		fichier.write('d-i grub-installer/bootdev  string /dev/sda /dev/sdb\n')
		fichier.write('d-i finish-install/reboot_in_progress note \n')
		fichier.write('d-i preseed/late_command string in-target wget --output-document=/tmp/postinstallraid.sh http://192.168.0.254/postinstallraid.sh; in-target /bin/sh /tmp/postinstallraid.sh \n')
		fichier.write('d-i preseed/late_command string in-target wget --output-document=/tmp/agregatubuntu.sh http://192.168.0.254/agregatubuntu.sh; in-target /bin/bash /tmp/agregatubuntu.sh \n')
