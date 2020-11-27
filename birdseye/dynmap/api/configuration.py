import requests

from ..exceptions.invalid_endpoint_exception import InvalidEndpointException
from ..models import DynmapConfigurationModel


def fetchServerConfiguration(dynmap_url: str) -> DynmapConfigurationModel:
    """Fetch server configuration data from a Dynmap server

    Args:
        dynmap_url (str): Dynmap URL

    Raises:
        InvalidEndpointException: Thrown if the server is invalid

    Returns:
        DynmapConfigurationModel: Deserialized data
    """

    # Make remote request
    response = requests.get(f"{dynmap_url}/up/configuration")

    # Handle response error
    if int(response.status_code / 100) != 2:
        raise InvalidEndpointException(f"{dynmap_url}/up/configuration")

    # Deserialize contents
    return DynmapConfigurationModel(**response.json())
