"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""

import logging

from tiler.config import Config
from tiler.config import exceptions

LOG = logging.getLogger(__name__)


class Installer(object):
    def __init__(self, state):
        self.state = state
        self.config = Config(self.state)

    def install(self):
        LOG.info("Installing Debian Linux.")

        LOG.info("Loading configuration file.")
        if self.state.config.exists():
            exceptions.ConfigError(
                f"Failed to load configuration: {self.state.config}")
        config = self.config.load_config()

        LOG.info("Perforfind install")
        print(config)
