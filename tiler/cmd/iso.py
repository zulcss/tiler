"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""
import click

from tiler.cmd.options import config_option
from tiler.cmd.options import url_option
from tiler.cmd import pass_state_context
from tiler.iso import ISO


@click.group(
    help="ISO Operations")
@pass_state_context
def iso(state):
    pass


@click.command(
    help="Fetch an ISO from a remote site.")
@pass_state_context
@url_option
def fetch(state, url):
    ISO(state).fetch()


@click.command(
    help="Build ISO.")
@pass_state_context
@config_option
def build(state, config):
    ISO(state).build()


iso.add_command(build)
iso.add_command(fetch)
