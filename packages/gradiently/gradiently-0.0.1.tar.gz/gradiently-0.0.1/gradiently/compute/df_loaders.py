from gradiently.core.configuration import GradientlyConfig
from pyspark.sql import SparkSession
from gradiently.core.data_sources.file import FileType
from gradiently.core.data_sources.source import SourceType, DataSource
from gradiently.core.obs_query import ObservationQuery
from pyspark.sql import DataFrame


def get_obs_df(config: GradientlyConfig, obs_query: ObservationQuery) -> DataFrame:
    return load_df_from_source(config, obs_query.source)


def load_df_from_file(path: str, file_type: FileType) -> DataFrame:
    spark = SparkSession.builder.getOrCreate()
    if file_type == FileType.CSV:
        return spark.read.csv(path, header=True, inferSchema=True)
    elif file_type == FileType.PARQUET:
        return spark.read.parquet(path)


def load_df_from_snowflake(
    config: GradientlyConfig, table: str, schema: str, database: str
):
    # Create Spark session

    spark = SparkSession.builder.getOrCreate()
    df = (
        spark.read.format("snowflake")
        .option("sfURL", config.snowflake.url)
        .option("sfUser", config.snowflake.user)
        .option("sfPassword", config.snowflake.password)
        .option("sfDatabase", database)
        .option("sfSchema", schema)
        .option("sfWarehouse", config.snowflake.warehouse)
        .option("dbtable", table)
        .load()
    )
    return df


def load_df_from_source(config: GradientlyConfig, source: DataSource) -> DataFrame:
    """Load a dataframe given a data source

    Args:
        source (DataSource): _description_

    Returns:
        DataFrame: _description_
    """
    if source.source_type == SourceType.FILE:
        return load_df_from_file(source.uri, source.file_type)
    elif source.source_type == SourceType.SNOWFLAKE:
        return load_df_from_snowflake(
            config, source.table, source.schema, source.database
        )
