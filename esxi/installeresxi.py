import re
import sys
import ajouterhost
import fichierpxeesxi
import ecrireksesxi


# variables
mac = '112233445566'
os = 'esxi'
ip = '192.168.0.191'
nom = 'esxitest'
mdp_root = 'password16$'
nom_user = 'nomuser'
mdp_user = 'password16$'

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
	
	
ajouterhost.ajouterhost(mac, os, ip, nom)
fichierpxeesxi.pxeesxi(mac)
ecrireksesxi.esxi(mac, mdp_root, nom_user, mdp_user)