from enum import Enum
from gradiently.core.data_sources.source import DataSource, SourceType
from gradiently.protos.gradiently.core.DataSource_pb2 import (
    DataSource as DataSourceProto,
)


class FileType(Enum):
    """Enumeration for supported file types."""

    CSV = 0
    PARQUET = 1


class FileSource(DataSource):
    uri: str
    file_type: FileType

    def __init__(
        self,
        *,
        name: str,
        description: str,
        timestamp_col: str,
        uri: str,
        file_type: FileType,
    ):
        """Initializes a new instance of FileSource."""
        super().__init__(
            name=name,
            description=description,
            timestamp_col=timestamp_col,
            source_type=SourceType.FILE,
        )
        self._uri = uri
        self._file_type = file_type

    @property
    def uri(self) -> str:
        """str: Gets the URI of the file."""
        return self._uri

    @property
    def file_type(self) -> FileType:
        """FileType: Gets the type of the file."""
        return self._file_type

    def to_proto(self):
        """
        Converts the instance to its Protocol Buffer representation.

        Returns:
            DataSourceProto: Protocol Buffer representation of the instance.
        """
        data_source = DataSourceProto()
        data_source.name = self.name
        data_source.description = self.description
        data_source.timestamp_col = self.timestamp_col
        data_source.source_type = self.source_type.value

        data_source.file_options.uri = self.uri
        data_source.file_options.file_type = self.file_type.value
        return data_source

    @classmethod
    def from_proto(cls, data_source_proto: DataSourceProto) -> "FileSource":
        """
        Creates a new instance of FileSource from its Protocol Buffer representation.

        Args:
            data_source_proto (DataSourceProto): Protocol Buffer representation of a FileSource.

        Returns:
            FileSource: A new instance of FileSource.
        """
        return cls(
            name=data_source_proto.name,
            description=data_source_proto.description,
            timestamp_col=data_source_proto.timestamp_col,
            uri=data_source_proto.file_options.uri,
            file_type=FileType(data_source_proto.file_options.file_type),
        )
