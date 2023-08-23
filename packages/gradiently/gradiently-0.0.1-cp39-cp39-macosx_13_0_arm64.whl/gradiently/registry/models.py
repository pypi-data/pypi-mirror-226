from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    String,
    ForeignKey,
    Enum,
    DateTime,
    BigInteger,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import JSON


Base = declarative_base()


class NamespaceModel(Base):
    __tablename__ = "namespace"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), nullable=False, unique=True)
    data_sources = relationship("DataSourceModel", backref="namespace")


class DataSourceModel(Base):
    __tablename__ = "data_source"
    id = Column(Integer, primary_key=True)
    namespace_id = Column(Integer, ForeignKey("namespace.id"), nullable=False)
    name = Column(String(length=255), nullable=False, unique=True)
    description = Column(String(length=255), nullable=True)
    timestamp_col = Column(String(length=255), nullable=False)
    source_type = Column(
        Enum("INVALID", "FILE", "SNOWFLAKE", "BIGQUERY", "REDSHIFT", name="sourcetype"),
        nullable=False,
    )
    file_options = Column(JSONB, nullable=True)
    big_query_options = Column(JSONB, nullable=True)
    snowflake_options = Column(JSONB, nullable=True)
    redshift_options = Column(JSONB, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    feature_bundles = relationship("FeatureBundleModel", back_populates="data_source")


class FeatureBundleModel(Base):
    __tablename__ = "feature_bundles"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), nullable=False, unique=True)
    description = Column(String(length=255), nullable=True)
    data_source_id = Column(Integer, ForeignKey("data_source.id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    entity_keys = Column(JSON, nullable=False)    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    data_source = relationship("DataSourceModel", back_populates="feature_bundles")
    features = relationship(
        "FeatureModel",
        back_populates="bundle",        
    )
    __table_args__ = (UniqueConstraint("id", "name"),)


class FeatureModel(Base):
    __tablename__ = "features"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), nullable=False)
    description = Column(String(length=255), nullable=True)
    expr = Column(String(length=255), nullable=False)
    dtype = Column(
        Enum("INT32", "INT64", "FLOAT64", "FLOAT32", "STRING", name="datatype"),
        nullable=False,
    )
    agg = Column(
        Enum("LATEST", "SUM", "AVG", "MIN", "MAX", name="aggregation"), nullable=False
    )
    window = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    bundle_id = Column(Integer, ForeignKey("feature_bundles.id"), nullable=False)
    bundle = relationship(
        "FeatureBundleModel",
        back_populates="features",
        foreign_keys=[bundle_id],
    )
