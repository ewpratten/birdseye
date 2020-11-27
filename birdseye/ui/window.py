import pygame
from typing import Optional, Tuple, List
import time
import math

from ..dynmap.models import DynmapPlayerModel, DynmapConfigurationModel
from ..dynmap.api import fetchPlayerFace, fetchWorldTile


class Window(object):

    # Window meta
    name: str
    endpoint: str

    # Rendering objects
    screen: pygame.Surface
    font: pygame.font.Font
    last_render_time = 0

    # Config
    config: Optional[DynmapConfigurationModel] = None

    # Ingame players
    online_players: List[DynmapPlayerModel] = []

    def __init__(self, name: str, endpoint: str, size: Optional[Tuple[int, int]] = (800, 600), font: Optional[pygame.font.Font] = None):
        self.name = name
        self.endpoint = endpoint

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
            return (self.config.updaterate * 1000) - (time.time() - self.last_render_time)

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
        player_face = fetchPlayerFace(self.endpoint, player.name)

        # Create the player name
        player_name = self.font.render(player.name, 1, (255, 255, 255))
        
        # Determine the number of chunks needed for the size
        chunks_needed = (math.ceil(size[0] / 128), math.ceil(size[1] / 128))


    def doRender(self):

        # Handle missing config
        if not self.isConnectedToServer():
            self.showFullscreenMessage("Connecting to server...")
            return

        # Track the time of render
        self.last_render_time = time.time()

        # Determine the number of screen segments to use
        screen_seg_count = len(self.online_players)
