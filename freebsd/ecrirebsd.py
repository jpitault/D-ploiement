#!/usr/bin/python3
import re

# On écrit le script d'installation de bsd, en partant du modèle et en changeant les variables
# Il faut que le script de sortie s'appelle : mac-00:11:22:33:44:aa ( définit dans l'image mfsbsd)

#mac = '001122334455'
#taille_swap= '1024'
#nom = 'testfreebsd'
#mdp_root = 'password'
#user = 'julian'
#mdp_user = 'password'


def ecrirebsd(mac, taille_swap, nom, mdp_root, nom_user, mdp_user):
	# On vérifie que l'adresse MAC en soit bien une
	X='([a-fA-F0-9]{2}[" ":\-]?){6}'
	ismac = re.compile(X).match(mac)
	if ismac:
		pass
	else:
		print('Adresse MAC invalide. Quitte le script')
		sys.exit



	# On veut une adresse MAC en majuscule, séparée par ":"
	# On commence par séparer l'adresse MAC dans une list
	listmac = re.findall('[a-fA-F0-9]{2}',mac)
	# Puis on remet en string, séparée par ":"
	mac = ":".join(listmac)
	# On met en minuscule
	mac = mac.lower()

	# Nos 2 fichiers
	modele = 'bsdinstallzfs.txt'
	outfile = '/var/www/html/mac-' + mac

	# On lit le modèle et on écrit dans la sortie
	with open(modele,"r") as in_f, open(outfile,"w") as out_f:
		# On lit, ligne par ligne
		for ligne in in_f.readlines():
			if 'SWAP=1G' in ligne:
				out_f.write('SWAP={}M\n'.format(taille_swap))
			elif 'NAME="CastleIT"' in ligne:
				out_f.write('NAME="{}"\n'.format(nom))
			elif 'MDPROOT="insecure"' in ligne:
				out_f.write('MDPROOT="{}"\n'.format(mdp_root))
			elif 'USER="username"' in ligne:
				out_f.write('USER="{}"\n'.format(nom_user))
			elif 'MDPUSER="insecure"' in ligne:
				out_f.write('MDPUSER="{}"\n'.format(mdp_user))
			else:
				out_f.write(ligne)

