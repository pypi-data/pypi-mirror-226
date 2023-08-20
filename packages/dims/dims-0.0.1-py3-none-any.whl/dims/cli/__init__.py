# SPDX-FileCopyrightText: 2023-present Marcel Blijleven <marcelblijleven@gmail.com>
#
# SPDX-License-Identifier: MIT
import click

from dims.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="dims")
def dims():
    click.echo("Hello world!")
