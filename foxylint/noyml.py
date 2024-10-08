import click
import pathlib
import re
import os
import subprocess
import glob


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
    accept_patterns = [re.compile(pattern) for pattern in accept]
    ok = True
    for file in files:
        if any([pattern.search(file) for pattern in accept_patterns]):
            continue

        path = pathlib.Path(file)
        if path.suffix == '.yml':
            ok = False
            new_path = path.with_suffix('.yaml')
            red(f'renaming {path} to {new_path}')
            subprocess.run(['git', 'mv', str(path), str(new_path)])

    if not ok:
        bold('had to fix some files')
        quit(1)
