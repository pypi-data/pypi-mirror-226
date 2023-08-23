from enum import Enum
from featureflow.core.hash_utils import md5_hash_str


class SourceType(Enum):
    INVALID = 0
    FILE = 1
    SNOWFLAKE = 2
    BIGQUERY = 3
    REDSHIFT = 4


class DataSource:
    name: str
    description: str
    timestamp_col: str
    source_type: SourceType

    def __init__(
        self,
        *,
        name: str,
        description: str,
        timestamp_col: str,
        source_type: SourceType,
    ):
        self._name = name
        self._description = description
        self._timestamp_col = timestamp_col
        self._source_type = source_type

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def timestamp_col(self):
        return self._timestamp_col

    @property
    def source_type(self):
        return self._source_type

    def __repr__(self):
        items = (f"{k} = {v}" for k, v in self.__dict__.items())
        return f"<{self.__class__.__name__}({', '.join(items)})>"
