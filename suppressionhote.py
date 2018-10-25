import os
import re
import subprocess
import xml.etree.ElementTree as ET


""" Script qui supprime tous les fichiers qui ont été crées à l'ajout d'un hôte.
Il faut supprimer :
	- Les fichiers DHCP ( nom )
		- Le fichier qui contient l'hôte
		- La ligne qui include l'hôte dans dhcpd.conf
		- Redémarrer le serveur pour que la modif soit prise en compte
	- Le fichier PXE ( MAC )
		- Pour tous les OS sauf OpenBSD
	- Le ou les fichiers d'installation (MAC)
		- Debian, Ubuntu, Proxmox : Preseed
		- Centos : Kickstart
		- Openbsd : (MAC + nom)
			- fichier réponse
			- fichier disklabel
			- fichier set (.tgz)
		- Freebsd : script d'installation
"""
# variables
#mac = '001122334455'
#nom = 'testsupp'
#osinstall = 'centos'

# Nettoyer la conf DHCP
def menagedhcp(mac, nom, osinstall):
	# On supprime le fichier à part
	path = '/etc/dhcp/' + nom
	try:
		os.remove(path)
	except OSError as  e:
		if e.errno == 2:
			pass

	# On supprime sa référence dans dhcpd.conf
	dhcpd = '/etc/dhcp/dhcpd.conf'
	# On lit le fichier dhcpd.conf
	with open(dhcpd, 'r') as ancien:
		lignes = ancien.readlines()
	# On le réécrit sans la ligne que l'on ne veut pas
	with open(dhcpd, 'w') as fichier:
		for ligne in lignes:
			if nom not in ligne:
				fichier.write(ligne)
				
	# On redémarre le service
	subprocess.run(["systemctl", "restart", "isc-dhcp-server.service"])


# Supprimer le fichier PXE
def menagepxe(mac, nom, osinstall):
	# On ne travail pas si osinstall == openbsd
	if osinstall == 'openbsd' :
		pass
	else:
		# Juste parce que je n'ai toujours pas changé mes répertoires
		if osinstall == 'debian':
			osinstall = 'debian2'
		if osinstall == 'ubuntu':
			osinstall = 'ubuntu2'
			
			
		# il faut que l'adresse mac soit séparé par des "-" et en minuscule
		# On vérifie que l'adresse MAC en soit bien une
		X='([a-fA-F0-9]{2}[" ":\-]?){6}'
		ismac = re.compile(X).match(mac)
		# Pas besoin, on ne fait que supprimer des fichiers
		#if ismac:
		#	pass
		#else:
		#	print('Adresse MAC invalide. Quitte le script')
		#	sys.exit

		# On veut une adresse MAC en minuscule, séparée par "-"
		# On commence par séparer l'adresse MAC dans une list
		listmac = re.findall('[a-fA-F0-9]{2}',mac)
		# Puis on remet en string, séparée par ":"
		mac = "-".join(listmac)
		# On met en minuscule
		mac = mac.lower()
		
		# le nom du fichier
		tftp = '/srv/tftp/'
		pxelinux = '/pxelinux.cfg/01-'
		fichierpxe = tftp + osinstall + pxelinux + mac
		
		# on le supprime
		try :
			os.remove(fichierpxe)
		except OSError as  e:
			if e.errno == 2:
				pass
			
# On supprime les fichiers de conf
def menageconf(mac, nom, osinstall):
	# On a besoin de la MAC en minuscule et séparée par des ":" et par des "-"
	# On met en minuscule
	mac = mac.lower()
	# On sépare l'adresse MAC dans une list
	listmac = re.findall('[a-fA-F0-9]{2}',mac)

	# Puis on remet en string, séparée par ":"
	macdp = ":".join(listmac)
	# Ou on remet en string, séparée par "-"
	mact = "-".join(listmac)

	serveurweb = '/var/www/html/'

	# OpenBSD et windows sont à part
	if osinstall == 'openbsd':
		# supprime fichier réponse et fichier disklabel
		for fichier in os.listdir(serveurweb + 'openbsd/'):
			if macdp in fichier:
				try:
					os.remove(serveurweb + 'openbsd/' + fichier)
				except OSError as  e:
					if e.errno == 2:
						pass
					
		# supprime archive site62-nom.tgz
		distrib = 'pub/OpenBSD/6.2/amd64/'
		archive = serveurweb + distrib + 'site62-' + nom + '.tgz'
		try:
			os.remove(archive)
		except OSError as  e:
			if e.errno == 2:
				pass
	
	if osinstall == 'windows':
		# supprime le fichier réponse (unattend), pour ça on a besoin de la mac en majuscule
		unattend = '/samba/winserv2016/' + mact.upper() + '.xml'
		try:
			os.remove(unattend)
		except OSError as e:
			if e.errno == 2:
				pass
		
	# Pour les autres OS
	else:
		for fichier in os.listdir(serveurweb):
			if macdp in fichier or mact in fichier:
				try:
					os.remove(serveurweb + fichier)
				except OSError as  e:
					if e.errno == 2:
						pass
				
def menage(mac, nom, osinstall):
	menagedhcp(mac, nom, osinstall)
	menagepxe(mac, nom, osinstall)
	menageconf(mac, nom, osinstall)

def menagexml(file):
	# Lit le .xml
	tree = ET.parse(file)
	root = tree.getroot()

	# Variables
	mac = root[0].text
	osinstall = root[1].text
	nom = root[3].text
	
	menage(mac, nom, osinstall)