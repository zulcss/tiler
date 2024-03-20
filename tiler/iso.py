"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""
import logging
import os

import requests

LOG = logging.getLogger(__name__)


class ISO(object):
    def __init__(self, state):
        self.state = state
        self.workspace = self.state.workspace

    def fetch(self):
        LOG.info(f"Downloading from {self.state.url}")

        if not self.workspace.exists():
            self.workspace.mkdir(parents=True, exist_ok=True)

        filename = self.state.url.split("/",)[-1].replace(" ", "_")
        path = self.workspace.joinpath(filename)
        r = requests.get(self.state.url, stream=True)
        if r.ok:
            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
            LOG.info(f"Succesfully downloaded {filename}.")
        else:
            raise Exception(f"Failed to download {self.stae.url}")

    def build(self):
        LOG.info("Running iso builder.")
