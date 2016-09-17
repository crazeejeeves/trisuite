import json
import logging
import logging.config
import os


def init_logging(config_file_path='log_config.json', config_env='LOG_CONFIG'):
    """Initialize logging system for the framework. Logging configuration is obtained
    (by default) from:

    a. LOG_CONFIG environment variable
    b. log_config.json file

    User may override both references, however environment variable ALWAYS takes priority
    """

    path_from_env = os.getenv(config_env, None)
    if path_from_env:
        config_file_path = path_from_env

    if os.path.exists(config_file_path):
        with open(config_file_path, 'rt') as file:
            config = json.load(file)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(handlers=[logging.NullHandler()])
