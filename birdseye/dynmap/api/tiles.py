import requests
from pygame import Surface
import pygame.image
import pygame.font
from io import BytesIO
from typing import List
import math

from ..exceptions.invalid_endpoint_exception import InvalidEndpointException


def fetchWorldTile(dynmap_url: str, world: str, x: int, y: int, debug=False) -> Surface:
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
    chunk_x = round(x/32)
    chunk_y = round((y*-1)/32)

    # Make remote request
    response = requests.get(
        f"{dynmap_url}/tiles/world/flat/-1_0/{chunk_x}_{chunk_y}.jpg")
    # print(f"{dynmap_url}/tiles/world/flat/-1_0/{chunk_x}_{chunk_y}.jpg")

    # Handle response error
    if int(response.status_code / 100) != 2:
        raise InvalidEndpointException(
            f"{dynmap_url}/tiles/world/flat/-1_0/{chunk_x}_{chunk_y}.jpg")

    # Load to an image
    img = BytesIO(response.content)

    loaded_texture = pygame.image.load(img)

    # Handle debug rendering
    if debug:
        font = pygame.font.Font(None, 25)
        text = font.render(f"({chunk_x}, {chunk_y})", 1, (255, 0, 0))
        loaded_texture.blit(text, (64,64))

    return loaded_texture

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
