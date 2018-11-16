#!/usr/bin/python3
import re
import ajouterhost
import reponseopen


# Installation d'une machine avec OpenBSD

# Variables
mac = input('Adresse MAC :')
os = 'openbsd'
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
	
	
ajouterhost.ajouterhost(mac, os, ip, nom)
reponseopen.openbsd(mac, nom, mdp_root, nom_user, mdp_user, taille_swap)