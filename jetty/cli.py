import click


@click.group()
def cli():
    pass


@cli.command()
def lock():
    click.echo("Ran lock")


@cli.command()
def sync():
    click.echo("Ran sync")


if __name__ == '__main__':
    cli()
