import re
import sys

server = '192.168.0.254'

def pxeesxi(mac):
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
	# Nom du fichier pxe
	file = "/srv/tftp/esxi/pxelinux.cfg/01-"+mac
	# On crée le fichier pxe
	with open(file, 'w') as fichier:
		fichier.write('DEFAULT esxi\n')
		fichier.write('nohalt 1\n')
		fichier.write('prompt 0\n')
		fichier.write('timeout 300\n')
		fichier.write('\nLABEL esxi\n')
		fichier.write('  menu label ESXi Installation\n')
		fichier.write('  KERNEL esxi6/mboot.c32\n')
		fichier.write('  APPEND -c esxi6/boot.cfg ks=http://{}/{}esxi.cfg'.format(server, mac))
	