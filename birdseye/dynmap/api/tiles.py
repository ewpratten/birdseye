import requests
from pygame import Surface
import pygame.image
from io import BytesIO
from typing import List

from ..exceptions.invalid_endpoint_exception import InvalidEndpointException


def fetchWorldTile(dynmap_url: str, world: str, x: int, y: int) -> Surface:
    """Fetches a world chunk

    Args:
        dynmap_url (str): Dynmap server url
        world (str): World name
        x (int): X coord
        y (int): Y coord

    Raises:
        InvalidEndpointException: Thrown if there is an API error

    Returns:
        Surface: Chunk surface
    """

    # Convert coords to chunk number
    chunk_x = x/16
    chunk_y = y/16

    # Make remote request
    response = requests.get(
        f"{dynmap_url}/tiles/world/flat/-1_0/{chunk_x}_{chunk_y}.jpg")

    # Handle response error
    if int(response.status_code / 100) != 2:
        raise InvalidEndpointException(
            f"{dynmap_url}/tiles/world/flat/-1_0/{chunk_x}_{chunk_y}.jpg")

    # Load to an image
    img = BytesIO(response.content)

    return pygame.image.load(img, namehint=f"({x}, {y})")


def fetch3X3WorldTiles(dynmap_url: str, world: str, x: int, y: int) -> List[List[Surface]]:
    """Get a 3x3 area of world tiles around a coordinate

    Args:
        dynmap_url (str): Dynmap API url
        world (str): World name
        x (int): X coord
        y (int): Y coord

    Returns:
        List[List[Surface]]: Images
    """

    output = []
    output.append([
        fetchWorldTile(dynmap_url, world, x - 16, y+16),
        fetchWorldTile(dynmap_url, world, x, y+16),
        fetchWorldTile(dynmap_url, world, x + 16, y+16),
    ])
    output.append([
        fetchWorldTile(dynmap_url, world, x - 16, y),
        fetchWorldTile(dynmap_url, world, x, y),
        fetchWorldTile(dynmap_url, world, x + 16, y),
    ])
    output.append([
        fetchWorldTile(dynmap_url, world, x - 16, y-16),
        fetchWorldTile(dynmap_url, world, x, y-16),
        fetchWorldTile(dynmap_url, world, x + 16, y-16),
    ])

    return output
