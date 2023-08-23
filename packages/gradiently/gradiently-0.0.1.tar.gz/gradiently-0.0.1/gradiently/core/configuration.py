from dataclasses import dataclass, is_dataclass
from typing import Optional


@dataclass
class SnowflakeConfig:
    """
    Configuration details for connecting to Snowflake.
    """

    url: str
    user: str
    password: str
    warehouse: str


@dataclass
class RedisConfig:
    """
    Configuration details for connecting to Redis.
    """

    host: str
    port: int
    db: str
    password: str = ""


@dataclass
class RedshiftConfig:
    """
    Configuration details for connecting to Redshift.
    """

    host: str
    port: int
    database: str
    user: str
    password: str
    cluster_id: str


@dataclass
class BigQueryConfig:
    """
    Configuration details for connecting to Google BigQuery.
    """

    project_id: str
    dataset_id: str
    table_id: str
    credentials: str


@dataclass
class ProviderConfig:
    """
    Configuration details for a service provider.
    """

    name: str
    region: str


@dataclass
class SecretsConfig:
    """
    Configuration details for secret data used across various data warehouses.
    """

    provider: ProviderConfig
    snowflake: Optional[SnowflakeConfig] = None
    redshift: Optional[RedshiftConfig] = None
    bigquery: Optional[BigQueryConfig] = None
    # you can continue to add more fields here for other data warehouses


@dataclass
class OnlineStoreConfig:
    """
    Configuration details for the online store.
    """

    redis: RedisConfig


@dataclass
class GradientlyConfig:
    """
    Configuration details for the gradiently system.
    """

    namespace: str
    runtime: str
    online_store: OnlineStoreConfig
    secrets: SecretsConfig


import yaml
import os
from typing import Any, Dict
from dataclasses import asdict


from dataclasses import fields


def load_config_from_path(path: str) -> GradientlyConfig:
    """Loads configuration given a path

    Args:
        path (str): Path to the config file.

    Raises:
        Exception: If there's an error during deserialization.

    Returns:
        GradientlyConfig: gradiently Configuration
    """
    with open(path) as f:
        conf = yaml.safe_load(os.path.expandvars(f.read()))
        namespace = conf.get("namespace")
        if not namespace:
            raise Exception("Namespace must be specified.")

        # Helper function to deserialize nested configs
        def deserialize(dataclass_type: Any, config: Dict[str, Any]) -> Any:
            dataclass_fields = {
                field.name: field.type for field in fields(dataclass_type)
            }
            dataclass_instance_data = {}
            for k, v in dataclass_fields.items():
                if k in config:
                    if is_dataclass(v):
                        dataclass_instance_data[k] = deserialize(v, config[k])
                    else:
                        dataclass_instance_data[k] = config[k]
            return dataclass_type(**dataclass_instance_data)

        # Start deserialization from the top-level dataclass
        try:
            gradiently_config = deserialize(GradientlyConfig, conf)
            return gradiently_config

        except Exception as e:
            raise Exception(f"Error deserializing the config: {str(e)}")
