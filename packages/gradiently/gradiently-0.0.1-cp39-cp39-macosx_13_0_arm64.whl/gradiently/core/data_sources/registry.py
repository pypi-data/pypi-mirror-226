from featureflow.core.data_sources.snowflake import SnowflakeSource
from featureflow.core.data_sources.file import FileSource
from featureflow.core.data_sources.source import SourceType


ENUM_TO_SOURCE_CLS = {
    SourceType.SNOWFLAKE.value: SnowflakeSource,
    SourceType.FILE.value: FileSource,
}
