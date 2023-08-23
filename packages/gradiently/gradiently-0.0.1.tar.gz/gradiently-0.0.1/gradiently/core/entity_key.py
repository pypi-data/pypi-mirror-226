from gradiently.core.dtypes import DataType
from gradiently.protos.gradiently.core.Entity_pb2 import EntityKey as EntityKeyProto


class EntityKey:
    """Represents a key entity with its name and data type."""

    name: str
    dtype: DataType

    def __init__(self, *, name: str, dtype: DataType):
        """Initializes an EntityKey instance.

        Args:
            name (str): The name of the entity key.
            dtype (DataType): The data type of the entity key.
        """
        self._name = name
        self._dtype = dtype

    @property
    def name(self):
        """str: Gets the name of the entity key."""
        return self._name

    @property
    def dtype(self):
        """DataType: Gets the data type of the entity key."""

        return self._dtype

    def __repr__(self):
        """Returns a string representation of the EntityKey.

        Returns:
            str: The string representation of the EntityKey.
        """
        items = (f"{k} = {v}" for k, v in self.__dict__.items())
        return f"<{self.__class__.__name__}({', '.join(items)})>"

    def to_proto(self) -> EntityKeyProto:
        """Converts the EntityKey instance to its corresponding protocol buffer representation.

        Returns:
            EntityKeyProto: The protobuf representation of the EntityKey.
        """
        entity_key = EntityKeyProto()
        entity_key.name = self.name
        entity_key.dtype = self.dtype.value
        return entity_key

    @classmethod
    def from_proto(cls, entity_key_proto: EntityKeyProto) -> "EntityKey":
        """Creates an EntityKey instance from its protocol buffer representation.

        Args:
            entity_key_proto (EntityKeyProto): The protobuf representation of an EntityKey.

        Returns:
            EntityKey: The EntityKey instance.
        """
        return cls(
            name=entity_key_proto.name,
            dtype=DataType(entity_key_proto.dtype),
        )
