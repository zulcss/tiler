"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""
import logging
import subprocess

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


def run_chroot(args, rootfs, efi=None, print_output=False, **kwargs):
    """Run bubblewarap in a seperate namespace."""
    cmd = [
        "bwrap",
        "--bind", rootfs, "/",
        "--ro-bind", "/etc/resolv.conf", "/etc/resolv.conf",
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
        cmd += ["--bind", f"{efi}/efi", "/efi",
                "--bind", f"{efi}/efi", "/boot/efi"]

    cmd += args
    return run_command(cmd, print_output=print_output, **kwargs)


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
