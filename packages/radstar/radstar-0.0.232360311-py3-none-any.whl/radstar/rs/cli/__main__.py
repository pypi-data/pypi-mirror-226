# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC


import os

from .. import init as rs_init


def main():
    from . import cli, configure, db, deps, python, run, setup  # pylint: disable=unused-import

    if os.path.isdir("/rs/project"):
        os.chdir("/rs/project")

    rs_init(["cli"])
    cli(prog_name="rs")


if __name__ == "__main__":
    main()
