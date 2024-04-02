"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""

import logging
import os

from stevedore import driver

from tiler.modules.base import ModuleBase
from tiler.mount import umount


class Post(ModuleBase):
    def __init__(self, state, config):
        self.state = state
        self.config = config

        self.logging = logging.getLogger(__name__)
        self.rootfs = self.state.workspace.joinpath(
            f"{self.config.name}/rootfs")

    def run(self):
        if self.config.stages.post:
            for step in self.config.stages.post:
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
        if os.path.ismount(self.rootfs):
            self.logging.info("Cleaning up")
            ret = umount(self.rootfs)
            if ret != 0:
                self.logging.error(f"Umounted {self.rootfs} failed.")
                sys.exit(1)
