"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""

import logging

from tiler import block
from tiler.modules.base import ModuleBase

LOG = logging.getLogger(__name__)


class Disk(ModuleBase):
    def __init__(self, state, config):
        self.state = state
        self.config = config

    def run(self):
        """Run the disk plugin."""
        pass