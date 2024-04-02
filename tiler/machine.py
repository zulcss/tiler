"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0
"""
import os
import stat
from platform import machine

import logging

LOG = logging.getLogger(__name__)

arch2machine = {
  "amd64":"x86_64",
  "arm64":"aarch64",
}

def valid_arch(arch):
    """Check to see if arch is a valid or not."""
    if not arch2machine.get(arch):
        LOG.error("Unkown arch %s" % arch)
        return False

    if arch2machine.get(arch) != machine():
        LOG.error("Arch %s(%s) is not supported on %s", arch, arch2machine.get(arch), machine())
        return False

    return True
