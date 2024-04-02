"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""
import logging
import shutil
import subprocess

LOG = logging.getLogger(__name__)


def run_command(args, data=None, **kwargs):
    LOG.debug('Running %s' % args)
    ret = False

    try:
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE
        stdin = subprocess.PIPE
        sp = subprocess.Popen(args, stdout=stdout,
                              stderr=stderr, stdin=stdin,
                              **kwargs)
        (out, err) = sp.communicate(data)
        ret = sp.poll()
    except OSError:
        try:
            out = out.decode("utf-8") if out else ""
            err = err.decode("utf-8") if err else ""
            raise Exception(
                f"Failed to run command {args}, out={out}, error={err}")
        except UnboundLocalError:
            raise Exception(args)

    out = out.decode("utf-8") if out else ""
    err = err.decode("utf-8") if err else ""

    if ret != 0:
        LOG.error(f"Failed to run command {args}, out={out}, error={err}")
        return (ret, out, err)

    if out:
        LOG.debug(f"out={out}")
    if err:
        LOG.debug(f"err={err}")

    return (ret, out, err)


def run_chroot_command(args, rootfs, efi=None, **kwargs):
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
    return run_command(cmd)


def which(cmd):
    return shutil.which(cmd)
