#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Commandline API gateway for arbejdstimer."""
import pathlib
import sys
from typing import List, Union

import typer

import arbejdstimer
import arbejdstimer.arbejdstimer as at

APP_NAME = 'Working hours (Danish arbejdstimer) or not?'
APP_ALIAS = 'arbejdstimer'
app = typer.Typer(
    add_completion=False,
    context_settings={'help_option_names': ['-h', '--help']},
    no_args_is_help=True,
)

TEMPLATE_EXAMPLE = """\
{
  "api": 1,
  "application": "arbejdstimer",
  "operator": "or",
  "holidays": [
    {
      "label": "public holiday",
      "at": [
        "2021-12-08"
      ]
    },
    {
      "label": "company holidays 2021/2022",
      "at": [
        "2021-12-24",
        "2022-01-02"
      ]
    }
  ],
  "working_hours": [8, 17]
}
"""


@app.callback(invoke_without_command=True)
def callback(
    version: bool = typer.Option(
        False,
        '-V',
        '--version',
        help='Display the arbejdstimer version and exit',
        is_eager=True,
    )
) -> None:
    """
    Working hours (Danish arbejdstimer) or not?

    Given a configuration file detect if today is a work day and
    if at the time of request is a working hour.

    Return code of 0 indicates work time, 1 no work time, and 2 usage error.

    Additional help available per command adding the -h/--help option
    """
    if version:
        typer.echo(f'{APP_NAME} version {arbejdstimer.__version__}')
        raise typer.Exit()


@app.command('template')
def app_template() -> int:
    """
    Write a template of a JSON configuration to standard out and exit
    """
    sys.stdout.write(TEMPLATE_EXAMPLE)
    return sys.exit(0)


@app.command('now')
def now(
    conf: str = typer.Option(
        '',
        '-c',
        '--config',
        help='Path to config file (default is $HOME/.arbejdstimer.json)',
        metavar='<configpath>',
    ),
) -> int:
    """
    Silently answer the question if now is a working hour (per return code 0 for yes, and 1 for no).
    """
    command = 'now'
    config = conf if conf else pathlib.Path.home() / at.DEFAULT_CONFIG_NAME
    action = [command, str(config)]
    return sys.exit(at.main(action))


def explain_enforce_defaults(conf: str = '', verbose: bool = False) -> int:
    """Until the root cause of https://github.com/tiangolo/typer/issues/106 remains unfixed."""
    command = 'explain'
    if verbose:
        command += '_verbatim'
    config = conf if conf else pathlib.Path.home() / at.DEFAULT_CONFIG_NAME
    action = [command, str(config)]
    return sys.exit(at.main(action))


@app.command('explain')
def explain(
    conf: str = typer.Option(
        '',
        '-c',
        '--config',
        help='Path to config file (default is $HOME/.arbejdstimer.json)',
        metavar='<configpath>',
    ),
    verbose: bool = typer.Option(
        False,
        '-v',
        '--verbose',
        help='Be more verbatim providing the effective config values (default is false if not provided)',
        metavar='<bool>',
    ),
) -> int:
    """
    Explain the answer to the question if now is a working hour
    (in addition to the return code 0 for yes, and 1 for no).
    """
    return explain_enforce_defaults(conf, verbose)


@app.command('version')
def app_version() -> None:
    """
    Display the arbejdstimer version and exit
    """
    callback(True)


# pylint: disable=expression-not-assigned
# @app.command()
def main(argv: Union[List[str], None] = None) -> int:
    """Delegate processing to functional module."""
    argv = sys.argv[1:] if argv is None else argv
    return at.main(argv)
