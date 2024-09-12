import click
import foxyy.imports


def red(text):
    return click.secho(text, fg='red', bold=True)


def normal(text):
    return click.secho(text)


@click.command()
@click.argument('files', nargs=-1, type=click.Path())
def main(files):
    findings = foxyy.imports.enforce(files)
    for file, analysis in findings.items():
        if analysis['ok']:
            continue
        red(f'{file} has non-foxyy imports:')
        for error in analysis['errors']:
            normal(f'  {error}')
