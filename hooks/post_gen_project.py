import os
import subprocess
from itertools import chain

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def generate_pyproject_toml():
    DEPS = ['click', 'loguru']
    DEV_DEPS = ['black==20.8b1', 'flake8', 'isort', 'pre-commit']

    deps_list = list(chain(*zip(['--dependency'] * len(DEPS), DEPS)))
    devdeps_list = list(chain(*zip(['--dev-dependency'] * len(DEV_DEPS), DEV_DEPS)))

    subprocess.call(['poetry', 'init', '-q', '-n'] + deps_list + devdeps_list)


def extend_pyproject_toml():
    with open('pyproject_complement.toml', 'rt') as f:
        other_tools_sections = f.read()

    with open('pyproject.toml', 'at') as f:
        f.write('\n' + other_tools_sections)

    remove_file('pyproject_complement.toml')


generate_pyproject_toml()
extend_pyproject_toml()
