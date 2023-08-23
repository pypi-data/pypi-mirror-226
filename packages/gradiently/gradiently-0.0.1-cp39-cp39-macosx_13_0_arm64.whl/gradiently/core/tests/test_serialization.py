import unittest
from gradiently.core import (
    Feature,
    Int32,
    String,
    FeatureBundle,
    SnowflakeSource,
)
from gradiently.core.entity_key import EntityKey
from gradiently.core.aggregation import Aggregation, AggregationType
from datetime import timedelta


class TestProtobufSerialization(unittest.TestCase):
    def test_feature_serialization(self):
        time_window = 10
        agg = Aggregation(
            method=AggregationType.SUM, window=timedelta(days=time_window)
        )

        f = Feature(
            name=f"f_total_streamed_secs_{time_window}_days",
            description="description",
            dtype=String,
            expr="streamed_secs",
            agg=agg,
        )

        proto_x = f.to_proto()
        new_f = Feature.from_proto(proto_x)

        self.assertEqual(
            f.name,
            new_f.name,
            "Feature names not equal after serialization/deserialization",
        )

    def test_bundle_serialization(self):
        snowflake_feature_bundle = self._get_feature_bundle()

        bundle_proto = snowflake_feature_bundle.to_proto()
        new_bundle = FeatureBundle.from_proto(bundle_proto)

        self.assertEqual(
            snowflake_feature_bundle.version,
            new_bundle.version,
            "Bundle ids not equal after serialization/deserialization",
        )

    def _get_feature_bundle(self):
        streaming_source = SnowflakeSource(
            name="Streaming Data",
            description="Stream Data",
            timestamp_col="timestamp",
            table="streamdata",
            database="gradiently",
            schema="public",
        )

        user_entity = EntityKey(
            name="user",
            dtype=Int32,
        )

        snowflake_feature_bundle = FeatureBundle(
            name="snowflake_numeric_aggregation_bundle",
            description="funny bundle",
            source=streaming_source,
            entity_keys=[user_entity],
        )

        time_windows = [x for x in range(1, 19)]

        snowflake_feature_bundle.add_features(
            [
                Feature(
                    name=f"f_total_streamed_secs_{x}_days",
                    description="description",
                    dtype=String,
                    expr="streamed_secs",
                    agg=Aggregation(
                        method=AggregationType.SUM, window=timedelta(days=x)
                    ),
                )
                for x in time_windows
            ]
        )

        return snowflake_feature_bundle


if __name__ == "__main__":
    unittest.main()
