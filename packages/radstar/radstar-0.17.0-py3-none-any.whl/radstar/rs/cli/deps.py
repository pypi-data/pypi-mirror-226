# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC


import os
import subprocess

from .. import list_units, shsplit
from . import cli


@cli.command()
def update_deps():
    """Update and install Python dependencies."""

    in_files = []
    for x in list_units():
        x = os.path.join(x.dir, "requirements.in")
        if os.path.exists(x):
            in_files.append(x)

    subprocess.check_call(
        shsplit(
            "pip-compile --resolver=backtracking --allow-unsafe --generate-hashes --upgrade -o requirements.txt --no-header"
        )
        + in_files,
        cwd="/rs/project",
    )

    subprocess.check_call(
        shsplit("python -m pip install -r requirements.txt --require-virtualenv"),
        cwd="/rs/project",
    )
