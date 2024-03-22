"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import logging
import os
import shutil
import sys

from tiler.mount import mount
from tiler.mount import umount
from tiler import utils


class VanillaInstall(object):
    def __init__(self, state, config):
        self.state = state
        self.config = config
        self.workspace = self.state.workspace

        self.logging = logging.getLogger(__name__)
        self.source = self.config.get("source")
        self.disk = self.config.get("disk")

    def run(self):
        """Install Debian to a disk."""
        self.logging.info("Running debian install.")

        device = self.disk.get("device")
        tarball = self.source.get("file")
        self.kernel_args = self.config.get("kernel_args")

        self.rootfs = self.workspace.joinpath("rootfs")
        if self.rootfs.exists():
            shutil.rmtree(self.rootfs)

        if not os.path.exists(tarball):
            self.logging.error(f"Unable to find tarball: {tarball}")
            sys.exit(1)

        self.logging.info(f"Mounting {device} on {self.rootfs}.")
        try:
            mount(device, self.rootfs)

            self.logging.info(f"Unpacking {tarball}.")
            utils.run_command(
                ["tar", "-C", self.rootfs,
                 "--exclude=./dev/*",
                 "-zxf", tarball, "--numeric-owner"])

            self.logging.info("Setting up bootloader.")
            utils.run_chroot_command(
                ["bootctl", "install",
                 "--no-variables",
                 "--entry-token", "os-id"],
                self.rootfs,
                efi=self.rootfs)

            self._kernel_install()

        finally:
            umount(self.rootfs)

    def _kernel_install(self):
        """Configure kernel command line."""
        self.logging.info("Cconfiguring kernel command line.")

        # Should be only one kernel.
        for d in self.rootfs.glob("boot/vmlinuz-*"):
            kver = d.name.removeprefix("vmlinuz-")

        cmdline = self.rootfs.joinpath("etc/kernel/cmdline")
        with open(cmdline, "w") as f:
            f.write(self.kernel_args)

        utils.run_chroot_command(
            ["kernel-install", "add", kver, f"/boot/vmlinuz-{kver}"],
            self.rootfs, efi=self.rootfs)
