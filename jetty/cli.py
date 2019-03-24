import sys

import click

from poetry.console.commands import LockCommand


@click.group()
def cli():
    pass


@cli.command()
def lock():
    click.echo("Ran lock")


@cli.command()
def sync():
    click.echo("Ran sync")


def run():
    return cli()


if __name__ == '__main__':
    sys.exit(run())
