import requests
from pygame import Surface
import pygame.image
from io import BytesIO

from ..exceptions.invalid_endpoint_exception import InvalidEndpointException


def fetchPlayerFace(dynmap_url: str, player_name: str) -> Surface:
    """Fetches a player's face texture

    Args:
        dynmap_url (str): URL of dynmap server
        player_name (str): Player name

    Raises:
        InvalidEndpointException: Thrown if there is an API error

    Returns:
        Surface: Image surface
    """

    # Make remote request
    response = requests.get(
        f"{dynmap_url}/tiles/faces/16x16/{player_name}.png")

    # Handle response error
    if int(response.status_code / 100) != 2:
        raise InvalidEndpointException(
            f"{dynmap_url}/tiles/faces/16x16/{player_name}.png")

    # Load to an image
    img = BytesIO(response.content)

    return pygame.image.load(img)
