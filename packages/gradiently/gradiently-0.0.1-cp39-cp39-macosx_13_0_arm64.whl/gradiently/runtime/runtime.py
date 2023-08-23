from abc import ABC, abstractmethod
from typing import List
from featureflow.core.obs_query import ObservationQuery
from featureflow.core.feature_bundle import FeatureBundle


class Runtime(ABC):
    @abstractmethod
    def compute_historical_features(
        self,
        job_name: str,
        observation_query: ObservationQuery,
        feature_bundles: List[FeatureBundle],
    ):
        raise NotImplementedError

    @abstractmethod
    def job_status(self):
        raise NotImplementedError

    @abstractmethod
    def materialize(
        self, bundles: List[FeatureBundle], secrets_provider: str, provider_region: str
    ):
        raise NotImplementedError
