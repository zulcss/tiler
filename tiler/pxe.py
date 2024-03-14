"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""
import logging

from tiler.config import Config

LOG = logging.getLogger(__name__)


class PXE(object):
    def __init__(self, state):
        self.state = state
        self.config = Config(self.state)

    def build(self):
        LOG.info("Running pxe builder.")
