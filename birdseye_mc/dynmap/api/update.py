import requests

from ..exceptions.invalid_endpoint_exception import InvalidEndpointException
from ..models import DynmapUpdateModel, DynmapConfigurationModel

def fetchServerUpdate(dynmap_url: str, config: DynmapConfigurationModel) -> DynmapUpdateModel:

    # Make remote request
    response = requests.get(f"{dynmap_url}/up/world/{config.defaultworld}/0")

    # Handle response error
    if int(response.status_code / 100) != 2:
        raise InvalidEndpointException(f"{dynmap_url}/up/world/{config.defaultworld}/0")

    # Deserialize contents
    return DynmapUpdateModel(**response.json())

