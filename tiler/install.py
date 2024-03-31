"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""

import logging

from stevedore import driver

from tiler.config import Config
from tiler.config import exceptions

LOG = logging.getLogger(__name__)


class Installer(object):
    def __init__(self, state):
        self.state = state
        self.config = Config(self.state)
        self.image = None

    def install(self):
        LOG.info("Installing Debian Linux.")

        LOG.info("Loading configuration file.")
        if self.state.config.exists():
            exceptions.ConfigError(
                f"Failed to load configuration: {self.state.config}")
        config = self.config.load_config()

        if config.stages:
            for stage in config.stages:
                LOG.info(f"Running {stage} stage.")

                try:
                    mgr = driver.DriverManager(
                        namespace="tiler.modules.stages",
                        name=stage,
                        invoke_on_load=True,
                        invoke_args=(self.state, config)
                    )
                    mgr.driver.run()
                except RuntimeError as e:
                    raise Exception(
                        f"Uable to load plugin: {stage}: {e}"
                    )