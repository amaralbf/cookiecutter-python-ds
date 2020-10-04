import os
import subprocess
from itertools import chain
from pathlib import Path

PROJECT_DIRECTORY = Path(os.path.realpath(os.path.curdir))

AFFIRMATIVE_OPTIONS = ['y', 'yes']
NEGATIVE_OPTIONS = ['n', 'no']
BOOL_OPTIONS = AFFIRMATIVE_OPTIONS + NEGATIVE_OPTIONS


def is_negative(option):
    return option in NEGATIVE_OPTIONS


def validate_option(option):
    if option not in BOOL_OPTIONS:
        raise ValueError(
            'ERROR: "use_pre_commit" option value must be one of the following: '
            + str(BOOL_OPTIONS)
        )


def remove_file(filepath):
    os.remove(PROJECT_DIRECTORY / filepath)


def generate_pyproject_toml():
    deps = ['click', 'loguru']
    dev_deps = ['black==20.8b1', 'flake8', 'isort']

    if not is_negative('{{ cookiecutter.use_pre_commit }}'):
        dev_deps.append('pre-commit')

    deps_list = list(chain(*zip(['--dependency'] * len(deps), deps)))
    devdeps_list = list(chain(*zip(['--dev-dependency'] * len(dev_deps), dev_deps)))

    subprocess.call(['poetry', 'init', '-q', '-n'] + deps_list + devdeps_list)

    extend_pyproject_toml()


def extend_pyproject_toml():
    with open('pyproject_complement.toml', 'rt') as f:
        other_tools_sections = f.read()

    with open('pyproject.toml', 'at') as f:
        f.write('\n' + other_tools_sections)

    remove_file('pyproject_complement.toml')


if __name__ == "__main__":
    validate_option('{{ cookiecutter.use_pre_commit }}')

    generate_pyproject_toml()

    if is_negative('{{ cookiecutter.use_pre_commit }}'):
        remove_file('.pre-commit-config.yaml')
