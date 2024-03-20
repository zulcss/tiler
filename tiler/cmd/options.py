"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import pathlib

import click

from tiler.cmd import State


def debug_option(f):
    def callback(ctxt, param, value):
        state = ctxt.ensure_object(State)
        state.debug = value
        return value
    return click.option(
        "--debug",
        is_flag=True,
        help="Increase verbosity",
        callback=callback
    )(f)


def workspace_option(f):
    def callback(ctxt, param, value):
        state = ctxt.ensure_object(State)
        state.workspace = pathlib.Path(value)
        return value
    return click.option(
        "--workspace",
        help="Path to the tiler workspace",
        nargs=1,
        default="/var/tmp/tiler",
        required=True,
        callback=callback
    )(f)


def config_option(f):
    """tiler configuration option"""
    def callback(ctxt, param, value):
        state = ctxt.ensure_object(State)
        state.config = pathlib.Path(value)
        return value
    return click.option(
        "--config",
        help="Path to the tiler autoinstall configuration.",
        nargs=1,
        required=True,
        callback=callback
    )(f)


""" ISO Options """


def url_option(f):
    def callback(ctxt, param, value):
        state = ctxt.ensure_object(State)
        state.url = value
        return value
    return click.option(
        "--url",
        help="URL to fetch ISO from.",
        nargs=1,
        callback=callback
    )(f)
