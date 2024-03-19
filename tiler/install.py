"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""

import logging

from tiler.config import Config
from tiler.config import exceptions
from tiler.image import ImagePart

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

        print(config)

        LOG.info("Create Disk Partition and Format Filesystem")
        self.image = ImagePart(self.state, config).run()

        LOG.info("Perforfind install")
