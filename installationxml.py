#!/usr/bin/python3
import re
import sys
import ajouterhost
import configinstall
import fichierspxe
import xml.etree.ElementTree as ET


def installxml(file):
	#xml = input('Quel fichier faut il lire ? :')
	tree = ET.parse(file)
	root = tree.getroot()

	# Installation d'une machine

	# Variables
	# mac = root[0].text
	# os = root[1].text
	# ip = root[2].text
	# nom = root[3].text
	#file = "/etc/dhcp/"+nom
	# mdp_root = root[4].text
	# nom_user = root[5].text
	# mdp_user = root[6].text
	# taille_swap = root[7].text
	
	# Sinon avec le nom des champs fixe
	mac = root.find('MACadd').text
	os = root.find('OS').text
	ip = root.find('IP').text
	nom = root.find('NOM').text
	mdp_root = root.find('MDP_ROOT').text
	nom_user = root.find('NOM_USER').text
	mdp_user = root.find('MDP_USER').text
	taille_swap = root.find('SWAP').text

	# On met le nom de l'OS en minuscules
	os = os.lower()

	# On vérifie que l'adresse MAC en soit bien une
	X='([a-fA-F0-9]{2}[" ":\-]?){6}'
	ismac = re.compile(X).match(mac)
	if ismac:
		pass
	else:
		print('Adresse MAC invalide. Quitte le script')
		sys.exit('mauvaise MAC')
		

	# On crée un host pour le DHCP, 1 seul script
	#ajouterhost.ajouterhost(mac, os, ip, nom, file)


	# On crée un fichier pour le boot pxe
	if os == 'debian':
		# On crée un host pour le DHCP, 1 seul script
		ajouterhost.ajouterhost(mac, os, ip, nom)
		# On crée le fichier pxe
		fichierspxe.pxedebian(mac)
		# On crée le preseed
		configinstall.debian(mac, mdp_root, nom_user, mdp_user, taille_swap)
	elif os == 'centos':
		# On crée un host pour le DHCP, 1 seul script
		ajouterhost.ajouterhost(mac, os, ip, nom)
		fichierspxe.pxecentos(mac)
		configinstall.centos(mac, mdp_root, nom_user, mdp_user, taille_swap)
	elif os == 'freebsd':
		# On crée un host pour le DHCP, 1 seul script
		ajouterhost.ajouterhost(mac, os, ip, nom)
		fichierspxe.pxefreebsd(mac)
		configinstall.freebsd(mac, taille_swap, nom, mdp_root, nom_user, mdp_user)
	elif os == 'ubuntu':
		# On crée un host pour le DHCP, 1 seul script
		ajouterhost.ajouterhost(mac, os, ip, nom)
		fichierspxe.pxeubuntu(mac)
		configinstall.ubuntu(mac, mdp_root, nom_user, mdp_user, taille_swap)
	elif os == 'proxmox':
		os = 'debian'
		# On crée un host pour le DHCP, 1 seul script
		ajouterhost.ajouterhost(mac, os, ip, nom)
		fichierspxe.pxedebian(mac)
		configinstall.proxmox(mac, mdp_root, nom_user, mdp_user, taille_swap)
	elif os == 'openbsd':
		ajouterhost.ajouterhost(mac, os, ip, nom)
		configinstall.openbsd(mac, nom, mdp_root, nom_user, mdp_user, taille_swap)
	elif os =='windows':
		# On attend un sous élément à OS si on veut du soft raid
		# il faut que root[1][0].text == 'raid' pour que le fichier unattend installe le soft raid
		try:
			#raid = root[1][1].text
			raid = root.find('OS/RAID').text
		#except IndexError:
		except AttributeError:
			raid = 'pas de soft raid'
		# On regarde si il y a un sous élément PRODUCTKEY, sinon on utilise la clé kms
		try:
			#prodkey = root[1][0].text
			prodkey = root.find('OS/PRODUCTKEY').text
		#except IndexError:
		except AttributeError:
			prodkey = 'WC2BQ-8NRM3-FDDYY-2BFGV-KHKQY'
		# il faut que le sous-élément SCRIPT existe pour que le fichier unattend exécute le script
		try:
			#scriptPs = root[1][2].text
			scriptPs = root.find('OS/SCRIPT').text
		#except IndexError:
		except AttributeError:
			scriptPs = 'PasDeScript'
		# On peut rajouter une deuxième adresse MAC dans le xml, pour palier au choix aléatoire
		# d'adresse MAC dans Windows pour la team.
		try:
			secondeMac = root.find('MACadd/MACadd2').text
		except AttributeError:
			secondeMac = 'PasDeMac'
		ajouterhost.ajouterhost(mac, os, ip, nom, mac2=secondeMac)
		fichierspxe.pxewindows(mac)
		configinstall.winunattend(mac, nom, mdp_root, raid, prodkey, ip, scriptPs)
	elif os == 'esxi':
		# On attend un sous élément à OS qui contiend la clé de licence
		try:
			# license_key = root[1][0].text
			license_key = root.find('OS/PRODUCTKEY').text
		except IndexError:
			license_key = ''
		ajouterhost.ajouterhost(mac, os, ip, nom)
		fichierspxe.pxeesxi(mac)
		configinstall.esxi(mac, mdp_root, nom_user, mdp_user, license_key)
	else:
		print('OS non supporté. Quitte le script')
		sys.exit()