#!/bin/sh

grub-install /dev/sdb
update-grub /dev/sdb

#lvremove -f /dev/volume_group00/asupprimer
#lvextend /dev/volume_group00/root /dev/md1
