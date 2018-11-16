#!/usr/bin/python3
import re

# Créer un fichier boot pxe pour centos
# Preseed = 00-11-22-33-44-55centos.cfg

def pxecentos(mac):
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

	file = "/srv/tftp/centos/pxelinux.cfg/01-"+mac


	# Créer le fichier
	with open(file, "w") as fichier:
		fichier.write("default centos\n")
		fichier.write("prompt 0\n")
		fichier.write("timeout 30\n\n")
		fichier.write("label centos\n")
		fichier.write("  kernel vmlinuz\n")
		fichier.write("  append initrd=initrd.img ip=dhcp ")
		fichier.write("inst.ks=http://{}/".format(server))
		fichier.write("{}centos.cfg".format(mac))
