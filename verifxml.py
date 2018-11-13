import xml.etree.ElementTree as ET
import re
import os

# On vérifie déjà si le content type est xml dans la méthode post

# On veut vérifier que le xml comprend 8 champs au premier niveau

"""
Le fichier xml doit correspondre au modèle 
<host>
	<MACadd>080027777777</MACadd>
	<OS>ubuntu</OS>
	<IP>192.168.0.77</IP>
	<NOM>TESTAPIMAC2</NOM>
	<MDP_ROOT>password</MDP_ROOT>
	<NOM_USER>julian</NOM_USER>
	<MDP_USER>password</MDP_USER>
	<SWAP>1024</SWAP>
</host>

"""


def xml_taille(xml):
	#tree = ET.parse(xml)
	#root = tree.getroot()
	root = ET.fromstring(xml)
	assert (len(list(root)) == 8), "Le fichier doit comprendre 8 champs"

	
# On veut vérifier que le champ [0] est bien une adresse MAC
def xml_mac(xml):
	#tree = ET.parse(xml)
	#root = tree.getroot()
	root = ET.fromstring(xml)
	#X='([a-fA-F0-9]{2}[:|\-]?){6}'
	X='^([a-fA-F0-9]{2})([:|\-]?[a-fA-F0-9]{2}){5}$'
	mac = root[0].text
	#mac = root.find('MACadd').text
	estunemac = re.compile(X).match(mac)
	
	assert (estunemac), "Le champ 0 n'est pas une mac"
	#print("Le champ 0 a le format d'une MAC")


# On veut vérifier que le champ 2 est bien une IP

def xml_ip(xml):
	#tree = ET.parse(xml)
	#root = tree.getroot()
	root = ET.fromstring(xml)
	X = '^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$'
	ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
	ipRFC1918 = '^(((^127\.)|(^10\.))(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.|(^192\.168\.)|((^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)))(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
	ip = root[2].text
	#ip = root.find('IP').text
	estuneip = re.compile(ipRFC1918).match(ip)
	assert (estuneip), "Le champ 2 n'est pas une IP"

	
# On veut vérifier que le champ 1 est bien un os supporté
def xml_os(xml):
	#tree = ET.parse(xml)
	#root = tree.getroot()
	root = ET.fromstring(xml)
	osSupport = ['debian','ubuntu','centos','proxmox','freebsd','openbsd','windows','esxi']
	osinstall = root[1].text
	#osinstall = root.find('OS').text
	osinstall = osinstall.lower()
	# containOs = 0
	# for o in osSupport:
		# if o in osinstall:
			# containOs = 1
	# assert (containOs == 1)
	assert (osinstall in osSupport), "Le champ 1 ne contient pas un OS supporté"
	


def xml_nom(xml):
	# On ne veut pas d'espaces dans le nom qui servira de hostname
	root = ET.fromstring(xml)
	nom = root[3].text
	#nom = root.find('NOM').text
	# Windows n'accepte pas les noms de plus de 15 caractères
	if root.find('OS').text.lower() == 'windows':
		X = '^[a-zA-Z0-9_-]{1,15}$'
	else:
		X = '^[a-zA-Z0-9_:-]+$'
	nomvalide = re.compile(X).match(nom)
	assert (nomvalide)
	"""FACON ALAMBIQUE
	X = '[^a-zA-Z0-9_:-]'
	assert not (re.search(X, nom))
	"""
	# On ne veut pas que le nom soit déjà utilisé non plus
	list = os.listdir(path='/etc/dhcp')
	assert not (nom in list)
	
	

# Check sur le champ username	
def xml_username(xml):
	# On veut pas d'espaces dans le nom d'utilisateur
	root = ET.fromstring(xml)
	username = root[5].text
	#username = root.find('NOM_USER').text
	X = '^[a-zA-Z0-9_:-]+$'
	usernameValide = re.compile(X).match(username)
	assert (usernameValide)
	
	
	
"""
ESXi ne s'installe pas si le mot de passe définit n'atteint pas une certaine complexité.
Il faut 7 caractères et que ces caractères proviennent d'au moins 3 classes différentes, plus :
The password policy in ESXi 6 has following requirements:
Passwords must contain characters from at least three character classes.
Passwords containing characters from three character classes must be at least seven characters long.
Passwords containing characters from all four character classes must be at least seven characters long.
An uppercase character that begins a password does not count toward the number of character classes used.
A number that ends a password does not count toward the number of character classes used.

Regex tentative : 
^(^(?!\D+\d$)(?!^([A-Z])[a-z\d@$!%*?&]{7,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*\d)|(?!^([A-Z])[a-z\d@$!%*?&]{7,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[@$!%*#?&])|^(?!\D+\d$)(?!^([A-Z])[a-z\d@$!%*?&]{7,}$)(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])|^(?!\D+\d$)(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&]))[A-Za-z\d@$!%*?&]{7,}$

"""
def xml_password(xml):
	# Regex qui vérifie que le mot de passe sera accepté par ESXi
	esxiReq = '^(^(?!\D+\d$)(?!^([A-Z])[a-z\d@$!%*?&]{7,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*\d)|(?!^([A-Z])[a-z\d@$!%*?&]{7,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[@$!%*#?&])|^(?!\D+\d$)(?!^([A-Z])[a-z\d@$!%*?&]{7,}$)(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])|^(?!\D+\d$)(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&]))[A-Za-z\d@$!%*?&]{7,}$'
	# On regarde le mdp de root
	root = ET.fromstring(xml)
	mdp_root = root[4].text
	#mdp_root = root.find('MDP_ROOT').text
	esxiValide = re.compile(esxiReq).match(mdp_root)
	assert (esxiValide), "Le mot de passe ne répond pas aux exigences d'ESXi"

# On rassemble le tout
def validationxml(xml):
	errors = ''
	try:
		root = ET.fromstring(xml)
	except ET.ParseError as e:
		errors = errors + "Le fichier n'est pas conforme au format XML."
	else:
		try:
			xml_taille(xml)
		except AssertionError:
			errors = errors + "Le fichier XML ne comprend pas 8 champs"
		else:
			try:
				xml_mac(xml)
			except AssertionError:
				errors = errors + '\n' + "Le champ 0 ne contient pas une MAC valide"
			try:
				xml_ip(xml)
			except AssertionError:
				errors = errors + '\n' + "Le champ 2 ne contient pas une IP valide"
			try:
				xml_os(xml)
			except AssertionError:
				errors = errors + '\n' + "Le champ 1 ne contient pas le nom d'un OS supporté"
			try:
				xml_nom(xml)
			except AssertionError:
				errors = errors + '\n' + "Le champ 3 ne contient pas un nom valide où déjà utilisé. Seul les caractères alphanumériques, '_' et '-' sont autorisés. Windows nécessite moins de 15 caractères."
			try:
				xml_username(xml)
			except AssertionError:
				errors = errors + '\n' + "Le champ 5 ne contient pas un nom valide. Seul les caractères alphanumériques, '_' et '-' sont autorisés." 
			osinstall = root[1].text
			#osinstall = root.find('OS').text
			osinstall = osinstall.lower()
			if osinstall == 'esxi':
				try:
					xml_password(xml)
				except AssertionError:
					errors = errors + '\n' + "Le mot de passe root ne répond pas aux exigences d'ESXi"
	
	return errors

"""
if validationxml(file) == '':
	print('Tout est bon')
else:
	print(validationxml(file))
"""
