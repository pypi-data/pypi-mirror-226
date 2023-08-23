import logging
from google.protobuf.json_format import MessageToJson
from typing import List, Optional
from gradiently.core.data_sources.source import SourceType
from gradiently.core.dtypes import DataType
from gradiently.registry.models import (
    DataSourceModel,
    NamespaceModel,
    FeatureBundleModel,
    FeatureModel,
)
import json
from gradiently.core.dtypes import DataType
from gradiently.protos.gradiently.services.Registry_pb2 import (
    BundleRequest,
    GetBundleRequest,
    GetDataSourceRequest,
)
import gradiently.protos.gradiently.core.DataSource_pb2 as DataSourceProto
from gradiently.core.aggregation import AggregationType, Aggregation
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)


class DBManager:
    def __init__(
        self,
        connection_uri: str = "postgresql+psycopg2://andrewtang@localhost/epochal",
    ):
        self.engine = create_engine(connection_uri, echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def insert_namespace_if_not_exists(
        self, session: Session, namespace_name: str, commit: bool = False
    ) -> NamespaceModel:
        """Inserts a namespace if it doesn't exist

        Args:
            session (Session): SQLALchemy session
            namespace_name (str): The name of the namespace
            commit (bool, optional): To commit the transaction. Defaults to False.

        Returns:
            NamespaceModel: Namespace SQL Alchemy Model
        """
        namespace = session.query(NamespaceModel).filter_by(name=namespace_name).first()

        if namespace is None:
            namespace = NamespaceModel(name=namespace_name)
            session.add(namespace)
        if commit:
            session.commit()
        return namespace

    def get_namespace(self, session: Session, namespace_name: str) -> NamespaceModel:
        namespace = session.query(NamespaceModel).filter_by(name=namespace_name).first()
        return namespace

    def get_datasource(
        self, request: GetDataSourceRequest
    ) -> Optional[DataSourceModel]:
        """
        Retrieves a specific data source by name from the provided namespace.

        Args:
            request (GetDataSourceRequest):

        Returns:
            Optional[DataSourceModel]: The matching data source if found, otherwise returns None.
        """
        with self.Session() as session:
            namespace = self.get_namespace(session, request.namespace)
            for source in namespace.data_sources:
                if source.name == request.name:
                    return source

    def insert_datasource_if_not_exists(
        self,
        session: Session,
        namespace: NamespaceModel,
        data_source_proto: DataSourceProto,
        commit: bool = False,
    ) -> DataSourceModel:
        """Inserts a data source if it doesn't exist

        Args:
            session (Session): SQLALchemy session
            namespace (NamespaceModel): NamespaceModel of the datasource
            data_source_proto (DataSourceProto): Protobuf representation of data source
            commit (bool, optional): If we should commit to DB within this call. Defaults to False.

        Returns:
            DataSourceModel: DataSourceModel Type (ORM)
        """
        data_source = (
            session.query(DataSourceModel)
            .filter_by(name=data_source_proto.name)
            .first()
        )
        if data_source is None:
            # Initialize all options to None
            file_options = None
            big_query_options = None
            snowflake_options = None
            redshift_options = None

            # Check which one of the options is set and convert it to JSON
            which_option = data_source_proto.WhichOneof("options")
            if which_option:
                option_value = getattr(data_source_proto, which_option)
                if which_option == "file_options":
                    file_options = MessageToJson(option_value)
                elif which_option == "big_query_options":
                    big_query_options = MessageToJson(option_value)
                elif which_option == "snowflake_options":
                    snowflake_options = MessageToJson(option_value)
                elif which_option == "redshift_options":
                    redshift_options = MessageToJson(option_value)

            data_source = DataSourceModel(
                namespace_id=namespace.id,
                name=data_source_proto.name,
                description=data_source_proto.description,
                timestamp_col=data_source_proto.timestamp_col,
                source_type=SourceType(data_source_proto.source_type).name,
                file_options=file_options,
                big_query_options=big_query_options,
                snowflake_options=snowflake_options,
                redshift_options=redshift_options,
            )
            session.add(data_source)
            if commit:
                session.commit()
        return data_source

    def insert_bundle(self, request: BundleRequest):
        """Inserts a bundle from a bundle request

        Args:
            request (BundleRequest): A request containing a bundle
        """
        session = self.Session()
        bundle = request.bundle

        try:
            namespace = self.insert_namespace_if_not_exists(
                session=session, namespace_name=request.namespace
            )
            data_source = self.insert_datasource_if_not_exists(
                session=session,
                namespace=namespace,
                data_source_proto=bundle.source,
            )

            feature_bundle = (
                session.query(FeatureBundleModel)
                .filter_by(name=bundle.name)
                .first()
            )
            if feature_bundle is not None:
                raise Exception("A bundle with this name already exists")

            feature_bundle = FeatureBundleModel(
                name=bundle.name,
                description=bundle.description,
                data_source_id=data_source.id,                
                entity_keys=json.dumps(
                    {key.name: key.dtype for key in bundle.entities}
                ),
            )
            session.add(feature_bundle)
            session.commit()

            with session.begin_nested():
                # Iterate through the features in the request, creating new FeatureModel objects if they don't exist
                for f in bundle.features:
                    feature = FeatureModel(
                        name=f.name,
                        description=f.description,
                        expr=f.expr,
                        dtype=DataType(f.dtype).name,
                        agg=AggregationType(f.agg.method).name,
                        window=f.agg.window,
                        bundle_id=feature_bundle.id,                        
                    )
                    session.add(feature)

                session.commit()
        except Exception as e:
            logger.exception(e)
            session.rollback()
            raise
        finally:
            session.close()

    def get_active_bundles(
        self, session: Session, request: BundleRequest
    ) -> List[FeatureBundleModel]:
        try:
            active_bundles = []
            namespace = self.get_namespace(session, request.namespace)
            if namespace:
                for source in namespace.data_sources:
                    for bundle in source.feature_bundles:
                        # if bundle.is_active:
                        active_bundles.append(bundle)

            return active_bundles
        except Exception as e:
            logger.exception(e)
            session.rollback()
            raise

    def activate_bundle(self, request: BundleRequest):
        with self.Session() as session:
            try:
                namespace = self.insert_namespace_if_not_exists(
                    session, request.namespace
                )
                active_features = set()

                for source in namespace.data_sources:
                    for bundle in source.feature_bundles:
                        if bundle.name == request.bundle.name:
                            bundle.is_active = False
                        elif bundle.is_active:
                            for feature in bundle.features:
                                logger.info(feature.name)
                                active_features.add(feature.name)

                features_to_active = set(f.name for f in request.bundle.features)
                intersecting_features = active_features & features_to_active
                if intersecting_features:
                    raise Exception(
                        f"Please use non-intersecting feature names in active bundles. These features are already active in a bundle: {intersecting_features}"
                    )

                feature_bundle = (
                    session.query(FeatureBundleModel)
                    .filter_by(name=request.bundle.name)
                    .first()
                )
                feature_bundle.is_active = True
                session.commit()
            except Exception as e:
                logger.exception(e)
                session.rollback()
                raise

    def deactivate_bundle(self, request: BundleRequest):
        with self.Session() as session:
            try:
                feature_bundle = (
                    session.query(FeatureBundleModel)
                    .filter_by(name=request.bundle.name)
                    .first()
                )
                if feature_bundle:
                    feature_bundle.is_active = False
                    session.commit()
                else:
                    logger.warning("Bundle not found!")
            except Exception as e:
                logger.exception(e)
                session.rollback()
                raise

    def get_bundle(self, request: GetBundleRequest) -> FeatureBundleModel:
        session = self.Session()
        feature_bundle = (
            session.query(FeatureBundleModel).filter_by(name=request.name).first()
        )

        if feature_bundle is None:
            raise Exception("Bundle not found")
        return feature_bundle
