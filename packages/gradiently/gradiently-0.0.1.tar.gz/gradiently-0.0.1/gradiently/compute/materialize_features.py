import time
import os
import logging
from gradiently.protos.gradiently.core.FeatureBundle_pb2 import (
    FeatureBundles as FeatureBundlesProto,
)
from gradiently.core.feature_bundle import FeatureBundle
from gradiently.secrets.utils import get_secret_provider
from google.protobuf.json_format import Parse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from gradiently.compute.bundle_processing import construct_obs_df
from gradiently.compute.bundle_processing import (
    process_bundle_expr,
    compute_bundle_with_obs_df,
)
from typing import NamedTuple


class MaterializeFeaturesArguments(NamedTuple):
    namespace: str
    feature_bundles_json: str
    secrets_provider: str
    provider_region: str


logger = logging.getLogger(__name__)


def materialize_features(args: MaterializeFeaturesArguments):
    SparkSession.builder.appName("S3 with Spark").config(
        "spark.executor.memory", "2g"
    ).config("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID")).config(
        "spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY")
    ).config(
        "spark.hadoop.fs.s3a.aws.credentials.provider",
        "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
    ).getOrCreate()

    namespace = args.namespace
    feature_bundles_json = args.feature_bundles_json
    feature_bundles_proto = Parse(feature_bundles_json, FeatureBundlesProto())
    bundles = [
        FeatureBundle.from_proto(bundle) for bundle in feature_bundles_proto.bundles
    ]
    provider = get_secret_provider(args.secrets_provider, args.provider_region)
    config = provider.get_secrets_conf()

    start_time = time.time()

    for bundle in bundles:
        for entity in bundle.entity_keys:
            obs_df = construct_obs_df(entity.name, entity.dtype, bundle, config)
            bundle_df = process_bundle_expr(config, bundle)
            result_df = compute_bundle_with_obs_df(
                obs_df, "current_timestamp", bundle, bundle_df
            )

            result_df = result_df.withColumn(
                "timestamp", col("timestamp").cast("string")
            )
            result_df.write.format("org.apache.spark.sql.redis").option(
                "table", f"{namespace}:{entity.name}"
            ).option("key.column", entity.name).mode("overwrite").save()

    end_time = time.time()
    logger.info(f"Time taken: {end_time - start_time:.2f} seconds")
