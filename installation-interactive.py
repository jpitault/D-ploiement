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
#file = "/etc/dhcp/"+nom
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
else:
	print('OS non supporté. Quitte le script')
	sys.exit()
