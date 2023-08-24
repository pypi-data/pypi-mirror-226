# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC


from rsrpc import json

from . import db, plugins, settings, unit
from .plugins import plugin
from .unit import get_unit, list_units
from .utils import attrs, getenv, import_dir, panic, readfile, shsplit


def init(modules: list[str] | None = None) -> unit.Unit:
    """load units and import modules. can be called multiple times."""

    if (main := get_unit("main")) is None:
        unit.init_unit("rs.core")
        main = unit.init_unit("main")

    if modules is not None:
        for u in list_units():
            for m in modules:
                u.import_module(m)

    return main
