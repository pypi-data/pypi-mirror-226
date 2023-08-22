import logging
from typing import List

from detecta_shared.loggers.log_handler_factories.log_handler_factory import LogHandlerFactory


class LogInitializer:
    def __init__(self, logger_name: str, log_level: int, log_handler_factories: List[LogHandlerFactory]):
        self.log_handler_factories = log_handler_factories
        self.log_level = log_level
        self.logger_name = logger_name

    def init_logger(self):
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.log_level)
        for handler_factory in self.log_handler_factories:
            logger.addHandler(handler_factory.create_handler())