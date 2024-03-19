#!/bin/bash
#

DATE=`date +%Y%m%d`

if [ -f pablo-live.iso ]; then
   rm -f pablo-live-$DATE.iso
fi

if [ -d config ]; then
    rm -rf config
fi

cp -rp pablo-config config

lb clean
lb config
lb build

mv live-image-amd64.hybrid.iso pablo-live-$DATE.iso
