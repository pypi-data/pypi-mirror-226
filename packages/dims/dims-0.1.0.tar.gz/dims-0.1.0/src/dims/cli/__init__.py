# SPDX-FileCopyrightText: 2023-present Marcel Blijleven <marcelblijleven@gmail.com>
#
# SPDX-License-Identifier: MIT
import click

from dims.__about__ import __version__
from dims.utils import compare_paths


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="dims")
@click.argument("src", type=click.Path(exists=True))
@click.argument("target", type=click.Path(exists=True))
@click.option(
    "-f",
    "--filenames-only",
    type=bool,
    default=False,
    is_flag=True,
    help="Ignores file paths and only looks at unique file names.",
)
def dims(src, target, filenames_only):
    result = compare_paths(src, target, exact_paths=not filenames_only)

    if not result:
        click.echo("Didn't miss something")
        return

    click.echo(result)
