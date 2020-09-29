from loguru import logger


def configure_logger():
    logger.add("{{cookiecutter.project_slug}}_{level}_{time}.log")
