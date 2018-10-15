#!/usr/bin/python3
import re
import ajouterhost
import configinstall
import fichierspxe


# Installation d'une machine

# Variables
mac = input('Adresse MAC :')
os = input('OS : ')
ip = input('Adresse IP : ')
nom = input('Hostname : ')
file = "/etc/dhcp/"+nom
mdp_root = 'password'
nom_user = 'julian'
mdp_user = 'password'
taille_swap = '1024'


# On vérifie que l'adresse MAC en soit bien une
X='([a-fA-F0-9]{2}[" ":\-]?){6}'
ismac = re.compile(X).match(mac)
if ismac:
	pass
else:
	print('Adresse MAC invalide. Quitte le script')
	sys.exit
	

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