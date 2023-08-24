# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC


import os

import click

from .. import shsplit


@click.group()
def cli():
    """Radstar Utility."""


def shexec(cmd_: str, **kw):
    """parse and execute command."""
    args = shsplit(cmd_, **kw)
    os.execvp(args[0], args)
