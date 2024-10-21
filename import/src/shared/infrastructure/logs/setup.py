import logging.config


def setup_logs_from_config_file(config_file_path: str) -> None:
    logging.config.fileConfig(config_file_path, disable_existing_loggers=False)
    logging.getLogger(__name__).debug(f'Loaded setup from config file: {config_file_path}')
