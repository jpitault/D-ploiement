# Scripts déploiement DHCP/TFTP(PXE) avec API 

Déployer différents OS en utilisant une interface API REST à l'aide d'un serveur DHCP, d'un serveur TFTP et d'un serveur SAMBA pour Windows.
OS présents :
 - Debian
 - Ubuntu
 - CentOS
 - FreeBSD
 - OpenBSD
 - Proxmox

## Prérequis

Serveur DHCP (isc-dhcp-server)
Serveur TFTP (tftpd-hpa)
Serveur Web (apache2)
Falcon https://falconframework.org/
Gunicorn https://gunicorn.org/

## L'API REST

L'API REST répond sur les URL /hosts /hosts/{uuid} et /hosts/ip
Elle fonctionne avec des fichiers .xml qui ont le format :
<host>
	<MACadd>001122334455</MACadd>
	<OS>debian</OS>
	<IP>192.168.0.X</IP>
	<NOM>hostname</NOM>
	<MDP_ROOT>passwordroot</MDP_ROOT>
	<NOM_USER>username</NOM_USER>
	<MDP_USER>passworduser</MDP_USER>
	<SWAP>1024</SWAP>
</host>

Le nom des champs n'a pas d'importance mais leurs ordre doit être respecté.
Le SWAP est en MO

Quand elle reçoit une requête POST, elle vérifie que le header content-type = application/xml


### Sur /hosts
---> GET
Retourne la liste de tous les hosts actuellement sur le serveur, sous la forme :

uuid
<Contenu du XML>
uuid
<Contenu du XML>
etc...

---> POST
Attend une requête qui contient content-type = application/xml
Puis elle utilise un script qui vérifie le contenue du xml :
 - 8 champs présents sous la racine
 - Le premier champ contient quelque chose qui a le format d'une adresse MAC, séparée par des ":", des "-" ou rien du tout
 - Le deuxième champ contient le nom d'un OS supporté
 - Le troisième champ contient une adresse IP

Elle renvoie une erreur 415 si une de ces conditions n'est pas respecté.
Sinon elle crée sur le serveur le fichier xml reçu et lance avec lui comme argument, le script qui crée les fichiers de conf
nécessaire au déploiement.

### Sur /hosts/{uuid}

L'universally unique identifier (uuid) est donné à la création d'une ressource et dans le résultat d'une requête GET sur /hosts.

---> GET
Répond avec le contenu xml de l'objet définit par l'uuid si l'uuid a été trouvé.
Sinon répond avec une erreur 404 et le message : "Host {uuid} n'a pas été trouvé.".

---> DELETE
Exécute un script qui supprime tous les fichiers crées à l'ajout de la ressource et supprime la ressource, si l'uuid a été trouvé.
Sinon répond avec une erreur 404 et le message : "Host {uuid} n'a pas été trouvé.".

### Sur /hosts/ip

---> GET
Renvoie une liste, sous forme de texte, qui fait le lien entre les hostnames et les IPs définit dans les ressources sur le serveur.
Sous la forme :
hostname1 : ip1
hostname2 : ip2
...


## Scripts python

### Pour l'API REST

apiDeploiement.py contient l'app qui utilise falcon et qui est servit par gunicorn.
Il contient l'emplacement où sont stocké les fichiers reçut par l'API.

Pour lancer l'app :
```bash
gunicorn apiDeploiement:api
```

### Vérification du contenue du xml

c'est le script verifxml.py qui s'en charge.

### Pour une installation

Scripts nécessaires pour l'ajout d'un host :
 - installationxml : prend un fichier xml et lance les scripts :
   - ajouterhost : s'occupe de la configuration du DHCP
   - fichierspxe : s'occupe de la configuration du PXE (fichier dans le serveur tftp)
   - configinstall : s'occupe de la création des fichiers requis pour ou pendant l'installation, avec les paramètres du .xml

Ils assument :
 - Que la conf du DHCP est à /etc/dhcp
 - Le serveur TFTP a pour racine /srv/tftp/ et qu'il utilise ensuite un dossier pour chaque OS
 - Pour OpenBSD, il existe une archive .tgz appellé site62.tgz qui sert de modèle
 
Le script bsdinstallzfs.txt est utilisé comme modèle par configinstall lors de la création des fichiers d'installation de freebsd.


### Pour la suppresion d'une ressource

suppressionhote.py supprime les fichiers DHCP, PXE et de configuration d'installation.

### Les autres

Les autres scripts et ceux qui sont dans les dossiers ne servent pas au déploiement par API.
Ils ne sont pas à jour.