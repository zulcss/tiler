"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import errno
import sys

import click

from tiler.cmd.options import config_option
from tiler.cmd import pass_state_context
from tiler.install import Installer


@click.command(
    help="Install Debian to disk.")
@pass_state_context
@config_option
def install(state, config):
    try:
        Installer(state).install()
    except KeyboardInterrupt:
        click.secho("\n" + ("Exiting at your request."))
        sys.exit(130)
    except BrokenPipeError:
        sys.exit()
    except OSError as error:
        if error.errno == errno.ENOSPC:
            sys.exit("error - No space left on device.")
