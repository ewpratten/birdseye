import requests
from pygame import Surface
import pygame.image
import pygame.font
from io import BytesIO
from typing import List, Dict
import math
import time

from ..exceptions.invalid_endpoint_exception import InvalidEndpointException

class _CachedSurface(object):
    surface: Surface
    clean_time: float

tile_cache: Dict[str, _CachedSurface] = {}


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

    global tile_cache

    # Convert coords to chunk number
    chunk_x = round(x/32)
    chunk_y = round((y * -1) / 32)
    
    # Search for (and clean) cache
    for key in list(tile_cache.keys()):

        if key == f"{chunk_x}_{chunk_y}" and key in list(tile_cache.keys()):
            if debug:
                print(f"using cached tile: {chunk_x}_{chunk_y}")
            return tile_cache[f"{chunk_x}_{chunk_y}"].surface

        if tile_cache[key].clean_time < time.time():
            del tile_cache[key]

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
        loaded_texture.blit(text, (64, 64))
        
    # Cache the image
    tile_cache[f"{chunk_x}_{chunk_y}"] = _CachedSurface()
    tile_cache[f"{chunk_x}_{chunk_y}"].surface = loaded_texture
    tile_cache[f"{chunk_x}_{chunk_y}"].clean_time = time.time() + 20.0
    if debug:
        print(f"Cached tile: {chunk_x}_{chunk_y}")

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
