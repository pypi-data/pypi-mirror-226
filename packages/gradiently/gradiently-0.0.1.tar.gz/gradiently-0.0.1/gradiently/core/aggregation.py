from enum import Enum
from datetime import timedelta
from typing import Optional
from gradiently.protos.gradiently.core.Aggregation_pb2 import Aggregation as AggregationProto

class AggregationType(Enum):
    """
    Enum class to define different aggregation types.
    """

    LATEST = 0
    SUM = 1
    AVG = 2
    MIN = 3
    MAX = 4


class Aggregation:
    """
    Represents an aggregation method and its associated time window.

    Attributes:
        _method (AggregationType): The aggregation method to use.
        _window (timedelta): The time window for which the aggregation is computed.
    """

    _method: AggregationType
    _window: timedelta

    def __init__(self, method: AggregationType, window: timedelta = timedelta(days=1)):
        self._method = method
        self._window = window

    @property
    def method(self) -> AggregationType:
        """
        Returns the aggregation method.

        Returns:
            AggregationType: The aggregation method.
        """
        return self._method

    @property
    def window(self) -> timedelta:
        """
        Returns the time window for aggregation.

        Returns:
            timedelta: The time window for aggregation.
        """
        return self._window

    def __repr__(self) -> str:
        items = (f"{k} = {v}" for k, v in self.__dict__.items())
        return f"<{self.__class__.__name__}({', '.join(items)})>"

    def to_proto(self) -> "AggregationProto":
        """
        Converts the Aggregation object to its protocol buffer representation.

        Returns:
            AggregationProto: The protocol buffer representation.
        """
        aggregation = AggregationProto()
        aggregation.method = self.method.value
        aggregation.window = int(self.window.total_seconds())
        return aggregation

    @classmethod
    def from_proto(cls, aggregation_proto: "AggregationProto") -> "Aggregation":
        """
        Constructs an Aggregation object from its protocol buffer representation.

        Args:
            aggregation_proto (AggregationProto): The protocol buffer representation.

        Returns:
            Aggregation: The constructed Aggregation object.
        """
        return cls(
            method=AggregationType(aggregation_proto.method),
            window=timedelta(seconds=aggregation_proto.window),
        )


DEFAULT_AGG = Aggregation(method=AggregationType.LATEST)
