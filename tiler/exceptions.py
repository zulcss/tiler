"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""


class TilerError(Exception):
    """Base class for microtlat exceptions."""

    def __init__(self, message=None):
        super(TilerError, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message or ""


class ConfigError(TilerError):
    """Tiler cofiguration error."""
    pass
