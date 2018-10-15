#!/usr/bin/python3
import re
import ajouterhost
import fichierpxecentos
import ecrireks

# variables
mac = input('MAC address :')
os = input('OS : ')
ip = input('Adresse IP : ')
nom = input('Hostname : ')
file = "/etc/dhcp/"+nom
mdp_root = 'password'
nom_user = 'julian'
mdp_user = 'password'
taille_swap = '512'


# On vérifie que l'adresse MAC en soit bien une
X='([a-fA-F0-9]{2}[" ":\-]?){6}'
ismac = re.compile(X).match(mac)
if ismac:
	pass
else:
	print('Adresse MAC invalide. Quitte le script')
	sys.exit


# On appelle la fonction ajouterhost() du fichier ajouterhost
ajouterhost.ajouterhost(mac, os, ip, nom, file)

# On appelle la fonction pxecentos() du fichierpxecentos
fichierpxecentos.pxecentos(mac)

# On appelle la fonction centosks() fu fichier ecrireks
ecrireks.centosks(mac, mdp_root, nom_user, mdp_user, taille_swap)
