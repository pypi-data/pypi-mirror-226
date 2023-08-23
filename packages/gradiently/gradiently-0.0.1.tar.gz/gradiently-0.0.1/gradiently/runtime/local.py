from typing import List
from featureflow.runtime.runtime import Runtime
from featureflow.core.obs_query import ObservationQuery
from featureflow.core.feature_bundle import FeatureBundle
from featureflow.core.utils import json_serialize_inputs, json_serialize_bundles
import featureflow.compute.compute_historical_features
from featureflow.runtime.constants import SPARK_PKGS
import featureflow.compute.entry
import logging
import subprocess

ENTRY_PATH = featureflow.compute.entry.__file__


logger = logging.getLogger(__name__)


class LocalRuntime:
    def compute_historical_features(
        self,
        job_name: str,
        namespace: str,
        observation_query: ObservationQuery,
        feature_bundles: List[FeatureBundle],
        output_path: str,
        secrets_provider: str,
        provider_region: str,
    ):
        bundles_json, query_json = json_serialize_inputs(
            feature_bundles=feature_bundles, observation_query=observation_query
        )
        command = [
            "spark-submit",
            "--packages",
            ",".join(SPARK_PKGS),
            ENTRY_PATH,
            "compute_historical_features",
            "--namespace",
            namespace,
            "--feature_bundles_json",
            bundles_json,
            "--observation_query_json",
            query_json,
            "--output_path",
            output_path,
            "--secrets_provider",
            secrets_provider,
            "--provider_region",
            provider_region,
        ]

        self.submit_and_listen(command=command)

    def materialize(
        self,
        namespace: str,
        feature_bundles: List[FeatureBundle],
        secrets_provider: str,
        provider_region: str,
    ):
        bundles_json = json_serialize_bundles(feature_bundles)

        command = [
            "spark-submit",
            "--packages",
            ",".join(SPARK_PKGS),
            ENTRY_PATH,
            "materialize",
            "--namespace",
            namespace,
            "--feature_bundles_json",
            bundles_json,
            "--secrets_provider",
            secrets_provider,
            "--provider_region",
            provider_region,
        ]

        self.submit_and_listen(command=command)

    def submit_and_listen(self, command: List[str]):
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )

        # Read and print the output in real-time
        for line in process.stdout:
            print(line.strip())

        # Wait for the process to complete
        process.wait()

        # Check the exit code
        if process.returncode != 0:
            logger.info(
                f"Error: The command exited with a non-zero status code: {process.returncode}"
            )
