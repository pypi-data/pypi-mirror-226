from typing import List
import logging
from gradiently.core.data_sources.source import DataSource
from gradiently.core.data_sources.registry import ENUM_TO_SOURCE_CLS
from gradiently.core import FeatureBundle, Feature
from gradiently.secrets.provider import SecretsProvider
from gradiently.secrets.aws_provider import AWSSecretsProvider
from gradiently.runtime import Runtime, LocalRuntime, DatabricksRuntime
import textwrap
from gradiently.core.obs_query import ObservationQuery
from gradiently.core.configuration import GradientlyConfig
from gradiently.core.configuration import load_config_from_path
from gradiently.protos.gradiently.services.Registry_pb2_grpc import RegistryStub
from gradiently.protos.gradiently.services.Registry_pb2 import (
    BundleRequest,
    GetBundleRequest,
    GetActiveBundlesRequest,
    GetDataSourceRequest,
)
import grpc

logger = logging.getLogger(__name__)


class Client:
    """gradiently Client SDK."""

    runtime: Runtime
    config: GradientlyConfig
    secrets_provider: SecretsProvider

    def __init__(
        self,
        conf_path: str,
        runtime: Runtime = LocalRuntime,
        secrets_provider: SecretsProvider = AWSSecretsProvider,
        registry_uri: str = "localhost:50051",
    ):
        """Initializes a Client instance.

        Args:
            conf_path (str): Path to the configuration file.
            runtime (Runtime, optional): The runtime environment. Defaults to LocalRuntime.
            secrets_provider (SecretsProvider, optional): Secrets provider. Defaults to AWSSecretsProvider.
            registry_uri (str, optional): URI for the registry. Defaults to "localhost:50051".
        """
        self._config = load_config_from_path(conf_path)
        self._runtime = runtime()
        self._secrets_provider = secrets_provider(
            region=self.config.secrets.provider.region
        )
        self._stub = RegistryStub(grpc.insecure_channel(registry_uri))

    @property
    def config(self):
        return self._config

    @property
    def runtime(self):
        return self._runtime

    @property
    def stub(self):
        return self._stub

    @property
    def secrets_provider(self):
        return self._secrets_provider

    def register_secrets(self):
        self.secrets_provider.register_secrets(self.config)

    def compute_historical_features(
        self,
        job_name: str,
        observation_query: ObservationQuery,
        feature_bundles: List[FeatureBundle],
        output_path: str,
    ) -> str:
        """Computes historical features for the given observation query and feature bundles.

        Args:
            job_name (str): Name of the job.
            observation_query (ObservationQuery): Query for fetching observations.
            feature_bundles (List[FeatureBundle]): List of feature bundles.
            output_path (str): Path where the output should be stored.

        Returns:
            str: The output path.
        """
        self.runtime.compute_historical_features(
            job_name=job_name,
            namespace=self.config.namespace,
            observation_query=observation_query,
            feature_bundles=feature_bundles,
            output_path=output_path,
            secrets_provider=self.secrets_provider.name,
            provider_region=self.secrets_provider.region,
        )
        return output_path

    def get_bundle(self, name: str) -> FeatureBundle:
        """Fetches a specific feature bundle by its name.

        Args:
            name (str): Name of the feature bundle.            

        Returns:
            FeatureBundle: The fetched feature bundle.
        """
        request = GetBundleRequest(
            namespace=self.config.namespace, name=name
        )
        response = self.stub.GetBundle(request)
        return FeatureBundle.from_proto(response.bundle)

    def get_active_features_names(self) -> List[str]:
        """Fetches the names of all active features from the active bundles.

        Returns:
            List[str]: A list containing the names of active features.
        """
        active_bundles = self.get_active_bundles()
        return [
            feature.name for bundle in active_bundles for feature in bundle.features
        ]

    def get_active_bundles(self) -> List[FeatureBundle]:
        """Fetches all the active feature bundles.

        Returns:
            List[FeatureBundle]: A list of active feature bundles.

        Raises:
            grpc.RpcError: If there's an error with the RPC communication.
        """
        try:
            request = GetActiveBundlesRequest(namespace=self.config.namespace)
            response = self.stub.GetActiveBundles(request)
            return [FeatureBundle.from_proto(bundle) for bundle in response.bundles]

        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INTERNAL:
                logger.exception(
                    "An internal error occurred on the server: ", e.details()
                )
            else:
                logger.exception("An unexpected error occurred: ", e.details())

    def get_data_source(self, source_name: str) -> DataSource:
        """Retrieves a specific data source based on its name.

        Args:
            source_name (str): The name of the desired data source.

        Returns:
            DataSource: The fetched data source object.
        """
        request = GetDataSourceRequest(
            namespace=self.config.namespace, name=source_name
        )
        response = self.stub.GetDataSource(request)
        data_source_constructor = ENUM_TO_SOURCE_CLS[response.source.source_type]
        return data_source_constructor.from_proto(response.source)

    def register_bundles(self, bundles: List[FeatureBundle]):
        """Registers multiple feature bundles.

        Args:
            bundles (List[FeatureBundle]): A list of feature bundles to register.
        """
        for bundle in bundles:
            self.register_bundle(bundle)

    def register_bundle(self, bundle: FeatureBundle) -> str:
        """Registers a single feature bundle.

        Args:
            bundle (FeatureBundle): The feature bundle to register.

        Returns:
            str: The name of the bundle

        Raises:
            grpc.RpcError: If there's an error with the RPC communication.
        """
        try:
            request = BundleRequest(
                namespace=self.config.namespace, bundle=bundle.to_proto()
            )
            response = self.stub.RegisterBundle(request)
            log_msg = textwrap.dedent(
                f"""
                    Namespace: {request.namespace},
                    Bundle: {response.bundle.name},                    
                    Features: {len(response.bundle.features)}
                    Successfully registered bundle.
                """
            )
            logger.info(log_msg)
            return response.bundle.name
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INTERNAL:
                logger.exception(
                    "An internal error occurred on the server: ", e.details()
                )
            else:
                logger.exception("An unexpected error occurred: ", e.details())

    def activate_bundle(self, bundle: FeatureBundle):
        """Activates a given feature bundle.

        Args:
            bundle (FeatureBundle): The feature bundle to activate.
        """
        request = BundleRequest(
            namespace=self.config.namespace, bundle=bundle.to_proto()
        )
        response = self.stub.ActivateBundle(request)

    def deactivate_bundle(self, bundle: FeatureBundle):
        """Deactivates a given feature bundle.

        Args:
            bundle (FeatureBundle): The feature bundle to deactivate.
        """
        request = BundleRequest(
            namespace=self.config.namespace, bundle=bundle.to_proto()
        )
        response = self.stub.DeactivateBundle(request)

    def materialize_bundles(self, bundles: List[FeatureBundle]):
        """Materializes the given list of feature bundles.

        Args:
            bundles (List[FeatureBundle]): The feature bundles to materialize.
        """
        self.runtime.materialize(
            namespace=self.config.namespace,
            feature_bundles=bundles,
            secrets_provider=self.secrets_provider.name,
            provider_region=self.secrets_provider.region,
        )
