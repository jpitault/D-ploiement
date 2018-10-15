#!/usr/bin/python3
import re
import sys
import ajouterhost
import configinstall
import fichierspxe
import xml.etree.ElementTree as ET


xml = input('Quel fichier faut il lire ? :')
tree = ET.parse(xml)
root = tree.getroot()

# Installation d'une machine

# Variables
mac = root[0].text
os = root[1].text
ip = root[2].text
nom = root[3].text
file = "/etc/dhcp/"+nom
mdp_root = root[4].text
nom_user = root[5].text
mdp_user = root[6].text
taille_swap = root[7].text


# On vérifie que l'adresse MAC en soit bien une
X='([a-fA-F0-9]{2}[" ":\-]?){6}'
ismac = re.compile(X).match(mac)
if ismac:
	pass
else:
	print('Adresse MAC invalide. Quitte le script')
	sys.exit('mauvaise MAC')
	

# On crée un host pour le DHCP, 1 seul script
ajouterhost.ajouterhost(mac, os, ip, nom, file)


# On crée un fichier pour le boot pxe
if os == 'debian2':
	fichierspxe.pxedebian(mac)
	configinstall.debian(mac, mdp_root, nom_user, mdp_user, taille_swap)
elif os == 'centos':
	fichierspxe.pxecentos(mac)
	configinstall.centos(mac, mdp_root, nom_user, mdp_user, taille_swap)
elif os == 'freebsd':
	fichierspxe.pxefreebsd(mac)
	configinstall.freebsd(mac, taille_swap, nom, mdp_root, nom_user, mdp_user)
else:
	print('OS non supporté. Quitte le script')
	sys.exit