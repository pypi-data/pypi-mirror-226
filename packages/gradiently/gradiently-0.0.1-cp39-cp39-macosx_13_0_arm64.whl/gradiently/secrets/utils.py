from featureflow.secrets.provider import SecretsProvider
from featureflow.secrets.aws_provider import AWSSecretsProvider


def get_secret_provider(provider: str, region: str) -> SecretsProvider:
    providers_registry = {"aws": AWSSecretsProvider(region=region)}

    if provider not in providers_registry:
        raise Exception(f"The provider {provider} is not in the providers registry.")

    return providers_registry.get(provider)
