import boto3
from gradiently.secrets.provider import SecretsProvider
from gradiently.core.configuration import GradientlyConfig, SnowflakeConfig, SecretsConfig
from dataclasses import fields, asdict, is_dataclass
from typing import Any, Dict, Union
import botocore.exceptions
import json


def is_valid_json(s: str):
    try:
        json.loads(s)
        return True
    except json.JSONDecodeError:
        return False


class AWSSecretsProvider(SecretsProvider):
    client: Any
    name: str
    region: str

    def __init__(self, region: str):
        # @TODO: Add region to secrets configuration and pass in dynamically
        self._client = boto3.client("secretsmanager", region_name=region)
        self._name = "aws"
        self._region = region

    @property
    def client(self) -> Any:
        return self._client

    @property
    def region(self) -> str:
        return self._region

    @property
    def name(self) -> str:
        return self._name

    def register_secrets(self, secrets_conf: SecretsConfig) -> None:
        """Register secrets from secrets configuration.

        Args:
            secrets_conf (GradientlyConfig): Secrets Configuration
        """
        for field in fields(secrets_conf):
            conf = getattr(secrets_conf, field.name)
            if is_dataclass(conf):
                json_ser = json.dumps(asdict(conf))
                try:
                    self.create_secret(key=field.name, value=json_ser)
                except botocore.exceptions.ClientError as error:
                    if error.response["Error"]["Code"] == "ResourceExistsException":
                        self._client.put_secret_value(
                            SecretId=field.name, SecretString=json_ser
                        )
                    else:
                        raise error

    def get_secrets_conf(self) -> SecretsConfig:
        """Gets the current secret configuration.

        Returns:
            GradientlyConfig: _description_
        """
        secrets_conf = SecretsConfig(provider=self.name)
        secret_key_to_cls = {"snowflake": SnowflakeConfig}

        for key, conf_cls in secret_key_to_cls.items():
            secret_dict = self.get_secret(key)
            setattr(secrets_conf, key, conf_cls(**secret_dict))
        return secrets_conf

    def get_secret(self, key: str) -> Union[Dict[str, Any], str]:
        """Gets a secret from the provider.

        Args:
            key (str): The key of the secret

        Returns:
            Union[Dict[str, Any], str]: The requested secret. Returns either a deserialized JSON or string literal.
        """
        response = self._client.get_secret_value(SecretId=key)
        secret_str = response.get("SecretString")

        if is_valid_json(secret_str):
            return json.loads(secret_str)

        return secret_str

    def create_secret(self, key: str, value: str) -> None:
        """Create a secret.

        Args:
            key (str): The key of the secret
            value (str): The value of the secret
        """
        self._client.create_secret(Name=key, SecretString=value)

    def delete_secret(self):
        pass
