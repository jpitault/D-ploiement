import re


def esxi(mac, MDP_ROOT, NOM_USER, MDP_USER):
	# On veut une adresse MAC en minuscule, séparée par "-"
	# On commence par séparer l'adresse MAC dans une list
	listmac = re.findall('[a-fA-F0-9]{2}',mac)
	# Puis on remet en string, séparée par ":"
	mac = "-".join(listmac)
	# On met en minuscule
	mac = mac.lower()

	nom_preseed = '/var/www/html/' + mac + "esxi.cfg"


	# On écrit le fichier
	with open(nom_preseed,'w') as fichier:
		fichier.write('#\n')
		fichier.write('# Sample scripted installation file\n')
		fichier.write('#\n')
		fichier.write('\n')
		fichier.write('# Accept the VMware End User License Agreement\n')
		fichier.write('vmaccepteula\n')
		fichier.write('\n')
		fichier.write('# Set the root password for the DCUI and Tech Support Mode chiffré ou password\n')
		fichier.write('#rootpw --iscrypted <mdpchiffré>\n')
		fichier.write('rootpw {}\n'.format(MDP_ROOT))
		fichier.write('\n')
		fichier.write('# Installe sur le premier disque trouvé, cherche en premier local, puis sur le network et enfin USB.\n')
		fichier.write('# overwritevmfs Supprime un VMFS datastore si il y en a un présent sur le disque.\n')
		fichier.write('install --firstdisk --overwritevmfs\n')
		fichier.write('\n')
		fichier.write('# On met le clavier en français\n')
		fichier.write("keyboard 'French'\n")
		fichier.write('\n')
		fichier.write('# Configure la licence, si non-inclus ESXi installe en mode évaluation\n')
		fichier.write('#vmserialnum --esx=<license-key>\n')
		fichier.write('\n')
		fichier.write('# Set the network to DHCP on the first network adapter\n')
		fichier.write('network --bootproto=dhcp --device=vmnic0\n')
		fichier.write('#network --bootproto=static --addvmportgroup=0 --device=vmnic0 --ip=${IPADDR} --netmask=${NETMASK} --gateway=${GATEWAY} --nameserver=${DNS} --hostname=${HOSTNAME}\n')
		fichier.write('\n')
		fichier.write("# On indique à la machine si elle doit redémarrer après l'installation\n")
		fichier.write('reboot\n')
		fichier.write('\n')
		fichier.write("# On peut spécifier un autre script d'installation\n")
		fichier.write('#%include /tmp/networking.cfg\n')
		fichier.write('\n')
		fichier.write('\n')
		fichier.write("# On peut avoir un script qui s'exécute avant le fichier kickstart. Par exemple, on peut l'utiliser pour générer des fichiers\n")
		fichier.write('# que le kickstart utilisera\n')
		fichier.write('# 2 interpreteurs possibles : busybox ou python (par défaut busybox)\n')
		fichier.write('#%pre --interpreter=busybox\n')
		fichier.write(' \n')
		fichier.write('## extract network info from bootup\n')
		fichier.write('#VMK_INT="vmk0"\n')
		fichier.write('#VMK_LINE=$(localcli network ip interface ipv4 get | grep "${VMK_INT}")\n')
		fichier.write('#IPADDR=$(echo "${VMK_LINE}" | awk \'{print $2}\')\n')
		fichier.write('#NETMASK=$(echo "${VMK_LINE}" | awk \'{print $3}\')\n')
		fichier.write('#GATEWAY=$(localcli network ip route ipv4 list | grep default | awk \'{print $3}\')\n')
		fichier.write('#DNS="172.30.0.100,172.30.0.200"\n')
		fichier.write('#HOSTNAME=$(nslookup "${IPADDR}" "${DNS}" | grep Address | grep "${IPADDR}" | awk \'{print $4}\')\n')
		fichier.write(' \n')
		fichier.write('#echo "network --bootproto=static --addvmportgroup=false --device=vmnic0 --ip=${IPADDR} --netmask=${NETMASK} --gateway=${GATEWAY} --nameserver=${DNS} --hostname=${HOSTNAME}" > /tmp/networking.cfg\n')
		fichier.write(' \n')
		fichier.write('\n')
		fichier.write("# On peut exécuter de la même manière un script après l'installation des packages\n")
		fichier.write('#%post --interpreter=python --ignorefailure=true\n')
		fichier.write('#import time\n')
		fichier.write("#stampFile = open('/finished.stamp', mode='w')\n")
		fichier.write('#stampFile.write( time.asctime() )\n')
		fichier.write('\n')
		fichier.write('\n')
		fichier.write("# On peut créer un script qui s'exécutera seulement au premier boot\n")
		fichier.write('%firstboot --interpreter=busybox\n')
		fichier.write('# active et démarre le service ssh\n')
		fichier.write('vim-cmd hostsvc/enable_ssh\n')
		fichier.write('vim-cmd hostsvc/start_ssh\n')
		fichier.write('\n')
		fichier.write('# active et démarre la console ESXi\n')
		fichier.write('vim-cmd hostsvc/enable_esx_shell\n')
		fichier.write('vim-cmd hostsvc/start_esx_shell\n')
		fichier.write('\n')
		fichier.write('%firstboot --interpreter=busybox\n')
		fichier.write("esxcli system account add -d 'description du compte' -i {0} -p {1} -c {1}\n".format(NOM_USER, MDP_USER))
		fichier.write('esxcli system permission set -i {} -r Admin\n'.format(NOM_USER))
		fichier.write('# assign license')
		fichier.write('#vim-cmd vimsvc/license --set AAAAA-BBBBB-CCCCC-DDDDD-EEEEE')
		fichier.write('##vSwitch configuration\n')
		fichier.write('# Attacher vmnic1 à vSwitch0\n')
		fichier.write('esxcli network vswitch standard uplink add --uplink-name vmnic1 --vswitch-name vSwitch0\n')