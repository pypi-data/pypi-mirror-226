# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC


from itertools import chain
import os
import shutil

import jinja2
import rs
import yaml

from . import cli

DEBIAN_CODENAMES = {
    "11": "bullseye",
    "12": "bookworm",
    "13": "trixie",
    "14": "forky",
}


@cli.command()
def configure():
    """Reconfigure project."""

    with open("project.yml") as f:
        project_data = yaml.safe_load(f)

    # jinja environment
    env = jinja2.Environment(undefined=jinja2.StrictUndefined)

    # versions
    project_data["v"] = project_data["versions"]
    project_data["v"]["codename"] = DEBIAN_CODENAMES[project_data["v"]["debian"]]

    # apt packages
    for x in ["", "build_", "dev_"]:
        project_data[f"apt_{x}pkgs"] = [
            render(env, p, **project_data) for p in chain_attrs(f"apt.{x}packages")
        ]

    # apt repos
    for x in ["repos", "build_repos", "dev_repos"]:
        repos = chain_attrs(f"apt.{x}")
        for r in repos:
            r["entry"] = render(env, r["entry"], **project_data)
        project_data[f"apt_{x}"] = repos

    # docker
    for x in ["build", "build_setup", "dev_setup", "setup"]:
        project_data[f"docker_{x}"] = "\n\n".join(
            render(env, cmds, **project_data)
            for unit in rs.list_units()
            if (cmds := unit.get_attr(f"docker.{x}"))
        )

    # process template files from all units
    for unit in rs.list_units():
        if os.path.exists(template_dir := os.path.join(unit.dir, "templates")):
            copy_with_templates(env, template_dir, "/rs/project", project_data)


def chain_attrs(key: str) -> list:
    return list(chain.from_iterable(x for unit in rs.list_units() if (x := unit.get_attr(key))))


def copy_with_templates(env: jinja2.Environment, src: str, dst: str, project_data: dict):
    def joinrepl(*paths) -> str:
        return os.path.join(*paths).replace("/dot-", "/.")

    for src_root, dirs, files in os.walk(src):
        dst_root = os.path.join(dst, src_root[len(src) + 1 :])

        for x in dirs:
            if x[0] == ".":
                continue
            if not os.path.isdir(dst_dir := joinrepl(dst_root, x)):
                os.mkdir(dst_dir)

        for x in files:
            if x[0] == ".":
                continue
            src_file = os.path.join(src_root, x)
            dst_file = joinrepl(dst_root, x)

            if x.endswith(".j2"):
                with open(src_file) as f:
                    data = env.from_string(f.read()).render(**project_data)
                with open(dst_file[:-3], "w") as f:
                    print(data, file=f)
            else:
                shutil.copy(src_file, dst_file)


def render(env_: jinja2.Environment, src_: str, **kw):
    return env_.from_string(src_).render(**kw)
