"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""

import logging
import os
import sys

from tiler.modules.base import ModuleBase
from tiler.mount import mount
from tiler import utils


class Unpack(ModuleBase):
    """Module that uses parted to create parttions."""

    def __init__(self, state, config, stage):
        self.state = state
        self.config = config
        self.stage = stage

        self.logging = logging.getLogger(__name__)
        self.device = self.config.params.disk
        self.source = self.config.params.source
        self.rootfs = self.state.workspace.joinpath(
            f"{self.config.name}/rootfs")

    def run(self):
        self.logging.info("Unpacking source.")

        if not os.path.exists(self.source):
            raise Exception(f"Couuld not find {self.source}.")

        if not self.rootfs.exists():
            self.rootfs.mkdir(parents=True, exist_ok=True)

        self.logging.info(f"Mounting {self.device} on {self.rootfs}.")
        ret = mount(self.device, self.rootfs)
        if ret != 0:
            self.logging.error(f"Mounted {self.device} on {self.rootfs} failed.")
            sys.exit(1)

        self.logging.info(f"Unpacking {self.source}.")
        utils.run_command(
            ["tar", "-C", self.rootfs,
             "--exclude=./dev/*",
             "-zxf", self.source, "--numeric-owner"])
