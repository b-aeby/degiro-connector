# IMPORTATION STANDARD
import abc
import logging
import requests
from typing import Any, Dict, final

# IMPORTATION THIRD PARTY

# IMPORTATION INTERNAL
from degiro_connector.core.models.model_connection import ModelConnection
from degiro_connector.core.models.model_session import ModelSession


class AbstractAction(abc.ABC):
    @final
    @staticmethod
    def build_logger() -> logging.Logger:
        return logging.getLogger(__name__)

    @final
    @staticmethod
    def build_session(headers: Dict[str, str] = None) -> requests.Session:
        return ModelSession.build_session()

    @final
    @property
    def credentials(self):
        return self._credentials

    @final
    @property
    def connection_storage(self):
        return self._connection_storage

    @final
    @property
    def logger(self):
        return self._logger

    @final
    @property
    def session_storage(self):
        return self._session_storage

    @final
    def __init__(
        self,
        credentials,
        connection_storage: ModelConnection,
        logger: logging.Logger = None,
        session_storage: ModelSession = None,
    ):
        self._credentials = credentials
        self._connection_storage = connection_storage
        self._logger = logger or logging.getLogger(self.__module__)
        self._session_storage = session_storage or ModelSession(
            hooks=self._connection_storage.build_hooks(),
            ssl_check=False,
        )

        self.post_init()

    @final
    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)

    def post_init(self):
        pass

    @abc.abstractmethod
    def call(self):
        pass