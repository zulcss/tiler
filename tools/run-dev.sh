#!/bin/bash

docker run \
     -i -t --privileged \
     -v $(pwd):/usr/src \
     -v $(pwd)/data:/var/tmp/tiler \
     -v /dev:/dev \
     -v /run:/run \
     -v /sys:/sys \
     -v /var/tmp:/var/tmp \
     -v /var/www/html:/var/www/html \
     tiler
