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


def add_poetry_to_pyproject():
    deps = ['click', 'loguru']
    dev_deps = ['black==20.8b1', 'flake8', 'ipykernel', 'isort']

    if not is_negative('{{ cookiecutter.use_pre_commit }}'):
        dev_deps.append('pre-commit')

    deps_list = list(chain(*zip(['--dependency'] * len(deps), deps)))
    devdeps_list = list(chain(*zip(['--dev-dependency'] * len(dev_deps), dev_deps)))

    subprocess.call(['poetry', 'init', '-q', '-n'] + deps_list + devdeps_list)

    add_script_section()


def add_script_section():
    script_section = (
        '\n[tool.poetry.scripts]'
        '\n{{ cookiecutter.project_slug }} = "{{ cookiecutter.package_name }}.main:run"'
        '\n'
    )

    with open('pyproject.toml', 'at') as f:
        f.write(script_section)


if __name__ == "__main__":
    validate_option('{{ cookiecutter.use_pre_commit }}')

    add_poetry_to_pyproject()

    if is_negative('{{ cookiecutter.use_pre_commit }}'):
        remove_file('.pre-commit-config.yaml')
