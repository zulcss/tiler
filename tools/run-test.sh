#!/bin/bash

DATE=`date +%Y%m%d`
LIBVIRT_STORAGE_PATH="/var/lib/libvirt/images/"


virt-install --name tiler-test \
    --osinfo debian12 \
    --boot loader=/usr/share/ovmf/OVMF.fd \
    --video virtio \
    --disk path=$LIBVIRT_STORAGE_PATH/tiler-test-disk0.qcow2,format=qcow2,size=20,device=disk,bus=virtio,cache=none \
    --cdrom live-config/pablo-live-$DATE.iso \
    --noautoconsole \
    --memory 3048 \
    --vcpu 2
