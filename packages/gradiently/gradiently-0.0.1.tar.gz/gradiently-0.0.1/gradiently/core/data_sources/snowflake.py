from gradiently.protos.gradiently.core.DataSource_pb2 import (
    DataSource as DataSourceProto,
)
from gradiently.core.data_sources.source import DataSource, SourceType


class SnowflakeSource(DataSource):
    database: str
    schema: str
    table: str
    source_type: SourceType

    def __init__(
        self,
        *,
        name: str,
        description: str,
        timestamp_col: str,
        table: str,
        database: str,
        schema: str,
    ):
        super().__init__(
            name=name,
            description=description,
            timestamp_col=timestamp_col,
            source_type=SourceType.SNOWFLAKE,
        )
        self._table = table
        self._database = database
        self._schema = schema
        self._source_type = SourceType.SNOWFLAKE

    @property
    def table(self):
        return self._table

    @property
    def database(self):
        return self._database

    @property
    def schema(self):
        return self._schema

    def to_proto(self):
        data_source = DataSourceProto()
        data_source.name = self.name
        data_source.description = self.description
        data_source.timestamp_col = self.timestamp_col
        data_source.source_type = self.source_type.value        

        data_source.snowflake_options.table = self.table
        data_source.snowflake_options.database = self.database
        data_source.snowflake_options.schema = self.schema        
        return data_source

    @classmethod
    def from_proto(cls, data_source_proto: DataSourceProto):
        return cls(
            name=data_source_proto.name,
            description=data_source_proto.description,
            timestamp_col=data_source_proto.timestamp_col,
            table=data_source_proto.snowflake_options.table,
            database=data_source_proto.snowflake_options.database,
            schema=data_source_proto.snowflake_options.schema,
        )
