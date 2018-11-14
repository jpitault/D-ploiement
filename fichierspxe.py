#!/usr/bin/python3
import re
import sys
import varconfig

# Scripts pour créer fichiers pxe

server = varconfig.ipserveurweb

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
		
def pxedebian(mac):
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


	file = "/srv/tftp/debian/pxelinux.cfg/01-"+mac


	# Créer le fichier
	with open(file, "w") as fichier:
		fichier.write("default debian\nprompt 0\ntimeout 30\n\nlabel debian\n  kernel linux\n  append auto=true priority=critical initrd=initrd.gz netcfg/choose_interface=auto preseed/url=http://")
		fichier.write(server)
		fichier.write("/")
		fichier.write(mac)
		fichier.write("debian.cfg")

		
def pxecentos(mac):
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

		
# Créer un fichier boot pxe pour ubuntu
# Preseed = 00-11-22-33-44-55ubuntu.cfg

def pxeubuntu(mac):
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

	file = "/srv/tftp/ubuntu/pxelinux.cfg/01-"+mac


	# Créer le fichier
	with open(file, "w") as fichier:
		fichier.write("default ubuntu\n")
		fichier.write("prompt 0\n")
		fichier.write("timeout 30\n\n")
		fichier.write("label ubuntu\n")
		fichier.write("  kernel linux\n")
		fichier.write("  append auto=true priority=critical initrd=initrd.gz")
		fichier.write(" netcfg/choose_interface=auto preseed/url=http://{}/".format(server))
		fichier.write("{}ubuntu.cfg".format(mac))

# fichier PXE windows
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
	
	file = '/srv/tftp/windows/pxelinux.cfg/01-' + mac
	
	with open(file, "w") as fichier:
		fichier.write("default windows\n")
		fichier.write("prompt 0\n")
		fichier.write("timeout 30\n\n")
		fichier.write("label windows\n")
		fichier.write("  menu label Install windows server2016 auto unattend\n")
		fichier.write("  KERNEL memdisk\n")
		# On peut utiliser l'IP où la MAC pour différencier le fichier réponse
		#fichier.write("  INITRD winpe_amd64_MAC.iso\n")
		fichier.write("  INITRD winpe_amd64-IP-sansprompt.iso\n")
		fichier.write("  APPEND iso raw")
		
		
# fichier PXE ESXi
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