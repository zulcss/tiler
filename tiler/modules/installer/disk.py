"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""

import logging

from tiler.modules.base import ModuleBase
from tiler import utils


class Parted(ModuleBase):
    """Module that uses parted to create parttions."""

    def __init__(self, state, config, stage):
        self.state = state
        self.config = config
        self.stage = stage

        self.logging = logging.getLogger(__name__)
        self.device = self.config.params.disk
        self.partitions = self.stage.partitions

    def run(self):
        self.logging.info("Running parted.")

        self.logging.info("Creating gpt disk label.")
        utils.run_command(
            ["parted", self.device, "--script", "mklabel", "gpt"])

        self.logging.info("Creating parttiions.")
        for index, part in enumerate(self.partitions, start=1):
            self.logging.info(f"Creating partition {index}: {part.name}")
            utils.run_command(
                ["parted", "-a", "optimal", "-s", self.device, "--", "mkpart",
                 part.name, part.start, part.end])
            if len(part.flags) != 0:
                for flag in part.flags:
                    utils.run_command(
                        ["parted", "-a", "optimal", "-s", self.device, "--",
                         "set", str(index), flag, "on"])
