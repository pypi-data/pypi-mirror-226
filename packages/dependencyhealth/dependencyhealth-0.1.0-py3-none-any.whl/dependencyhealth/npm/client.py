import logging
from dependencyhealth import AbstractClient


class Client(AbstractClient):
    def __init__(self, key: str = None, token: str = None, log_level=logging.WARNING):
        super().__init__(key=key, token=token, log_level=log_level)
        self._system = "npm"
