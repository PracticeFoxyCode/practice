import click
import glob
import foxyy.imports


def red(text):
    return click.secho(text, fg='red', bold=True)


def green(text):
    return click.secho(text, fg='green', bold=True)


def normal(text):
    return click.secho(text)


@click.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('--exclude', '-e', multiple=True)
def main(files, exclude):
    excluded = []
    for pattern in exclude:
        excluded.extend(glob.glob(pattern))

    files = [file for file in files if file not in excluded]
    findings = foxyy.imports.analyze(files)
    bad_files = 0
    for file, analysis in findings.items():
        if analysis['ok']:
            continue
        bad_files += 1
        red(f'{file} has non-foxyy imports:')
        for error in analysis['errors']:
            line, content = error['line_number'], error['line_content']
            normal(f'  {line}: {content}')

    if bad_files > 0:
        red(f'found {bad_files} out of {len(files)} files with non-foxyy imports.')
        quit(1)
    else:
        green(f'all {len(files)} files have foxyy imports.')
        quit(0)
