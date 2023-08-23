from typing import Optional
from gradiently.core.aggregation import Aggregation, DEFAULT_AGG
from gradiently.core.dtypes import DataType
from gradiently.protos.gradiently.core.Feature_pb2 import Feature as FeatureProto
from gradiently.core.hash_utils import md5_hash_str
from gradiently.core.aggregation import Aggregation


class Feature:
    """Represents a feature with its specifications."""

    name: str
    description: str
    expr: str
    dtype: DataType
    agg: Aggregation

    def __init__(
        self,
        *,
        name: str,
        description: str,
        expr: str,
        dtype: DataType,
        agg: Aggregation = DEFAULT_AGG,
    ):
        """Initializes a Feature instance.

        Args:
            name (str): The name of the feature.
            description (str): Description for the feature.
            expr (str): Expression associated with the feature.
            dtype (DataType): The data type of the feature.
            agg (Aggregation, optional): The aggregation type for the feature. Defaults to DEFAULT_AGG.
        """
        self._name = name
        self._description = description
        self._expr = expr
        self._dtype = dtype
        self._agg = agg

    @property
    def name(self) -> str:
        """str: The name of the feature."""
        return self._name

    @property
    def description(self) -> str:
        """str: A descriptive text explaining the purpose or usage of the feature."""
        return self._description

    @property
    def expr(self) -> str:
        """str: The expression representing the computation or extraction of this feature."""
        return self._expr

    @property
    def dtype(self) -> DataType:
        """DataType: Specifies the data type of the feature. For example, it can be integer, float, etc."""
        return self._dtype

    @property
    def agg(self) -> Aggregation:
        """Aggregation: The aggregation type used for the feature. It could be sum, average, etc."""
        return self._agg

    def __repr__(self):
        """Returns a string representation of the feature instance.

        Returns:
            str: String representation of the feature.
        """
        items = (f"{k} = {v}" for k, v in self.__dict__.items())
        return f"<{self.__class__.__name__}({', '.join(items)})>"

    def to_proto(self):
        """Convert the feature instance to a protobuf representation.

        Returns:
            FeatureProto: The protobuf representation of the feature.
        """
        feature = FeatureProto()
        feature.name = self.name
        feature.description = self.description
        feature.expr = self.expr
        feature.dtype = self.dtype.value
        feature.agg.CopyFrom(self.agg.to_proto())
        return feature

    @classmethod
    def from_proto(cls, feature_proto: FeatureProto):
        """Create a feature instance from a protobuf representation.

        Args:
            feature_proto (FeatureProto): The protobuf representation of the feature.

        Returns:
            Feature: A feature instance created from the given protobuf.
        """
        return cls(
            name=feature_proto.name,
            description=feature_proto.description,
            expr=feature_proto.expr,
            dtype=DataType(feature_proto.dtype),
            agg=Aggregation.from_proto(feature_proto.agg),
        )
