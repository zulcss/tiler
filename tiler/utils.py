"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""
import subprocess
import logging

LOG = logging.getLogger(__name__)


def run_command(cmd, print_output=True, **kwargs):
    LOG.debug('Running %s' % cmd)

    outputs = ""
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               universal_newlines=True,
                               **kwargs)
    while True:
        output = process.stdout.readline()
        if output:
            if print_output:
                LOG.debug(output.rstrip("\n"))
            outputs += output
        if process.poll() is not None:
            break

    # Read the remaining logs from stdout after process terminates
    output = process.stdout.read()
    if output:
        LOG.debug(output.rstrip("\n"))
        outputs += output

    rc = process.poll()
    LOG.debug("rc %d" % rc)
    return rc, outputs


def run_chroot(args, image, **kwargs):
    """Run a command in a seperate namespace."""
    cmd = [
        "systemd-nspawn",
        "--quiet",
        "--as-pid2",
        "-i",
        image
    ]
    cmd += args

    return run_command(cmd, **kwargs)


def bwrap(args, rootfs, workspace=None, efi=False, **kwargs):
    """Run bubblewarap in a seperate namespace."""
    cmd = [
        "bwrap",
        "--bind", rootfs, "/",
        "--proc", "/proc",
        "--dev-bind", "/dev", "/dev",
        "--bind", "/sys", "/sys",
        "--dir", "/run",
        "--bind", "/tmp", "/tmp",
        "--share-net",
        "--die-with-parent",
        "--chdir", "/",
    ]

    if efi:
        cmd += [
            "--bind", f"{workspace}/efi", "/efi",
            "--bind", "/sys/firmware/efi/efivars", "/sys/firmware/efi/efivars",
        ]

    print(cmd)
    cmd += args

    return run_command(cmd, **kwargs)
