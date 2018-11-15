#!/usr/bin/python3
# nécessaire pour lancer des commandes dans le shell
import subprocess
import re


def ajouterhost(mac, os, ip, nom, **kwargs):
	file = "/etc/dhcp/"+nom

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
	# On met en majuscule
	mac = mac.upper()

	# Créer un fichier host
	with open(file, "w") as fichier:
		fichier.write("host {} ".format(nom))
		fichier.write("{\n")
		fichier.write("  hardware ethernet {};\n".format(mac))
		if os == 'openbsd':
			fichier.write('  filename "{}/auto_install";\n'.format(os))
		else:
			fichier.write('  filename "{}/pxelinux.0";\n'.format(os))
		fichier.write('  fixed-address {};\n'.format(ip))
		fichier.write('  option host-name "{}";'.format(nom))
		fichier.write('\n}')
		# On écrit la seconde adresse MAC
		for key, value in kwargs.items():
			if key == 'mac2'  and value != 'PasDeMac':
				fichier.write("\nhost {}Secondaire ".format(nom))
				fichier.write("{\n")
				fichier.write("  hardware ethernet {};\n".format(value))
				if os == 'openbsd':
					fichier.write('  filename "{}/auto_install";\n'.format(os))
				else:
					fichier.write('  filename "{}/pxelinux.0";\n'.format(os))
				fichier.write('  fixed-address {};\n'.format(ip))
				fichier.write('  option host-name "{}";'.format(nom))
				fichier.write('\n}')

	# Ajoute le fichier host créer à dhcpd.conf
	with open("/etc/dhcp/dhcpd.conf", "a") as fichier:
			fichier.write('include "{}";\n'.format(file))

	# Redémarre le service DHCP
	subprocess.run(["systemctl", "restart", "isc-dhcp-server.service"])

