"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""

import logging

from tiler.config import Config
from tiler.config import exceptions
from tiler.disk import ImagePart
from tiler.ostree import OstreeDeploy
from tiler.vm import VanillaInstall

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

        LOG.info("Create Disk Partition and Format Filesystem")
        self.image = ImagePart(self.state, config).run()

        source = config.get("source")
        if source.get("repository") and source.get("branch"):
            LOG.info("Deploy Ostree to Disk device")
            OstreeDeploy(self.state, config).run()
        elif source.get("origin") or source.get("file"):
            VanillaInstall(self.state, config).run()

        LOG.info("Perforfind install")
