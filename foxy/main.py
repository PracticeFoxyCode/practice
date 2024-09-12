import click


@click.command()
@click.argument('files', nargs=-1, type=click.Path())
def main(files):
    click.echo(files)
