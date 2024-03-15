FROM debian:bookworm

RUN apt-get update && \
    apt-get install -y \
        dosfstools \
        python3-pip \
        python3-yaml \
        python3-rich \
        python3-click \
        python3-gi \
        dosfstools \
        systemd-container \
        ostree \
        dosfstools \
        gir1.2-ostree-1.0 \
        git

COPY files/pip.conf /etc/pip.conf

RUN mkdir -p usr/src

