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
	mac = root[0].text
	os = root[1].text
	ip = root[2].text
	nom = root[3].text
	#file = "/etc/dhcp/"+nom
	mdp_root = root[4].text
	nom_user = root[5].text
	mdp_user = root[6].text
	taille_swap = root[7].text

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
	if os == 'debian2' or os == 'debian':
		os = 'debian2'
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
	elif os == 'ubuntu2' or os == 'ubuntu':
		os = 'ubuntu2'
		# On crée un host pour le DHCP, 1 seul script
		ajouterhost.ajouterhost(mac, os, ip, nom)
		fichierspxe.pxeubuntu(mac)
		configinstall.ubuntu(mac, mdp_root, nom_user, mdp_user, taille_swap)
	elif os == 'proxmox':
		os = 'debian2'
		# On crée un host pour le DHCP, 1 seul script
		ajouterhost.ajouterhost(mac, os, ip, nom)
		fichierspxe.pxedebian(mac)
		configinstall.proxmox(mac, mdp_root, nom_user, mdp_user, taille_swap)
	elif os == 'openbsd':
		ajouterhost.ajouterhost(mac, os, ip, nom)
		configinstall.openbsd(mac, nom, mdp_root, nom_user, mdp_user, taille_swap)
	elif os =='windows':
		ajouterhost.ajouterhost(mac, os, ip, nom)
		fichierspxe.pxewindows(mac)
		configinstall.winunattend(mac, nom, mdp_root)
	else:
		print('OS non supporté. Quitte le script')
		sys.exit()