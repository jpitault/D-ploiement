import re
import sys


def pxewindows(mac):
	# variables
	# il faut que l'adresse mac soit séparé par des "-" et en minuscule
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
	
	file = '/srv/tftp/windows/01-' + mac
	
	with open(file, "w") as fichier:
		fichier.write("default windows\n")
		fichier.write("prompt 0\n")
		fichier.write("timeout 30\n\n")
		fichier.write("label windows\n")
		fichier.write("  menu label Install windows server2016 auto unattend\n")
		fichier.write("  KERNEL memdisk\n")
		fichier.write("  INITRD winpe_amd64_MAC.iso\n")
		fichier.write("  APPEND iso raw")