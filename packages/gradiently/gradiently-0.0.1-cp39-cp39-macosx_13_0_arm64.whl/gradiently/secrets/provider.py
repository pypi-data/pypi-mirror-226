from typing import Any, Dict, Union
from gradiently.core.configuration import GradientlyConfig
from abc import ABC, abstractmethod


class SecretsProvider(ABC):
    @abstractmethod
    def register_secrets(secrets_conf: GradientlyConfig) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_secret(key: str, val: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_secret(key: str) -> Union[Dict[str, Any], str]:
        raise NotImplementedError

    @abstractmethod
    def delete_secret(key: str) -> None:
        raise NotImplementedError
