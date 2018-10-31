import xml.etree.ElementTree as ET
import re

# On vérifie déjà si le content type est xml dans la méthode post

# On veut vérifier que le xml comprend 8 champs au premier niveau

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
	X='([a-fA-F0-9]{2}[:|\-]?){6}'
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
	X = '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}'
	ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
	ip = root[2].text
	#ip = root.find('IP').text
	estuneip = re.compile(X).match(ip)
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
	assert (osinstall in osSupport), "Le champ 1 ne contient pas un OS supporté"
	

# On ne veut pas d'espaces dans le nom qui servira de hostname
def xml_nom(xml):
	root = ET.fromstring(xml)
	nom = root[3].text
	#nom = root.find('NOM').text
	X = '[^a-zA-Z0-9_:-]'
	assert not (re.search(X, nom))
	

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
				errors = errors + '\n' + "Le champ 3 ne contient pas un nom valide. Seul les caractères alphanumériques '_' et '-' sont autorisés"
	
	return errors

"""
if validationxml(file) == '':
	print('Tout est bon')
else:
	print(validationxml(file))
"""