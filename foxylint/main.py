import click
import os
import glob
import foxylint.imports


def red(text):
    return click.secho(text, fg='red', bold=True)


def bold(text):
    return click.secho(text, fg='white', bold=True)


@click.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('--exclude', '-e', multiple=True)
@click.option('--accept', multiple=True)
def main(files, exclude, accept):
    excluded = []
    for pattern in exclude:
        excluded.extend(glob.glob(pattern, recursive=True))

    excluded = [str(os.path.abspath(file)) for file in excluded]

    candidates = [file for file in files if file not in excluded]
    files = []
    for file in candidates:
        if os.path.abspath(file) not in excluded:
            files.append(file)

    accept = [pattern.strip('/') for pattern in accept]
    findings = foxylint.imports.analyze(files, acceptable_patterns=accept)
    bad_files = 0
    for file, analysis in findings.items():
        if analysis['ok']:
            continue
        bad_files += 1
        red(f'{file}:')
        for error in analysis['errors']:
            line, content = error['line_number'], error['line_content']
            bold(f'  {file}:{line}: {content}')

    if bad_files > 0:
        quit(1)
    else:
        quit(0)
