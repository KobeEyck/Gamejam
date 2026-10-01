"""
World Map & Terrain (Dev 3)
Builds the 2D world layout:
- Tranquil Lake (far left)
- Concrete Helipad (near lake)
- Rugged terrain slopes
- Massive glowing Caldera (far right)
"""
import pygame
from src.settings import (
    WORLD_WIDTH, WORLD_HEIGHT,
    LAKE_ZONE_START, LAKE_ZONE_END, LAKE_WATER_LEVEL,
    HELIPAD_X, HELIPAD_WIDTH, HELIPAD_Y,
    CALDERA_X_CENTER, CALDERA_CRATER_WIDTH, CALDERA_Y,
    COLOR_TERRAIN, COLOR_TERRAIN_OUTLINE,
    COLOR_LAKE, COLOR_LAKE_SURFACE,
    COLOR_LAVA, COLOR_HELIPAD, COLOR_HELIPAD_MARKING
)
from src.world.zones import LakeZone, HelipadZone, CalderaZone

class WorldMap:
    def __init__(self):
        self.lake_zone = LakeZone()
        self.helipad_zone = HelipadZone()
        self.caldera_zone = CalderaZone()
        
        # Precomputed terrain polygon points
        self.terrain_points = self._generate_terrain_polygon()

    def _generate_terrain_polygon(self):
        """Creates the contour profile of the landscape from lake to volcano."""
        pts = [
            (0, LAKE_WATER_LEVEL),
            (LAKE_ZONE_START, LAKE_WATER_LEVEL),
            # Lake depression
            (LAKE_ZONE_START + 50, LAKE_WATER_LEVEL + 80),
            (LAKE_ZONE_END - 50, LAKE_WATER_LEVEL + 80),
            (LAKE_ZONE_END, LAKE_WATER_LEVEL),
            # Helipad area
            (HELIPAD_X - 20, HELIPAD_Y),
            (HELIPAD_X + HELIPAD_WIDTH + 20, HELIPAD_Y),
            # Gentle rise
            (1600, 680),
            (2200, 620),
            # Rugged volcano slope
            (3000, 520),
            (3600, 380),
            # Caldera crater rim
            (CALDERA_X_CENTER - (CALDERA_CRATER_WIDTH // 2), 350),
            # Caldera crater floor (lava pit)
            (CALDERA_X_CENTER - 150, CALDERA_Y),
            (CALDERA_X_CENTER + 150, CALDERA_Y),
            # Caldera right rim
            (CALDERA_X_CENTER + (CALDERA_CRATER_WIDTH // 2), 350),
            # Far right slope
            (WORLD_WIDTH, 480),
            # World bottom border
            (WORLD_WIDTH, WORLD_HEIGHT),
            (0, WORLD_HEIGHT)
        ]
        return pts

    def draw(self, surface: pygame.Surface, camera):
        # 1. Transform terrain points to screen coordinates
        screen_pts = [camera.apply(pt) for pt in self.terrain_points]
        pygame.draw.polygon(surface, COLOR_TERRAIN, screen_pts)
        pygame.draw.lines(surface, COLOR_TERRAIN_OUTLINE, False, screen_pts[:-2], 3)

        # 2. Draw Lake Water
        lake_rect = pygame.Rect(LAKE_ZONE_START, LAKE_WATER_LEVEL, 
                                LAKE_ZONE_END - LAKE_ZONE_START, 80)
        screen_lake = camera.apply(lake_rect)
        pygame.draw.rect(surface, COLOR_LAKE, screen_lake)
        pygame.draw.line(surface, COLOR_LAKE_SURFACE, screen_lake.topleft, screen_lake.topright, 3)

        # 3. Draw Concrete Helipad
        helipad_rect = pygame.Rect(HELIPAD_X, HELIPAD_Y, HELIPAD_WIDTH, 12)
        screen_pad = camera.apply(helipad_rect)
        pygame.draw.rect(surface, COLOR_HELIPAD, screen_pad)
        # Yellow "H" landing mark
        font = pygame.font.Font(None, 24)
        h_surf = font.render("[ H ] SHOP", True, COLOR_HELIPAD_MARKING)
        surface.blit(h_surf, (screen_pad.x + 35, screen_pad.y - 18))

        # 4. Draw Caldera Lava Pit
        lava_rect = pygame.Rect(CALDERA_X_CENTER - 150, CALDERA_Y - 15, 300, 30)
        screen_lava = camera.apply(lava_rect)
        pygame.draw.rect(surface, COLOR_LAVA, screen_lava)
