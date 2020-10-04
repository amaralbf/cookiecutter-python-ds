from loguru import logger

from . import config


def run():
    config.configure_logger()

    logger.info('Starting application "{{ cookiecutter.project_name }}".')

    logger.info('Finished application "{{ cookiecutter.project_name }}".')
