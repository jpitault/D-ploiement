#!/usr/bin/python3
import re

# Créer un fichier boot pxe pour freebsd

def pxefreebsd(mac):
	# Pour freebsd pas vraiment besoin de variables
	# On peut utiliser tout le temps le même script

	# Mais pour l'instant on créer un fichier pour la MAC
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

	file = "/srv/tftp/freebsd/pxelinux.cfg/01-"+mac
	
	# Créer le fichier
	with open(file, "w") as fichier:
		fichier.write("default freebsd\n")
		fichier.write("prompt 0\n")
		fichier.write("timeout 30\n\n")
		fichier.write("label freebsd\n")
		fichier.write("  menu label mfsFreeBSD auto install script mac-xx:xx:xx:xx:xx:xx\n")
		fichier.write("  kernel memdisk\n")
		fichier.write("  initrd mfsbsdimagepersoscript.img raw")