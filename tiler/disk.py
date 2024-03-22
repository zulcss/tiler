"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""

import logging
import os
import shlex
import subprocess

from tiler import utils


class ImagePart(object):
    def __init__(self, state, config):
        self.state = state
        self.config = config

        self.logging = logging.getLogger(__name__)
        self.disk = self.config.get("disk")
        self.device = self.disk.get("device")
        self.partitiontype = self.disk.get("partitiontype")

        self.partitions = self.disk.get("partitions")
        self.filesystems = self.disk.get("filesystems")

    def run(self):
        self.create_label()
        self.create_partitions()
        self.create_filesystems()

    def create_label(self):
        label = self.disk.get("label") or "gpt"
        if os.path.exists(self.device):
            utils.run_command(
                ["parted", self.device, "--script", "mklabel", label])

    def create_partitions(self):
        """Use parted to create the partitions."""
        for index, part in enumerate(self.partitions, start=1):
            (err, out) = utils.run_command(
                ["parted", "-s", self.device, "--", "mkpart", part.get("name"),
                 part.get("start"), part.get("end")])
            flags = part.get("flags")
            if flags:
                for flag in flags:
                    cmd = f"parted -s {self.device} -- set {index} {flag} on"
                    utils.run_command(shlex.split(cmd))
            part_type = part.get("type")
            if part_type:
                cmd = f"sfdisk --part-type {self.device} {index} {part_type}"
                utils.run_command(shlex.split(cmd))

    def create_filesystems(self):
        """Setup the disk for the filesystems to be formatted."""
        for index, part in enumerate(self.filesystems, start=1):
            fs = self.get_partition_device(index, self.device)
            if os.path.exists(fs):
                self.mkfs(fs,
                          part.get("fs"),
                          part.get("label"),
                          part.get("name"))

    def mkfs(self, fs, fs_type, label, name):
        """Formatting the filesystem."""
        self.logging.info(f"Formatting filesystems for {name}.")

        if fs_type == "vfat":
            # vfat is a special case
            subprocess.run(
                ["mkfs.vfat", "-F", "32", "-n", label, fs],
                check=True)
        else:
            subprocess.run(
                ["mkfs", "-F", "-t", fs_type, "-L", label, fs], check=True)

    def get_partition_device(self, number, device):
        suffix = "p"
        # Check partition naming first: if used 'by-id'i naming convention
        if "/disk/by-id" in device:
            suffix = "-part"

        # If the iamge device has a digit as the last character, the partition
        # suffix is p<number> else it's just <number>
        last = device[len(device) - 1]
        if last >= "0" and last <= "9":
            return "%s%s%d" % (device, suffix, number)
        else:
            return "%s%d" % (device, number)
