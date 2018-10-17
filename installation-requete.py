import falcon
import uuid
import os
import installationxml as ix


class host(object):
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
		resp.location = '/test/' + name
		
		# On exécute le script qui prépare l'intalle
		ix.installxml(res_path)
		
		
api = falcon.API()

api.add_route('/test', host(storage_path='/root/fichiersxml'))