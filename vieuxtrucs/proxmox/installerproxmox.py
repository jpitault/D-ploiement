#!/usr/bin/python3
import re
import ajouterhost
import fichierpxedebian
import ecrirepreseed

# variables
mac = input('MAC address :')
os = input('OS : ')
ip = input('Adresse IP : ')
nom = input('Hostname : ')
file = "/etc/dhcp/"+nom
mdp_root = '5BgGwXwSFs9AU'
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


ajouterhost.ajouterhost(mac, os, ip, nom, file)

fichierpxedebian.pxedebian(mac)

ecrirepreseed.debpreseed(mac, mdp_root, nom_user, mdp_user, taille_swap)
