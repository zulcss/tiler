"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""

import logging
import sys

from tiler.modules.base import ModuleBase
from tiler.mount import mount
from tiler import utils


class OstreeInit(ModuleBase):
    def __init__(self, state, config, stage):
        self.state = state
        self.config = config
        self.stage = stage

        self.logging = logging.getLogger(__name__)
        self.device = self.config.params.disk
        self.repo = self.config.params.repository
        self.branch = self.config.params.branch
        self.rootfs = self.state.workspace.joinpath(
            f"{self.config.name}/rootfs")

    def run(self):
        self.logging.info("Unpacking source.")

        self.logging.info(f"Mounting {self.device} on {self.rootfs}.")
        ret = mount(self.device, self.rootfs)
        if ret != 0:
            self.logging.error(f"Mounted {self.device} on {self.rootfs} failed.")
            sys.exit(1)

        repo = self.rootfs.joinpath("ostree/repo")
        self.logging.info(f"Creating {repo}")
        if not repo.exists():
            repo.mkdir(parents=True, exist_ok=True)
        utils.run_command(
            ["ostree", "init", "--repo", repo, "--mode", "bare"])


class OstreePullLocal(ModuleBase):
    def __init__(self, state, config, stage):
        self.state = state
        self.config = config
        self.stage = stage

        self.logging = logging.getLogger(__name__)
        self.device = self.config.params.disk
        self.repo = self.config.params.repository
        self.branch = self.config.params.branch
        self.rootfs = self.state.workspace.joinpath(
            f"{self.config.name}/rootfs")

    def run(self):
        repo = self.rootfs.joinpath("ostree/repo")
        self.logging.info(f"Pulling {self.branch} from {self.repo}")
        utils.run_command(
            ["ostree", "pull-local", "--repo", repo, self.repo, self.branch])


class OstreePullRemote(ModuleBase):
    def __init__(self, state, config, stage):
        self.state = state
        self.config = config
        self.stage = stage

        self.logging = logging.getLogger(__name__)
        self.device = self.config.params.disk
        self.repo = self.config.params.repository
        self.branch = self.config.params.branch
        self.rootfs = self.state.workspace.joinpath(
            f"{self.config.name}/rootfs")

    def run(self):
        repo = self.rootfs.joinpath("ostree/repo")
        if self.repo.startswith("http"):
            self.logging.info(f"Pulling from {self.repo}")
            utils.run_command(
                ["ostree", "remote", "--repo={0}".format(repo), "add",
                 "--no-gpg-verify", "pablo-edge", self.repo])
            utils.run_command(
                ["ostree", "pull", "--repo={0}".format(repo), "pablo-edge",
                 self.branch])


class OstreeDeploy(ModuleBase):
    def __init__(self, state, config, stage):
        self.state = state
        self.config = config
        self.stage = stage

        self.logging = logging.getLogger(__name__)
        self.device = self.config.params.disk
        self.repo = self.config.params.repository
        self.branch = self.config.params.branch
        self.kernel_args = self.stage.kernel_args
        self.rootfs = self.state.workspace.joinpath(
            f"{self.config.name}/rootfs")

    def run(self):
        self.logging.info(f"Configuring {self.device} for ostree.")
        utils.run_command(
            ["ostree", "admin", "init-fs", self.rootfs])
        utils.run_command(
            ["ostree", "admin", "os-init", "--sysroot", self.rootfs, "debian"])

        self.logging.info(f"Deploying {self.branch}")
        ostree_deploy = [
            "ostree", "admin", "deploy",
            "--sysroot", self.rootfs,
            "--os", "debian", self.branch]
        for arg in self.kernel_args:
            ostree_deploy.append(f"--karg={arg}")
        utils.run_command(ostree_deploy)
