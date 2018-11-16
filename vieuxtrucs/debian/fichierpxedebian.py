#!/usr/bin/python3
import re

# Créer un fichier boot pxe pour debian
# Preseed = 00-11-22-33-44-55debian.cfg

def pxedebian(mac):
	# variables
	# il faut que l'adresse mac soit séparé par des "-" et en minuscule
	server = "192.168.0.254"

	# On vérifie que l'adresse MAC en soit bien une
	X='([a-fA-F0-9]{2}[" ":\-]?){6}'
	ismac = re.compile(X).match(mac)
	if ismac:
		pass
	else:
		print('Adresse MAC invalide. Quitte le script')
		sys.exit

	# On veut une adresse MAC en minuscule, séparée par "-"
	# On commence par séparer l'adresse MAC dans une list
	listmac = re.findall('[a-fA-F0-9]{2}',mac)
	# Puis on remet en string, séparée par ":"
	mac = "-".join(listmac)
	# On met en minuscule
	mac = mac.lower()

	file = "/srv/tftp/debian2/pxelinux.cfg/01-"+mac


	# Créer le fichier
	with open(file, "a") as fichier:
		fichier.write("default debian\nprompt 0\ntimeout 30\n\nlabel debian\n  kernel linux\n  append auto=true priority=critical initrd=initrd.gz netcfg/choose_interface=auto preseed/url=http://")
		fichier.write(server)
		fichier.write("/")
		fichier.write(mac)
		fichier.write("debian.cfg")
