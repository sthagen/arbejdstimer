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
    """
    if version:
        typer.echo(f'{APP_NAME} version {arbejdstimer.__version__}')
        raise typer.Exit()


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
    Answer the question if now is a working hour.
    """
    command = 'now'
    config = conf if conf else pathlib.Path.home() / at.DEFAULT_CONFIG_NAME
    action = [command, str(config)]
    return sys.exit(at.main(action))


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
