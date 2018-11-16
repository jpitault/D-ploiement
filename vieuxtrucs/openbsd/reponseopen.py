#!/usr/bin/python3
import re
import subprocess

# Ecrire fichier qui répond aux questions de l'installateur OpenBSD, le fichier disklabel et le set agrégat

def openbsd(mac, nom, mdp_root, nom_user, mdp_user, taille_swap):
	# Variables
	#mac = '001122334455'
	#nom = 'openbsdtest'
	#mdp_root = 'password'
	#nom_user = 'julian'
	#mdp_user = 'password'
	#taille_swap = '1024'

	# On vérifie que l'adresse MAC en soit bien une
	X='([a-fA-F0-9]{2}[" ":\-]?){6}'
	ismac = re.compile(X).match(mac)
	if ismac:
		pass
	else:
		print('Adresse MAC invalide. Quitte le script')
		sys.exit

	# on veut que la mac soit séparé par des : et en minuscules
	# On commence par séparer l'adresse MAC dans une list
	listmac = re.findall('[a-fA-F0-9]{2}',mac)
	# Puis on remet en string, séparée par ":"
	mac = ":".join(listmac)
	# On met en minuscule
	mac = mac.lower()

	# Le nom du fichier qui sera créé
	file = '/var/www/html/openbsd/' + mac + '-install.conf'

	# Le nom du fichier disklabel
	disklabel = mac + '-disklabel'
	disklabelfile = '/var/www/html/openbsd/' + disklabel

	# Puis on écrit le fichier réponse
	with open(file, 'w') as fichier:
		fichier.write('Choose your keyboard layout=fr\n')
		fichier.write('System hostname = {}\n'.format(nom))
		fichier.write('Do you expect to run the X window System = no\n')
		fichier.write('Password for root = {}\n'.format(mdp_root))
		fichier.write('Network interfaces = em0\n')
		fichier.write('IPv4 address for em0 = dhcp\n')
		fichier.write('Setup a user = {}\n'.format(nom_user))
		fichier.write('Password for user = {}\n'.format(mdp_user))
		fichier.write('What timezone are you in = Europe/Paris\n')
		fichier.write('Location of sets = http\n')
		fichier.write('HTTP Server = 192.168.0.254\n')
		fichier.write('Use http instead = yes\n')
		fichier.write('Set name(s) = -x* -g* done\n')
		fichier.write('Checksum test for site62-{}.tgz failed. Continue anyway = yes\n'.format(nom))
		fichier.write('Unverified sets: site62-{}.tgz. Continue without verification = yes\n'.format(nom))
		fichier.write('URL to autopartitioning template for disklabel = http://192.168.0.254/openbsd/{}\n'.format(disklabel))
		
		
	# On écrit le fichier Disklabel
	with open(disklabelfile, 'w') as fichier:
		fichier.write('/	500M\n')
		fichier.write('swap	{}M\n'.format(taille_swap))
		fichier.write('/tmp	1G-*	25%\n')
		fichier.write('/var	1G-*	25%\n')
		fichier.write('/usr	1G-*	25%\n')
		fichier.write('/home	1G-*	25%\n')
		
		
	# Pour la conf agrégat on a besoin d'utiliser un set
	# Pour l'instant on ne fait que copier, en renommant, un set déjà créer
	nouv_set = 'site62-' + nom + '.tgz'
	subprocess.run(['cp', 'site62.tgz', '/var/www/html/pub/OpenBSD/6.2/amd64/{}'.format(nouv_set)])
	
	# Il faut mettre à jour le fichier index
	index = '/var/www/html/pub/OpenBSD/6.2/amd64/index.txt'
	proc = subprocess.Popen(['ls', '-l', '/var/www/html/pub/OpenBSD/6.2/amd64/'], stdout=subprocess.PIPE)
	list = proc.stdout.read().decode("utf-8")
	
	with open(index, 'w') as fichier:
		fichier.write(list)
	
	#subprocess.run(['ls', '-l', '/var/www/html/pub/OpenBSD/6.2/amd64/', '>', '/var/www/html/pub/OpenBSD/6.2/amd64/index.txt'])