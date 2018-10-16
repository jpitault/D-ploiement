#!/bin/sh

# Supprimer les traces du programme ajouterhost.py 

echo "Cible pour désigner les lignes à supprimer :"

read cible

# Supprimer le fichier qui contient la config host
fichier="/etc/dhcp/$cible"
rm "$fichier"

# Supprimer la ligne qui include le fichier host dans le fichier /etc/dhcp/dhcpd.conf
grep -v "$cible" /etc/dhcp/dhcpd.conf > temp && mv temp /etc/dhcp/dhcpd.conf
