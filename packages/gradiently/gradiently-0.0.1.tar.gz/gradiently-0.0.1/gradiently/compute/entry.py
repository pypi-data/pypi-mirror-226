import logging
import argparse
from gradiently.compute.compute_historical_features import (
    compute_historical_features,
)
from gradiently.compute.materialize_features import materialize_features
from pyspark.sql import functions as F


logging.basicConfig(
    level=logging.INFO,  # Set the logging level to DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]",  # Set the format of the logs
    handlers=[logging.StreamHandler()],  # Use StreamHandler to log to the console
)
logger = logging.getLogger(__name__)


def cli():
    parser = argparse.ArgumentParser(description="gradiently Computation Engine")
    subparsers = parser.add_subparsers()

    # Define compute historical features parser
    compute_historical_features_parser = subparsers.add_parser(
        "compute_historical_features", help="Computes Historical Features"
    )
    compute_historical_features_parser.add_argument(
        "--namespace",
        type=str,
        required=True,
        help="Namespace of the job",
    )

    compute_historical_features_parser.add_argument(
        "--feature_bundles_json", type=str, help="Feature bundles string", required=True
    )
    compute_historical_features_parser.add_argument(
        "--observation_query_json",
        type=str,
        help="observation query json",
        required=True,
    )
    compute_historical_features_parser.add_argument(
        "--output_path", type=str, help="the output path of the job", required=True
    )
    compute_historical_features_parser.add_argument(
        "--secrets_provider",
        type=str,
        choices=["aws", "gcp", "azure", "local"],
        required=True,
        help="Choose a secrets provider: aws, gcp, or azure",
    )
    compute_historical_features_parser.add_argument(
        "--provider_region",
        type=str,
        required=True,
        help="Choose a region for your secrets provider",
    )

    compute_historical_features_parser.set_defaults(func=compute_historical_features)

    materialize_features_parser = subparsers.add_parser(
        "materialize", help="Materialize Features into an online store"
    )
    materialize_features_parser.add_argument(
        "--namespace",
        type=str,
        required=True,
        help="Namespace of the job",
    )
    materialize_features_parser.add_argument(
        "--feature_bundles_json", type=str, help="Feature bundles string", required=True
    )
    materialize_features_parser.add_argument(
        "--secrets_provider",
        type=str,
        choices=["aws", "gcp", "azure", "local"],
        required=True,
        help="Choose a secrets provider: aws, gcp, or azure",
    )
    materialize_features_parser.add_argument(
        "--provider_region",
        type=str,
        required=True,
        help="Choose a region for your secrets provider",
    )
    materialize_features_parser.set_defaults(func=materialize_features)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    cli()
