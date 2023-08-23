#!/usr/bin/env python3

"""
This file contains the entry point of the application.
"""

import io
import os
import sys

import click

from fastimer import constants
from fastimer.commands import (
    command_cancel,
    command_info,
    command_show,
    command_start,
    command_stop,
)


def __get_path(path: str | None) -> str:
    """
    Determines the path to a working directory. It is supposed to be the "Fastimer" folder
    in user's home directory in case it's not specified via app's options.
    """

    if path is None:
        path = os.path.expanduser("~")
        path = os.path.join(path, "Fastimer")

    return path


def __path_help() -> str:
    return "Set path to working directory."


def __path_type() -> click.Path:
    return click.Path(exists=True)


@click.group(help="CLI tool that helps to fast.", invoke_without_command=True)
@click.pass_context
@click.option("-p", "--path", type=__path_type(), help=__path_help())
def cli(context: click.core.Context | None, path: str | None) -> None:
    """
    Main CLI entry point.
    """

    if isinstance(sys.stdout, io.TextIOWrapper) and sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding=constants.ENCODING)

    if context is None or not context.invoked_subcommand:
        __show(path)


@cli.command(help="Start a new fasting.")
@click.argument("length", type=click.INT, default=16)
@click.option("-p", "--path", type=__path_type(), help=__path_help())
def start(path: str | None, length: int) -> None:
    """
    Creates a new fast entry in the data file.
    """

    path = __get_path(path)
    command_start.main(path, length)


@cli.command(help="Show details of fasting.")
@click.argument("what", default="last", type=click.Choice(["last", "prev", "on"]))
@click.option("-p", "--path", type=__path_type(), help=__path_help())
def show(path: str | None, what: str) -> None:
    """
    Outputs detailed information about a fast.
    """

    __show(path, what)


@cli.command(help="Stop ongoing fasting.")
@click.option("-p", "--path", type=__path_type(), help=__path_help())
def stop(path: str | None) -> None:
    """
    Stops ongoing fast.
    """

    path = __get_path(path)
    command_stop.main(path)


@cli.command(help="Show accumulated statistics.")
@click.option("-p", "--path", type=__path_type(), help=__path_help())
def info(path: str | None) -> None:
    """
    Show accumulated fasting statistics.
    """

    path = __get_path(path)
    command_info.main(path)


@cli.command(help="Cancel ongoing fast.")
@click.option("-p", "--path", type=__path_type(), help=__path_help())
def cancel(path: str | None) -> None:
    """
    Cancels ongoing fast.
    """

    path = __get_path(path)
    command_cancel.main(path)


def __show(path: str | None, what: str | None = "last") -> None:
    """
    Executes SHOW command (outputs detailed information about a fast).
    """

    path = __get_path(path)
    command_show.main(path, what)


if __name__ == "__main__":
    cli(context=None, path=None)
