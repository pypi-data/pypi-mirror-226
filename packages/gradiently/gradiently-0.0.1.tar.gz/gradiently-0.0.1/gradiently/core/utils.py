from typing import List, Tuple
from gradiently.core.feature_bundle import FeatureBundle
from gradiently.protos.gradiently.core.FeatureBundle_pb2 import (
    FeatureBundles as FeatureBundlesProto,
)
from gradiently.core.obs_query import ObservationQuery
from google.protobuf.json_format import MessageToJson


def json_serialize_bundles(bundles: List[FeatureBundle]) -> str:
    f_bundles_proto = FeatureBundlesProto()
    f_bundles_proto.bundles.extend([bundle.to_proto() for bundle in bundles])
    feature_bundles_proto_json = MessageToJson(f_bundles_proto)
    return feature_bundles_proto_json


def json_serialize_inputs(
    feature_bundles: List[FeatureBundle], observation_query: ObservationQuery
) -> Tuple[str, str]:
    obs_query_proto = observation_query.to_proto()
    obs_query_proto_json = MessageToJson(obs_query_proto)

    return json_serialize_bundles(feature_bundles), obs_query_proto_json
