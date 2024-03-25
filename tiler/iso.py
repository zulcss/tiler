"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""
from datetime import datetime
import logging
import os
import shutil
import subprocess

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
        """Build an live ISO from the specified configuration in tiler."""
        LOG.info("Running iso builder.")
        timestamp = datetime.timestamp(datetime.now())

        shutil.copytree(self.state.config, self.workspace, dirs_exist_ok=True)

        if os.path.exists(self.workspace.joinpath("config")):
            shutil.rmtree(self.workspace.joinpath("config"))

        shutil.copytree(
            self.workspace.joinpath("pablo-config"),
            self.workspace.joinpath("config"))

        LOG.info("Cleaning workspace.")
        subprocess.run(["lb", "clean", "--all"], cwd=self.workspace)

        LOG.info("Configuring ISO.")
        subprocess.run(["lb", "build"], cwd=self.workspace)

        tmp_iso = self.workspace.joinpath("live-image-amd64.hybrid.iso")
        final_iso = self.workspace.joinpath(f"pablo-iso-{timestamp}.iso")
        os.rename(tmp_iso, final_iso)
        LOG.info(f"Your ISO can be found at: {final_iso}")
