== source configuration ==

Unpack ruck generated tarballs to the filesytem.
Used in vanilla installs with prepared rootfs tarballs.

Only compressed tarballs are supported currently.

source:
  origin: https://192.168.100.1
  file: rootfs.tar.gz
  compression: gz
  md5sum: 013f5b44670d81280b5b1bc02455842b250df2f0c6763398feb69af1a805a14fq

Mandatory properties:

- origin -- URL where to download the rootfs tarball from.

- file -- archive's file name.

Optional parameters:

- compression -- optional hint for unapckging the rootfs.tar.gz.

- md5sum -- optional md5sum for verifying that the user is insalling the
  correct rootfs.
