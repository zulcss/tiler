"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

from tiler import utils


def mount(image, rootfs):
    ret,_,_ = utils.run_command(
        ["systemd-dissect", "-m", image, rootfs])
    return ret

def umount(rootfs):
    ret,_,_ = utils.run_command(
        ["systemd-dissect", "-u", rootfs])
    return ret
