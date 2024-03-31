"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""

import logging

from stevedore import driver

from tiler.modules.base import ModuleBase


class Unpack(ModuleBase):
    def __init__(self, state, config):
        self.state = state
        self.config = config

        self.logging = logging.getLogger(__name__)

    def run(self):
        if self.config.stages.unpack:
            for step in self.config.stages.unpack:
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
