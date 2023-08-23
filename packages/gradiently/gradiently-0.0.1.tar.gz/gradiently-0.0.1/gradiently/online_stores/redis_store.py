from featureflow.online_stores.base_store import BaseStore
from featureflow.core import OnlineStoreConfig, EntityKey
from typing import Any, Dict, List
from dataclasses import dataclass
import redis
import aioredis


class RedisStore(BaseStore):
    """
    A store implementation using Redis as the backend storage.

    Args:
        namespace (str): Namespace for the Redis store.
        conf (OnlineStoreConfig): Configuration details for the online store.
    """

    namespace: str
    client: aioredis.Redis
    config: OnlineStoreConfig

    def __init__(self, namespace: str, conf: OnlineStoreConfig):
        """Initializes the Redis store with the given namespace and configuration."""

        redis_url = f"redis://{conf.redis.host}:{conf.redis.port}/{conf.redis.db}"
        if conf.redis.password:
            redis_url = f"redis://:{conf.redis.password}@{conf.redis.host}:{conf.redis.port}/{conf.redis.db}"

        self._namespace = namespace
        self._async_client = aioredis.from_url(redis_url, decode_responses=True)
        self._sync_client = redis.Redis.from_url(redis_url, decode_responses=True)
        self._config = conf

    @property
    def sync_client(self) -> redis.Redis:
        """redis.Redis: Returns the synchronous Redis client."""
        return self._sync_client

    @property
    def async_client(self) -> aioredis.Redis:
        """aioredis.Redis: Returns the asynchronous Redis client."""
        return self._async_client

    @property
    def namespace(self) -> str:
        """str: Returns the namespace associated with the Redis store."""
        return self._namespace

    @property
    def config(self) -> OnlineStoreConfig:
        """OnlineStoreConfig: Returns the configuration details of the online store."""
        return self._config

    def get_online_features(
        self, entity_key: EntityKey, entity_ids: List[str], feature_names: List[str]
    ) -> Dict[str, Any]:
        """
        Fetches online features from the Redis store for given entities and feature names.

        Args:
            entity_key (EntityKey): The key to identify the entity.
            entity_ids (List[str]): List of entity IDs.
            feature_names (List[str]): List of feature names to fetch.

        Returns:
            Dict[str, Any]: A dictionary mapping entity IDs to their respective feature data.
        """
        redis_keys = [
            f"{self.namespace}:{entity_key.name}:{entity_id}"
            for entity_id in entity_ids
        ]

        with self.sync_client.pipeline(transaction=True) as pipe:
            for redis_key in redis_keys:
                pipe.hgetall(redis_key)

            fetched_data = pipe.execute()

        result = {}

        for idx, entity_id in enumerate(entity_ids):
            result[entity_id] = {}

            for feature in feature_names:
                result[entity_id][feature] = (
                    fetched_data[idx][feature] if feature in fetched_data[idx] else None
                )

        return result

    async def get_online_features_async(
        self, entity_key: EntityKey, entity_ids: List[str], feature_names: List[str]
    ) -> Dict[str, Any]:
        """
        Asynchronously fetches online features from the Redis store for given entities and feature names.

        Args:
            entity_key (EntityKey): The key to identify the entity.
            entity_ids (List[str]): List of entity IDs.
            feature_names (List[str]): List of feature names to fetch.

        Returns:
            Dict[str, Any]: A dictionary mapping entity IDs to their respective feature data.
        """
        redis_keys = [
            f"{self.namespace}:{entity_key.name}:{entity_id}"
            for entity_id in entity_ids
        ]

        async with self.async_client.pipeline(transaction=True) as pipe:
            for redis_key in redis_keys:
                pipe.hgetall(redis_key)

            fetched_data = await pipe.execute()

        result = {}

        for idx, entity_id in enumerate(entity_ids):
            result[entity_id] = {}

            for feature in feature_names:
                result[entity_id][feature] = (
                    fetched_data[idx][feature] if feature in fetched_data[idx] else None
                )

        return result
