from typing import List, Optional
from gradiently.core.data_sources.source import DataSource
from gradiently.core.data_sources.registry import ENUM_TO_SOURCE_CLS
from gradiently.core.feature import Feature
from gradiently.core.entity_key import EntityKey
from gradiently.protos.gradiently.core.FeatureBundle_pb2 import (
    FeatureBundle as FeatureBundleProto,
)
import datetime
from gradiently.core.hash_utils import md5_hash_str


class FeatureBundle:
    def __init__(
        self,
        name: str,
        description: str,
        source: DataSource,
        features: List[Feature] = [],
        entity_keys: List[EntityKey] = [],        
    ):
        """Initializes a FeatureBundle.

        Args:
            name (str): The name of the feature bundle.
            description (str): A description of the bundle.
            source (DataSource): Data source for the bundle.
            features (List[Feature], optional): List of features in the bundle.
            entity_keys (List[EntityKey], optional): List of entity keys.            
        """
        self._name = name
        self._description = description
        self._source = source
        self._features = features
        self._entity_keys = entity_keys        

    def add_feature(self, feature: Feature) -> None:
        """Adds a feature to the bundle.

        Args:
            feature (Feature): The feature to be added.
        """
        self.features.append(feature)

    def add_features(self, features: List[Feature]) -> None:
        """Adds a list of features to the bundle

        Args:
            features (List[Feature]): The list of features to be added.
        """
        for feature in features:
            self.features.append(feature)

    @property
    def name(self) -> str:
        """str: The name of the feature bundle."""
        return self._name

    @property
    def description(self) -> str:
        """str: A descriptive text explaining the purpose or content of the bundle."""
        return self._description

    @property
    def source(self) -> DataSource:
        """DataSource: The source of the data for the feature bundle."""
        return self._source

    @property
    def features(self) -> List[Feature]:
        """List[Feature]: The features contained in the bundle."""
        return self._features

    @property
    def entity_keys(self) -> List[EntityKey]:
        """List[EntityKey]: The entity keys associated with the bundle."""
        return self._entity_keys

    def to_proto(self):
        """Converts the FeatureBundle instance to its corresponding protocol buffer representation.

        Returns:
            FeatureBundleProto: The protobuf representation of the FeatureBundle.
        """
        bundle_proto = FeatureBundleProto()
        bundle_proto.name = self.name
        bundle_proto.description = self.description
        bundle_proto.source.CopyFrom(self.source.to_proto())
        bundle_proto.features.extend([f.to_proto() for f in self.features])
        bundle_proto.entities.extend([entity.to_proto() for entity in self.entity_keys])        
        return bundle_proto

    @classmethod
    def from_proto(cls, bundle_proto: FeatureBundleProto):
        """Creates a FeatureBundle instance from its protocol buffer representation.

        Args:
            bundle_proto (FeatureBundleProto): The protobuf representation of a FeatureBundle.

        Returns:
            FeatureBundle: The FeatureBundle instance.
        """
        data_source_constructor = ENUM_TO_SOURCE_CLS[bundle_proto.source.source_type]

        return cls(
            name=bundle_proto.name,
            description=bundle_proto.description,
            source=data_source_constructor.from_proto(bundle_proto.source),
            features=[Feature.from_proto(feature) for feature in bundle_proto.features],
            entity_keys=[
                EntityKey.from_proto(entity) for entity in bundle_proto.entities
            ],            
        )

    def __repr__(self):
        """Returns a string representation of the FeatureBundle.

        Returns:
            str: The string representation of the FeatureBundle.
        """
        items = (f"{k} = {v}" for k, v in self.__dict__.items())
        return f"<{self.__class__.__name__}({', '.join(items)})>"