# Scripts déploiement DHCP/TFTP(PXE) avec API 

Déployer différents OS en utilisant une interface API REST à l'aide d'un serveur DHCP, d'un serveur TFTP et d'un serveur SAMBA pour Windows.
OS présents :
 - Debian
 - Ubuntu
 - CentOS
 - FreeBSD
 - OpenBSD
 - Proxmox
 - Windows
 - ESXi

## Prérequis

 - Serveur DHCP (isc-dhcp-server)
 - Serveur TFTP (tftpd-hpa)
 - Serveur Web (apache2)
 - Serveur SAMBA (pour Windows)
 - Falcon https://falconframework.org/
 - Gunicorn https://gunicorn.org/

## L'API REST

L'API REST répond sur les URL /hosts /hosts/{uuid} et /hosts/ip
Elle fonctionne avec des fichiers .xml qui ont le format :
```xml
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
```
Pour Windows et ESXi, on peut ajouter des sous-éléments à OS. Pour indiquer la clé de produit et pour Windows si on veut du software RAID,
la seconde adresse MAC pour l'agrégat et exécuter un script.
Il ne faut pas qu'il y ait d'espaces ou de retour à la ligne entre le nom de l'OS et un sous-élément.
```xml
<host>
	<MACadd>001122334455<MACadd2>998877665544</MACadd2></MACadd>
	<OS>windows<PRODUCTKEY>AAAA-BBBB-DDDD</PRODUCTKEY><RAID>raid</RAID><SCRIPT>scriptpowershell.ps1</SCRIPT>
	</OS>
	<IP>192.168.0.X</IP>
	<NOM>hostname</NOM>
	<MDP_ROOT>passwordroot</MDP_ROOT>
	<NOM_USER>username</NOM_USER>
	<MDP_USER>passworduser</MDP_USER>
	<SWAP>1024</SWAP>
</host>
```
Il y avait un mix, où certaines fonctions ne regardait que le nom du champ et d'autres, sa position relative aux autres. 
Normalement, toutes les fonctions ne regarde que le nom du champ désormais.
Le SWAP est en MO.

Quand elle reçoit une requête POST, elle vérifie que le header content-type = application/xml.


### Sur /hosts
---> GET
Retourne la liste de tous les hosts actuellement sur le serveur, sous la forme :

```
uuid
<Contenu du XML>
uuid
<Contenu du XML>
etc...
```

---> POST
Attend une requête qui contient content-type = application/xml
Puis elle utilise un script (verifxml.py) qui vérifie le contenu du xml :
 - 8 champs présents sous la racine
 - Les champs <MACadd> et <MACadd2> contiennent quelque chose qui a le format d'une adresse MAC, séparée par des ":", des "-" ou rien du tout. Et qu'une ressource déjà existante ne contient pas la même adresse MAC.
 - Le champ <OS> contient le nom d'un OS supporté
 - Le champ <IP> contient une adresse IP locale (RFC1918)
 - Le champ <NOM> contient un nom dans lequel il n'y a que des caractères acceptés (alphanumériques, "-", "_" et ":"). Et pour Windows si le nom contient moins de 15 caractères. Vérifie aussi si le nom n'est pas déjà utilisé par le DHCP.
 - Si on essaie d'installer ESXi, que le cinquième <MDP_ROOT> contient un mot de passe qui vérifie les demandes d'ESXi.
 - Le sixième champ <NOM_USER>contient un nom d'utilisateur, fait de caractères alphanumériques et sans espaces.


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

```
hostname1 : ip1
hostname2 : ip2
...
```

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
 - Que la conf du DHCP se trouve dans le dossier /etc/dhcp
 - Le serveur TFTP a pour racine /srv/tftp/ et qu'il utilise ensuite un dossier pour chaque OS
 - Pour OpenBSD, il existe une archive .tgz appellé site62.tgz qui sert de modèle
 
Le script bsdinstallzfs.txt est utilisé comme modèle par configinstall lors de la création des fichiers d'installation de freebsd.


### Pour la suppresion d'une ressource

suppressionhote.py supprime les fichiers DHCP, PXE et de configuration d'installation.

### Variable à changer

Le fichier varconfig.py contient plusieurs variables, celle de l'ip du serveur web, de la gateway et du DNS. Elle sont appelées dans les scripts :
 - fichierspxe.py
 - configinstall.py

Et la version de OpenBSD, appelée dans :
 - configinstall.py
 - suppressionhote.py

Et le chemin où les fichiers xml sont stockés :
 - apiDeploiement.py
 - verifxml.py
 
### Les autres

Les autres scripts et ceux qui sont dans les dossiers ne servent pas au déploiement par API. Le dossier scriptpostinstall contient 
des scripts shell pour référence.
Ils ne sont pas à jour.