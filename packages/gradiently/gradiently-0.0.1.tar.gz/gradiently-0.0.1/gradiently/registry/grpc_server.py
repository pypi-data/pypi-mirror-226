import grpc
from gradiently.protos.gradiently.services.Registry_pb2_grpc import (
    RegistryServicer as RegistryServicerPb,
    add_RegistryServicer_to_server,
)
from gradiently.core.data_sources.file import FileType
from gradiently.protos.gradiently.services.Registry_pb2 import (
    BundleRequest,
    BundleResponse,
    GetBundleRequest,
    GetActiveBundlesRequest,
    GetActiveBundlesResponse,
    GetDataSourceRequest,
    GetDataSourceResponse,
)
import json
from gradiently.core.dtypes import DataType
from gradiently.core.data_sources.source import SourceType
from gradiently.protos.gradiently.core.Entity_pb2 import EntityKey as EntityKeyProto
from gradiently.protos.gradiently.core.Feature_pb2 import Feature as FeatureProto
from gradiently.protos.gradiently.core.FeatureBundle_pb2 import (
    FeatureBundle as FeatureBundleProto,
)
from gradiently.protos.gradiently.core.DataSource_pb2 import DataSource as DataSourceProto
from gradiently.registry.db_manager import DBManager
import logging
from google.protobuf import empty_pb2
from concurrent import futures
from datetime import timedelta
from gradiently.core.aggregation import AggregationType, Aggregation
from gradiently.registry.models import FeatureBundleModel
from google.protobuf.timestamp_pb2 import Timestamp


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]",  # Set the format of the logs
    handlers=[logging.StreamHandler()],  # Use StreamHandler to log to the console
)

logger = logging.getLogger(__name__)

def datetime_to_pb_timestamp(dt):
    timestamp = Timestamp()
    timestamp.FromDatetime(dt)
    return timestamp

def create_bundle_proto(bundle: FeatureBundleModel):
    bundle_proto = FeatureBundleProto()
    bundle_proto.name = bundle.name
    bundle_proto.description = bundle.description    

    data_source_proto = DataSourceProto()
    data_source_proto.name = bundle.data_source.name
    data_source_proto.description = bundle.data_source.description
    data_source_proto.timestamp_col = bundle.data_source.timestamp_col
    data_source_proto.source_type = SourceType[bundle.data_source.source_type].value
    entity_keys = json.loads(bundle.entity_keys)

    for entity, dtype in entity_keys.items():
        entity_proto = EntityKeyProto()
        entity_proto.name = entity
        entity_proto.dtype = dtype
        bundle_proto.entities.extend([entity_proto])

    if bundle.data_source.file_options:
        file_options = json.loads(bundle.data_source.file_options)
        data_source_proto.file_options.uri = file_options.get("uri")
        data_source_proto.file_options.file_type = FileType[
            file_options.get("file_type")
        ].value

    elif bundle.data_source.snowflake_options:
        snowflake_options = json.loads(bundle.data_source.snowflake_options)
        data_source_proto.snowflake_options.database = snowflake_options.get("database")
        data_source_proto.snowflake_options.table = snowflake_options.get("table")
        data_source_proto.snowflake_options.schema = snowflake_options.get("schema")

        data_source_proto.created_at.CopyFrom(datetime_to_pb_timestamp(bundle.data_source.created_at))

    bundle_proto.source.CopyFrom(data_source_proto)

    for feature in bundle.features:
        aggregation = Aggregation(
            method=AggregationType[feature.agg],
            window=timedelta(seconds=feature.window),
        )
        feature_proto = FeatureProto(
            name=feature.name,
            description=feature.description,
            expr=feature.expr,
            dtype=DataType[feature.dtype].value,
        )
        feature_proto.agg.CopyFrom(aggregation.to_proto())
        bundle_proto.features.extend([feature_proto])

    return bundle_proto


class RegistryServicer(RegistryServicerPb):
    def __init__(self):
        self._db = DBManager()

    @property
    def db(self):
        return self._db

    def GetDataSource(
        self, request: GetDataSourceRequest, context: grpc.ServicerContext
    ) -> GetDataSourceResponse:
        try:
            data_source = self.db.get_datasource(request)

            if not data_source:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Data source not found.")
                return

            data_source_proto = DataSourceProto()
            data_source_proto.name = data_source.name
            data_source_proto.description = data_source.description
            data_source_proto.timestamp_col = data_source.timestamp_col
            data_source_proto.source_type = SourceType[data_source.source_type].value

            response = GetDataSourceResponse()

            if data_source.snowflake_options:
                snowflake_options = json.loads(data_source.snowflake_options)
                data_source_proto.snowflake_options.database = snowflake_options.get(
                    "database"
                )
                data_source_proto.snowflake_options.table = snowflake_options.get(
                    "table"
                )
                data_source_proto.snowflake_options.schema = snowflake_options.get(
                    "schema"
                )
            elif data_source.redshift_options:                
                pass

            response.source.CopyFrom(data_source_proto)
            return response

        except Exception as e:
            logger.exception("An error occurred getting the data source: ", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(
                f"An internal error occurred while retrieving active bundles: {e}"
            )

    def GetBundle(self, request: GetBundleRequest, context: grpc.ServicerContext):
        try:
            bundle = self.db.get_bundle(request)
            bundle_proto = create_bundle_proto(bundle)
            response = BundleResponse()
            response.bundle.CopyFrom(bundle_proto)
            return response
        except Exception as e:
            logger.exception("An error occured getting this bundle: ", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(
                f"An internal error occurred while retrieving active bundles: {e}"
            )

    def GetActiveBundles(
        self, request: GetActiveBundlesRequest, context: grpc.ServicerContext
    ):
        try:
            # Assume you have a method in your database interface called get_active_bundle
            session = self.db.Session()
            active_bundles = self.db.get_active_bundles(session, request)
            response = GetActiveBundlesResponse()

            for bundle in active_bundles:
                bundle_proto = create_bundle_proto(bundle)
                response.bundles.extend([bundle_proto])
            return response
        except Exception as e:
            logger.exception("An error occurred getting active bundles: ", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(
                f"An internal error occurred while retrieving active bundles: {e}"
            )
        finally:
            session.close()

    def RegisterBundle(self, request: BundleRequest, context: grpc.ServicerContext):
        try:
            self.db.insert_bundle(request=request)
            response = BundleResponse()
            response.bundle.CopyFrom(request.bundle)
            return response
        except Exception as e:
            logger.exception("An error occurred reigstering the bundle: ", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(
                f"An internal error occurred while registering the bundle., {e}"
            )

    def ActivateBundle(self, request: BundleRequest, context: grpc.ServicerContext):
        try:
            self.db.activate_bundle(request)
            return empty_pb2.Empty()
        except Exception as e:
            logger.exception("An error occurred activating the bundle: ", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(
                f"An internal error occurred while registering the bundle., {e}"
            )

    def DeactivateBundle(self, request: BundleRequest, context):
        try:
            self.db.deactivate_bundle(request)
            return empty_pb2.Empty()
        except Exception as e:
            logger.exception("An error occurred deactivating the bundle: ", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(
                "An internal error occurred while deactivating the bundle."
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_RegistryServicer_to_server(RegistryServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Starting GRPC server...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
