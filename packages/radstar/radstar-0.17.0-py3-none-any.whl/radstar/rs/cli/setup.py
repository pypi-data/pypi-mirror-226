# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC


from .. import list_units
from . import cli


@cli.command(hidden=True)
def setup_apps():
    for app in list_units():
        if (mod := app.import_module("setup")) is not None:
            mod.setup()
