import inspect
from pathlib import Path

import {{ cookiecutter.package_name }}
from loguru import logger

PROJECT_DIR = Path(inspect.getfile({{ cookiecutter.package_name }})).resolve().parents[2]

{% raw %}
def configure_logger():
    logger.add(f"{PROJECT_DIR}/logs/{{time}}_debug_my_ds_project.log", level='DEBUG')
    logger.add(f"{PROJECT_DIR}/logs/{{time}}_info_my_ds_project.log", level='INFO'){% endraw %}
