"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""

import logging

from tiler.modules.base import ModuleBase

LOG = logging.getLogger(__name__)


class Final(ModuleBase):
    def __init__(self, state, config):
        self.state = state
        self.config = config

    def run(self):
        pass
