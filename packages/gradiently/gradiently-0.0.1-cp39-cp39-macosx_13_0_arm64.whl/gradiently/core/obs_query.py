from gradiently.protos.gradiently.core.ObservationQuery_pb2 import (
    ObservationQuery as ObservationQueryProto,
)
from gradiently.core.data_sources.source import DataSource
from gradiently.core.data_sources.registry import ENUM_TO_SOURCE_CLS


class ObservationQuery:
    query: str
    timestamp_col: str
    source: DataSource

    def __init__(self, *, query: str, timestamp_col: str, source: DataSource):
        self._query = query
        self._timestamp_col = timestamp_col
        self._source = source

    @property
    def query(self):
        return self._query

    @property
    def timestamp_col(self):
        return self._timestamp_col

    @property
    def source(self):
        return self._source

    def __repr__(self):
        items = (f"{k} = {v}" for k, v in self.__dict__.items())
        return f"<{self.__class__.__name__}({', '.join(items)})>"

    def to_proto(self):
        observation_query = ObservationQueryProto()
        observation_query.query = self.query
        observation_query.timestamp_col = self.timestamp_col
        observation_query.source.CopyFrom(self.source.to_proto())
        return observation_query

    @classmethod
    def from_proto(cls, observation_query_proto: ObservationQueryProto):
        data_source_constructor = ENUM_TO_SOURCE_CLS[
            observation_query_proto.source.source_type
        ]

        return cls(
            query=observation_query_proto.query,
            timestamp_col=observation_query_proto.timestamp_col,
            source=data_source_constructor.from_proto(observation_query_proto.source),
        )
