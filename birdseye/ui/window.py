import pygame
from typing import Optional, Tuple, List
import time
import math

from ..dynmap.models import DynmapPlayerModel, DynmapConfigurationModel
from ..dynmap.api import fetchPlayerFace, fetchWorldTile
from ..dynmap.exceptions import InvalidEndpointException


class _WorldTile(object):
    x: int
    y: int
    image: pygame.Surface


class Window(object):

    # Window meta
    name: str
    endpoint: str
    debug: bool

    # Rendering objects
    screen: pygame.Surface
    font: pygame.font.Font
    last_render_time = 0

    # Config
    config: Optional[DynmapConfigurationModel] = None

    # Ingame players
    online_players: List[DynmapPlayerModel] = []

    def __init__(self, name: str, endpoint: str, size: Optional[Tuple[int, int]] = (800, 600), font: Optional[pygame.font.Font] = None, debug: Optional[bool] = False):
        self.name = name
        self.endpoint = endpoint
        self.debug = debug

        # Init the window
        pygame.init()
        self.screen = pygame.display.set_mode(
            size=size, flags=pygame.RESIZABLE | pygame.SHOWN)
        pygame.display.set_caption(name)

        # Handle font setup
        if not font:
            self.font = pygame.font.Font(None, 36)
        else:
            self.font = font

        # Render startup message
        self.showFullscreenMessage("Waiting for data...")

    def _getScreenSize(self) -> Tuple[int, int]:
        return self.screen.get_size()

    def _generateBackgroundTexture(self) -> pygame.Surface:

        # Create a new black surface
        bg = pygame.Surface(self._getScreenSize())
        bg = bg.convert()
        bg.fill((0, 0, 0))

        return bg

    def showFullscreenMessage(self, message: str) -> None:

        # Create a background
        bg = self._generateBackgroundTexture()

        # Create a text object
        text: pygame.Surface = self.font.render(message, 1, (255, 255, 255))

        # Translate the text to the center of the screen
        text_bounds = text.get_rect()
        bg_bounds = bg.get_rect()
        text_bounds.centerx = bg_bounds.centerx
        text_bounds.centery = bg_bounds.centery

        # Render everything
        bg.blit(text, text_bounds)
        self.screen.blit(bg, (0, 0))
        pygame.display.flip()

    def loadServerConfig(self, model: DynmapConfigurationModel) -> None:
        self.config = model

    def isConnectedToServer(self) -> bool:
        return self.config != None

    def getTimeUntilNextFrame(self) -> float:

        # If there is no connection, default on a large timeout
        if not self.isConnectedToServer():
            return 0
        else:
            return ((self.config.updaterate / 2) / 1000) - (time.time() - self.last_render_time)

    def updatePlayerList(self, players: List[DynmapPlayerModel]):
        self.online_players = players

    def shouldQuit(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        else:
            return False

    def _getPlayerSurface(self, player: DynmapPlayerModel, size: Tuple[int, int]) -> pygame.Surface:

        # Build a base surface
        base_surf = pygame.Surface(size)
        base_surf = base_surf.convert()

        # Fetch the player's head
        player_face: pygame.Surface = None
        if not player.test:
            try:
                player_face = fetchPlayerFace(self.endpoint, player.name)
            except InvalidEndpointException as e:
                pass

        # Create the player name
        player_name = self.font.render(player.name, 1, (255, 255, 255))
        player_nameplate = pygame.Surface((player_name.get_rect().width, player_name.get_rect().height), pygame.SRCALPHA)
        player_nameplate.fill((50,50,50,128))
        player_nameplate.blit(player_name, (0,0))

        # Determine the number of chunks needed for the size
        chunks_needed = (
            math.ceil(size[0] / 128) + 1, math.ceil(size[1] / 128) + 1)

        # List of surfaces
        world_tiles: List[_WorldTile] = []

        # Fetch all tiles
        for x in range(chunks_needed[0]):
            x = x - chunks_needed[0]/2
            for y in range(chunks_needed[1]):
                y = y - chunks_needed[1]/2

                # Convert to a world coordinate
                # NOTE: My program uses an X/Y plane for coordinates, while Minecaft is X/Z, so this also converts coordinates
                # On top of this, Minecraft is built on a 16x256x16 chunk system, but dynmap uses a 32x256x32 system
                x_coord = (x * 32) + player.x
                y_coord = (y * 32) + player.z

                # Get the tile
                tile = fetchWorldTile(
                    self.endpoint, player.world, x_coord, y_coord, debug=self.debug)

                # Build tile
                w_tile = _WorldTile()
                w_tile.image = tile
                w_tile.x = x
                w_tile.y = y
                world_tiles.append(w_tile)

        # Get the base surface bounds
        base_bounds = base_surf.get_rect()

        # Render every tile onto the surface
        for tile in world_tiles:

            # Get the tile bounds
            tile_bounds = tile.image.get_rect()

            # Determine the tile position in pixels
            tile_bounds.centerx = (
                (tile.x * tile_bounds.width) + base_bounds.centerx)
            tile_bounds.centery = (
                (tile.y * tile_bounds.height) + base_bounds.centery)

            # Overlay
            base_surf.blit(tile.image, tile_bounds)

        # Render the player head
        if player_face:
            base_surf.blit(player_face, (10, 10))

        # Render the player name
        base_surf.blit(player_nameplate, (35, 10))

        # Add a border
        pygame.draw.rect(base_surf, (128, 0, 0), base_bounds, width=5)

        return base_surf

    def doRender(self):

        # Handle missing config
        if not self.isConnectedToServer():
            self.showFullscreenMessage("Connecting to server...")
            return

        # Track the time of render
        self.last_render_time = time.time()

        # Determine the number of screen segments to use
        screen_seg_count = len(self.online_players)

        # Create a background
        bg = self._generateBackgroundTexture()
        self.screen.blit(bg, (0, 0))

        # TODO: Test only
        i = 0
        for player in self.online_players:
            if not player.isInHiddenWorld():
                self.screen.blit(self._getPlayerSurface(
                    player, (256 * 2, 256 * 2)), (256 * 2 * i, 0))
                i += 1

        # Display screen contents
        pygame.display.flip()
