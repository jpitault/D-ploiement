import falcon
import uuid
import os
import installationxml as ix
import suppressionhote as suph


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
		#allfiles = ['red', 'blue']
		mbody = ''
		for file in os.listdir(self._storage_path):
			name = os.path.join(self._storage_path, file)
			with open(name, 'r') as fichier:
				contents = fichier.read()
				mbody = mbody + file + '\n' + contents 
		#	allfiles.append(contents)
		resp.body = mbody
		resp.content_type = falcon.MEDIA_XML
		
	# Gère les requêtes post	
	def on_post(self, req, resp):
		resp.status = falcon.HTTP_201
		# On lit le contenue de la requête, on le met en string
		data = req.stream.read().decode('utf-8')
		#print(data)
		# On lui donne un nom unique
		name = '{uuid}'.format(uuid=uuid.uuid4())
		# On définit le chemin où le contenue sera sauvegardé
		res_path = os.path.join(self._storage_path, name)
		# On écrit le fichier sur le serveur
		with open(res_path, 'w') as fichier:
			fichier.write(data)
		# Location header pour la ressource
		resp.location = '/host/' + name
		
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
			
		
		
api = falcon.API()

api.add_route('/hosts', Hosts(storage_path='/root/fichiersxml'))
api.add_route('/hosts/{name}', Host(storage_path='/root/fichiersxml'))