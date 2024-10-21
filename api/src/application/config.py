import logging
from config import settings, AppConfig


def setup_app_config(path: str, debug: bool) -> None:
    settings.app_config = AppConfig.from_config_file(path)

    if debug:
        settings.DEBUG = debug
    if settings.DEBUG:
        logging.root.setLevel(logging.DEBUG)
