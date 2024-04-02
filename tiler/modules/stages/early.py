"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""

import logging

from stevedore import driver

from tiler.block import is_block
from tiler.machine import valid_arch

from tiler.modules.base import ModuleBase


class Early(ModuleBase):
    def __init__(self, state, config):
        self.state = state
        self.config = config

        self.logging = logging.getLogger(__name__)

    def run(self):
        self.logging.info("Running early stage")
        if not self.config.params.disk:
            raise Exception(f"{self.config.params.disk} is not specified.")

        self.logging.info("Checking for block device.")
        if not is_block(self.config.params.disk):
            raise Exception(
                f"{self.config.params.disk} is not a block device.")

        self.logging.info("Checking for architecture.")
        if not valid_arch(self.config.architecture):
            raise Exception(
                f"Invalid architecture: {self.config.architecture}.")

        if self.config.stages.early:
            for step in self.config.stages.early:
                self.logging.info(step.name)
                self.logging.info(f"Running {step.module}.")

                try:
                    mgr = driver.DriverManager(
                        namespace="tiler.modules",
                        name=step.module,
                        invoke_on_load=True,
                        invoke_args=(self.state, self.config, step.options)
                    )
                    mgr.driver.run()
                except RuntimeError as e:
                    raise Exception(
                        f"Uable to load module: {step.module}: {e}"
                    )
