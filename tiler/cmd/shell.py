"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""
import logging

import click

from tiler.cmd.install import install
from tiler.cmd.iso import iso
from tiler.cmd.options import debug_option
from tiler.cmd.options import workspace_option
from tiler.cmd import pass_state_context
from tiler.cmd.pxe import pxe
from tiler.log import setup_log

LOG = logging.getLogger(__name__)


@click.group(
    help="Debian installer."
)
@pass_state_context
@debug_option
@workspace_option
def cli(state, debug, workspace):
    setup_log(debug)

    state.workspace.mkdir(parents=True, exist_ok=True)
    LOG.info("Loading tiler.")


def main():
    cli(prog_name="tiler")


# tiler sub-commands
cli.add_command(install)
cli.add_command(iso)
cli.add_command(pxe)
