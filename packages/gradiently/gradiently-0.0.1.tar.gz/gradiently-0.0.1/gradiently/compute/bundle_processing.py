from gradiently.core.aggregation import AggregationType
from gradiently.core.obs_query import ObservationQuery
from gradiently.core.configuration import GradientlyConfig
from gradiently.core.feature_bundle import FeatureBundle
from gradiently.compute.df_loaders import load_df_from_source, get_obs_df
from typing import List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
import logging
from gradiently.core.dtypes import DataType
from pyspark.sql.functions import col


logger = logging.getLogger(__name__)


def construct_obs_df(
    entity_name: str, dtype: DataType, bundle: FeatureBundle, config: GradientlyConfig
):
    df = load_df_from_source(config, bundle.source)
    df.createOrReplaceTempView("my_table")
    distinct_df = df.select(entity_name).distinct()
    df_with_timestamp = distinct_df.withColumn(
        "current_timestamp", F.current_timestamp()
    )
    return df_with_timestamp


def process_bundle_expr(config: GradientlyConfig, bundle: FeatureBundle) -> DataFrame:
    spark = SparkSession.builder.getOrCreate()
    df = load_df_from_source(config, bundle.source)
    df.createOrReplaceTempView("my_table")

    join_keys = [entity.name for entity in bundle.entity_keys]

    query = f"SELECT {bundle.source.timestamp_col}, {', '.join(join_keys)}, "
    for feature in bundle.features:
        query += f"{feature.expr}"

        if feature.expr.startswith("CASE"):
            query += f" END AS {feature.name}, "
        else:
            query += f" AS {feature.name}, "

    query = query.rstrip(", ")
    query += " FROM my_table"
    result = spark.sql(query)
    return result


def compute_bundle_with_obs_df(
    obs_df: DataFrame, timestamp_col: str, bundle: FeatureBundle, bundle_df: DataFrame
):
    from pyspark.sql import functions as F
    from pyspark.sql.functions import monotonically_increasing_id

    bundle_timestamp_col = bundle.source.timestamp_col
    bundle_df = bundle_df.withColumnRenamed(bundle_timestamp_col, "event_timestamp")

    obs_df = obs_df.withColumnRenamed(timestamp_col, "timestamp")
    obs_df = obs_df.withColumn("temp_id", monotonically_increasing_id())

    df1 = obs_df

    df1 = df1.withColumn("timestamp", col("timestamp").cast("timestamp"))
    df2 = bundle_df.withColumn(
        "event_timestamp", col("event_timestamp").cast("timestamp")
    )

    num_partitions = 200  # choose this based on the size of your cluster
    df1 = df1.repartition(num_partitions, F.hash("id"))
    df2 = df2.repartition(num_partitions, F.hash("id"))

    df1 = df1.withColumn("timestamp", F.col("timestamp").cast("long"))
    df2 = df2.withColumn("event_timestamp", F.col("event_timestamp").cast("long"))

    for feature in bundle.features:
        logger.info(
            f"Computing feature with window size: {feature.agg.window.total_seconds()}"
        )
        df_result = computed_feature_df(
            df1,
            df2,
            feature.name,
            feature.agg.window.total_seconds(),
            feature.agg.method.name,
        )
        obs_df = obs_df.join(df_result, "temp_id")
        logger.info(f"Finished joining feature: {feature.name}")

    return obs_df


def computed_feature_df(
    df1: DataFrame,
    df2: DataFrame,
    feature_name: str,
    window_size_secs: int,
    agg_type: str,
) -> DataFrame:
    from pyspark.sql import functions as F

    AGG_TO_FUNC = {
        AggregationType.SUM.name: F.sum,
        AggregationType.AVG.name: F.avg,
        AggregationType.MAX.name: F.max,
        AggregationType.MIN.name: F.min,
    }

    agg_func = AGG_TO_FUNC.get(agg_type)
    df_joined = df1.join(
        df2,
        (df1["id"] == df2["id"])
        & (df2.event_timestamp <= df1.timestamp)
        & (df2.event_timestamp >= df1.timestamp - window_size_secs),
        "left_outer",
    )

    df_result = df_joined.groupBy("temp_id").agg(
        agg_func(df2[feature_name]).alias(feature_name)
    )

    return df_result


def compute_features_for_bundles(
    config: GradientlyConfig,
    observation_query: ObservationQuery,
    bundles: List[FeatureBundle],
):
    obs_df = get_obs_df(config, observation_query)

    for bundle in bundles:
        bundle_df = process_bundle_expr(config, bundle)
        df = compute_bundle_with_obs_df(
            obs_df=obs_df,
            timestamp_col=observation_query.timestamp_col,
            bundle=bundle,
            bundle_df=bundle_df,
        )
    return df
