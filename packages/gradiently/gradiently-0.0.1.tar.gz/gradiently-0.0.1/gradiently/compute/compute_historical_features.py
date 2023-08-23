import os
from gradiently.protos.gradiently.core.FeatureBundle_pb2 import (
    FeatureBundles as FeatureBundlesProto,
)
from gradiently.protos.gradiently.core.ObservationQuery_pb2 import (
    ObservationQuery as ObservationQueryProto,
)
from gradiently.core.obs_query import ObservationQuery
from gradiently.compute.bundle_processing import compute_features_for_bundles
from gradiently.core.feature_bundle import FeatureBundle
from gradiently.secrets.utils import get_secret_provider
from google.protobuf.json_format import Parse
from pyspark.sql import SparkSession
from typing import NamedTuple
import logging

logger = logging.getLogger(__name__)


class ComputeHistoricalFeaturesArguments(NamedTuple):
    feature_bundles_json: str
    observation_query_json: str
    output_path: str
    secrets_provider: str
    provider_region: str


def compute_historical_features(args: ComputeHistoricalFeaturesArguments):
    feature_bundles_json = args.feature_bundles_json
    observation_query_json = args.observation_query_json
    output_path = args.output_path
    secrets_provider = args.secrets_provider
    provider_region = args.provider_region
    # If the current script is located in the child directory
    logger.info(
        f"Running materialization job with feature bundles: {feature_bundles_json}, observation query: {observation_query_json}, output_path: {output_path}, secrets_provider: {secrets_provider}"
    )
    for key, value in os.environ.items():
        logger.info(f"{key}: {value}")

    SparkSession.builder.appName("S3 with Spark").config(
        "spark.executor.memory", "2g"
    ).config("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID")).config(
        "spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY")
    ).config(
        "spark.hadoop.fs.s3a.aws.credentials.provider",
        "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
    ).getOrCreate()

    provider = get_secret_provider(secrets_provider, provider_region)
    config = provider.get_secrets_conf()

    feature_bundles_proto = Parse(feature_bundles_json, FeatureBundlesProto())
    bundles = [
        FeatureBundle.from_proto(bundle) for bundle in feature_bundles_proto.bundles
    ]

    obs_query_proto = Parse(observation_query_json, ObservationQueryProto())
    obs_query = ObservationQuery.from_proto(obs_query_proto)
    logger.info(f"Computing features for bundles...")
    df = compute_features_for_bundles(config, obs_query, bundles)
    logger.info(
        f"Finished computing features for bundles.. writing to path: {output_path}"
    )
    num_partitions = df.rdd.getNumPartitions()
    logger.info(f"Number of partitions: {num_partitions}")
    df.write.mode("overwrite").parquet(output_path)
