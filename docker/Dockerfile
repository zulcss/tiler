FROM debian:bookworm

RUN apt-get update && \
    apt-get install -y \
        mmdebstrap \
        python3-pip \
        python3-yaml \
        python3-rich \
        python3-click \
        python3-systemd \
        python3-gi \
        python3-pbr \
        live-build \
        dosfstools \
        systemd-container \
        ostree \
        dosfstools \
        gir1.2-ostree-1.0 \
        git

COPY files/pip.conf /etc/pip.conf

# Needed for ruck - change me when there is a proper repo.
RUN pip3 install -e git+https://github.com/zulcss/ruck.git#egg=ruck
RUN mkdir -p /var/www/html

RUN mkdir -p usr/src

WORKDIR /usr/src
