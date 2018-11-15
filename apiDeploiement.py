import falcon
import uuid
import os
import installationxml as ix
import suppressionhote as suph
import xml.etree.ElementTree as ET
import verifxml 

ALLOWED_FILE_TYPE = (
	'application/xml',
)

# Chemin ou seront stockés les ressources
storage_path='/root/fichiersxml'
if not os.path.exists(storage_path):
	os.makedirs(storage_path)

def validate_file_type(req, resp, resource, params):
	"""Vérifie que la requête POST a pour content_type xml
	Il faut l'utiliser avant une méthode où une classe pour
	qu'elle agisse sur celle-ci
	"""
	if req.content_type not in ALLOWED_FILE_TYPE:
		msg = 'Le format du fichier doit être XML'
		raise falcon.HTTPBadRequest('Bad request', msg)

class Hosts(object):
	# Chemin pour le fichier POST
	def __init__(self, storage_path):
		self._storage_path = storage_path
	
	# Gère les requêtes get
	#def on_get(self, req, resp):
	#	resp.status = falcon.HTTP_200
	#	# On sert un fichier xml 
	#	with open('/root/scriptxml/exemple.xml', 'r') as fichier:
	#		contents = fichier.read()
	#	# On affiche le fichier xml
	#	resp.body = contents
		
	# Get affiche tous les fichiers xml présents dans le dossier
	def on_get(self, req, resp):
		resp.status = falcon.HTTP_200
		mbody = ''
		if os.listdir(self._storage_path) == []:
			resp.body = "Il n'y a aucun hôte enregistré"
			resp.content_type = falcon.MEDIA_TEXT
		else:
			for file in os.listdir(self._storage_path):
				name = os.path.join(self._storage_path, file)
				with open(name, 'r') as fichier:
					contents = fichier.read()
					mbody = mbody + file + '\n' + contents 
			resp.body = mbody
			resp.content_type = falcon.MEDIA_XML
		
	# Gère les requêtes post
	@falcon.before(validate_file_type)
	def on_post(self, req, resp):
		# On lit le contenue de la requête, on le met en string
		data = req.stream.read().decode('utf-8')
		#print(data)
		# On exécute un script qui retourne une string vide si on accepte la data envoyé
		# Sinon retourne une string avec les problèmes que l'on a trouvé.
		test = verifxml.validationxml(data)
		if test != '':
			#print(test)
			resp.status = falcon.HTTP_415
			resp.body = test
			resp.content_type = falcon.MEDIA_TEXT
		else:
			#print("Tout va bien")
			resp.status = falcon.HTTP_201
			# On lui donne un nom unique
			name = '{uuid}'.format(uuid=uuid.uuid4())
			# On définit le chemin où le contenue sera sauvegardé
			res_path = os.path.join(self._storage_path, name)
			# On écrit le fichier sur le serveur
			with open(res_path, 'w') as fichier:
				fichier.write(data)
			# Location header pour la ressource
			resp.location = '/hosts/' + name
			
			# On exécute le script qui prépare l'intalle
			ix.installxml(res_path)
			
		
class Host(object):
	"""Affiche ou supprime un host 
	"""
	def __init__(self, storage_path):
		self._storage_path = storage_path
		
	def on_get(self , req, resp, name):
		if name in os.listdir(self._storage_path):
			resp.status = falcon.HTTP_200
			name_path = os.path.join(self._storage_path, name)
			
			with open(name_path, 'r') as fichier:
				contents = fichier.read()
			resp.body = contents
			resp.content_type = falcon.MEDIA_XML
		else:
			message = 'Host {} n\'a pas été trouvé.'.format(name)
			resp.content_type = falcon.MEDIA_TEXT
			resp.status = falcon.HTTP_404
			resp.body = message
		
	def on_delete(self, req, resp, name):
		if name in os.listdir(self._storage_path):
			resp.status = falcon.HTTP_200
			# Le fichier xml
			name_path = os.path.join(self._storage_path, name)
			# On lit le fichier xml pour supprimer les fichiers crées à sa création
			suph.menagexml(name_path)
			# On supprime le fichier xml
			os.remove(name_path)
		else:
			message = 'Host {} n\'a pas été trouvé.'.format(name)
			resp.content_type = falcon.MEDIA_TEXT
			resp.status = falcon.HTTP_404
			resp.body = message			
			
class UsedIP(object):
	"""Affiche les IP utilisés par les fichiers xml
	"""
	def __init__(self, storage_path):
		self._storage_path = storage_path
		
	def on_get(self, req, resp):
		tempbody = ''
		for file in os.listdir(self._storage_path):
			name_path = os.path.join(self._storage_path, file)
			tree = ET.parse(name_path)
			root = tree.getroot()
			#nom = root[3].text
			nom = root.find("NOM").text
			#ip = root[2].text
			ip = root.find("IP").text
			tempbody = tempbody + nom + '	:	' + ip + '\n'
		resp.body = tempbody
		resp.content_type = falcon.MEDIA_TEXT

			
api = falcon.API()



api.add_route('/hosts', Hosts(storage_path))
api.add_route('/hosts/{name}', Host(storage_path))
api.add_route('/hosts/ip', UsedIP(storage_path))