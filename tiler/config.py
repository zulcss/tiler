"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""
import os

from omegaconf import OmegaConf
import yaml

from tiler import exceptions

class Config(object):
    """load the configuration file from the CLI."""

    def __init__(self, state):
        self.state = state

    def load_config(self):
        """Load the manifest.yaml"""
        try:
            with open(self.state.config, "r") as f:
                try:
                    return OmegaConf.create(yaml.safe_load(f))
                except yaml.YAMLError as error:
                    raise exceptions.ConfigError(
                        f"{self.state.config} failed validateion: {error}.")
        except OSError:
            raise exceptions.ConfigError(
                f"Configuration not found: {self.state.config}")
