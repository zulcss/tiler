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


class OstreeDeploy(object):
    def __init__(self, state, config):
        self.state = state
        self.config = config
        self.workspace = self.state.workspace

        self.logging = logging.getLogger(__name__)
        self.source = self.config.get("source")
        self.disk = self.config.get("disk")

    def run(self):
        self.logging.info("Deploying ostree repository.")

        repo = self.source.get("repository")
        branch = self.source.get("branch")
        device = self.disk.get("device")
        kernel_args = self.source.get("kernel_args") or ""

        rootfs = self.workspace.joinpath("rootfs")
        if rootfs.exists():
            shutil.rmtree(rootfs)
        if not os.path.exists(device):
            self.logging.error("Unable to find {device}.")
            sys.exit(1)

        self.logging.info(f"Mounting {device} on {rootfs}")
        mount(device, rootfs)

        ostree_repo = rootfs.joinpath("ostree/repo")
        self.logging.info(f"Creating {ostree_repo}.")
        ostree_repo.mkdir(parents=True, exist_ok=True)
        utils.run_command(
            ["ostree", "init", "--repo", ostree_repo, "--mode", "bare"])
        self.logging.info(f"Pulling {branch}")
        utils.run_command(
            ["ostree", "pull-local", "--repo", ostree_repo, repo, branch])
        utils.run_command(
            ["ostree", "config", "--repo", ostree_repo, "--group", "sysroot",
             "set", "bootloader", "none"])

        self.logging.info(f"Configuring {device} for ostree.")
        utils.run_command(
            ["ostree", "admin", "init-fs", rootfs])
        utils.run_command(
            ["ostree", "admin", "os-init", "--sysroot", rootfs, "debian"])

        self.logging.info(f"Deploying {branch}")
        ostree_deploy = [
            "ostree", "admin", "deploy",
            "--sysroot", rootfs,
            "--os", "debian", branch]
        for arg in kernel_args:
            ostree_deploy.append(f"--karg={arg}")
        utils.run_command(ostree_deploy)

        self.logging.info("Setting up bootloader.")
        for d in rootfs.glob("ostree/deploy/debian/deploy/*.0"):
            repo_root = d
        utils.run_chroot(["bootctl", "install"], repo_root, efi=rootfs)
        shutil.copytree(rootfs.joinpath("boot/ostree"),
                        rootfs.joinpath("efi/ostree"))
        shutil.copy2(
            rootfs.joinpath("boot/loader/entries/ostree-1-debian.conf"),
            rootfs.joinpath("efi/loader/entries/ostree-0-1.conf"))

        umount(rootfs)
