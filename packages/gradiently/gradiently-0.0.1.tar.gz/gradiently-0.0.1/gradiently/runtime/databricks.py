from gradiently.runtime.runtime import Runtime
from gradiently.core.feature_bundle import FeatureBundle
from typing import List
from gradiently.protos.gradiently.core.FeatureBundle_pb2 import (
    FeatureBundles as FeatureBundlesProto,
)
from gradiently.core.obs_query import ObservationQuery
from gradiently.core.utils import json_serialize_inputs
from databricks.sdk.service.compute import Library, ClusterSpec
from databricks.sdk.service.jobs import Task, PythonWheelTask
from databricks.sdk import WorkspaceClient
from boto3 import Session

ENTRY = "submit-job"
PKG_NAME = "gradiently"

DEFAULT_LIB = Library(
    whl="dbfs:/FileStore/jars/942059e2_6ffe_492e_b759_d7bdaa118cd3/gradiently-0.1.0-py3-none-any.whl"
)

session = Session()
creds = session.get_credentials()

DEFAULT_CLUSTER_SPEC = ClusterSpec(
    node_type_id="i3.xlarge",
    num_workers=2,
    spark_version="12.2.x-scala2.12",
    spark_env_vars={
        "PYSPARK_PYTHON": "/databricks/python3/bin/python3",
        "AWS_ACCESS_KEY_ID": creds.access_key,
        "AWS_SECRET_ACCESS_KEY": creds.secret_key,
    },
)


class DatabricksRuntime(Runtime):
    def __init__(self):
        self._databricks_client = WorkspaceClient()

    @property
    def databricks_client(self):
        return self._databricks_client

    def _gen_task(
        job_name: str,
        namespace: str,
        observation_query: ObservationQuery,
        feature_bundles: List[FeatureBundle],
        secrets_provider: str,
        output_path: str,
        provider_region: str,
    ) -> Task:
        bundles_json, query_json = json_serialize_inputs(
            feature_bundles=feature_bundles, observation_query=observation_query
        )
        return Task(
            task_key="gradiently_feature_job",
            python_wheel_task=PythonWheelTask(
                entry_point=ENTRY,
                # named_parameters={
                #     "compute_historical_features": None,
                #     "namespace": namespace,
                #     "feature_bundles_json": bundles_json,
                #     "observation_query_json": query_json,
                #     "secrets_provider": secrets_provider,
                #     "output_path": output_path,
                #     "provider_region": provider_region,
                # },
                parameters=[
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
                ],
                package_name=PKG_NAME,
            ),
            libraries=[DEFAULT_LIB],
            new_cluster=DEFAULT_CLUSTER_SPEC,
        )

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
        f_bundles_proto = FeatureBundlesProto()
        f_bundles_proto.bundles.extend(
            [bundle.to_proto() for bundle in feature_bundles]
        )
        resp = self.databricks_client.jobs.submit(
            run_name=job_name,
            tasks=[
                self._gen_task(
                    namespace=namespace,
                    observation_query=observation_query,
                    feature_bundles=feature_bundles,
                    secrets_provider=secrets_provider,
                    output_path=output_path,
                    provider_region=provider_region,
                )
            ],
        )
        print(resp)

    def job_status(self):
        pass

    def materialize(self):
        pass
