import click
import sys
import os
import glob
import foxylint.imports


def red(text):
    return click.secho(text, fg='red', bold=True)


def green(text):
    return click.secho(text, fg='green', bold=True)


def normal(text):
    return click.secho(text)


@click.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('--exclude', '-e', multiple=True)
@click.option('--accept', multiple=True)
def main(files, exclude, accept):
    excluded = []
    for pattern in exclude:
        excluded.extend(glob.glob(pattern))

    excluded = [str(os.path.abspath(file)) for file in excluded]

    candidates = [file for file in files if file not in excluded]
    files = []
    for file in candidates:
        if os.path.abspath(file) not in excluded:
            files.append(file)

    findings = foxylint.imports.analyze(files, acceptable_patterns=accept)
    bad_files = 0
    for file, analysis in findings.items():
        if analysis['ok']:
            continue
        bad_files += 1
        red(f'{file}:')
        for error in analysis['errors']:
            line, content = error['line_number'], error['line_content']
            normal(f'  {file}:{line}: {content}')

    print(f'XXXXXXXXXXXXXX {bad_files=}')

    command_line = ' '.join(sys.argv)
    if bad_files > 0:
        red(f'{os.getpid()} {command_line=}  found {bad_files} out of {len(files)} files with non-foxy imports.')
        quit(10 + bad_files)
    else:
        green(f'{os.getpid()}  {command_line=} ALL {len(files)} files have foxy imports.')
        quit(0)
