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
    COLOR_LAVA, COLOR_HELIPAD, COLOR_HELIPAD_MARKING,
    COLOR_BG_LAYER1, COLOR_BG_LAYER2
)
from src.world.zones import LakeZone, HelipadZone, CalderaZone

class WorldMap:
    def __init__(self):
        self.lake_zone = LakeZone()
        self.helipad_zone = HelipadZone()
        self.caldera_zone = CalderaZone()
        
        # Precomputed terrain polygon points
        self.terrain_points = self._generate_terrain_polygon()
        self._generate_backgrounds()

    def _generate_backgrounds(self):
        import math
        # Layer 1: Distant mountains (slow parallax)
        self.bg_layer1 = []
        for x in range(-1500, WORLD_WIDTH + 2500, 250):
            y = 400 + math.sin(x * 0.005) * 120 + math.cos(x * 0.01) * 60
            self.bg_layer1.append((x, y))
        self.bg_layer1 = [(-1500, WORLD_HEIGHT)] + self.bg_layer1 + [(WORLD_WIDTH + 2500, WORLD_HEIGHT)]

        # Layer 2: Closer mountains/hills (medium parallax)
        self.bg_layer2 = []
        for x in range(-1500, WORLD_WIDTH + 2500, 150):
            y = 550 + math.sin(x * 0.008 + 1.0) * 90 + math.cos(x * 0.015) * 45
            self.bg_layer2.append((x, y))
        self.bg_layer2 = [(-1500, WORLD_HEIGHT)] + self.bg_layer2 + [(WORLD_WIDTH + 2500, WORLD_HEIGHT)]

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
            (2600, 580),
            # Rugged volcano steep slope
            (3000, 450),
            (3400, 300),
            # Caldera crater left rim (sharp peak)
            (CALDERA_X_CENTER - (CALDERA_CRATER_WIDTH // 2), 220),
            # Caldera crater floor (lava pit, very deep)
            (CALDERA_X_CENTER - 150, CALDERA_Y),
            (CALDERA_X_CENTER + 150, CALDERA_Y),
            # Caldera right rim
            (CALDERA_X_CENTER + (CALDERA_CRATER_WIDTH // 2), 220),
            # Far right slope
            (4700, 450),
            (WORLD_WIDTH, 550),
            # World bottom border
            (WORLD_WIDTH, WORLD_HEIGHT),
            (0, WORLD_HEIGHT)
        ]
        return pts

    def get_terrain_y(self, x: float) -> float:
        """Returns the interpolated y-coordinate of the terrain at a given x."""
        for i in range(len(self.terrain_points) - 1):
            p1 = self.terrain_points[i]
            p2 = self.terrain_points[i+1]
            # Since the points generally progress from left to right:
            if p1[0] <= x <= p2[0] and p2[0] != p1[0]:
                t = (x - p1[0]) / (p2[0] - p1[0])
                return p1[1] + t * (p2[1] - p1[1])
        return WORLD_HEIGHT

    def draw(self, surface: pygame.Surface, camera):
        # Draw Parallax Backgrounds
        # Layer 1 (Slow parallax)
        l1_pts = []
        for pt in self.bg_layer1:
            lx = pt[0] - camera.offset_x * 0.2
            ly = pt[1] - camera.offset_y * 0.1
            l1_pts.append((lx, ly))
        pygame.draw.polygon(surface, COLOR_BG_LAYER1, l1_pts)

        # Layer 2 (Medium parallax)
        l2_pts = []
        for pt in self.bg_layer2:
            lx = pt[0] - camera.offset_x * 0.5
            ly = pt[1] - camera.offset_y * 0.2
            l2_pts.append((lx, ly))
        pygame.draw.polygon(surface, COLOR_BG_LAYER2, l2_pts)

        # 1. Transform main terrain points to screen coordinates
        screen_pts = [camera.apply(pt) for pt in self.terrain_points]
        pygame.draw.polygon(surface, COLOR_TERRAIN, screen_pts)
        pygame.draw.lines(surface, COLOR_TERRAIN_OUTLINE, False, screen_pts[:-2], 3)

        # 1.5 Draw Volcano Rocky Overlay
        volc_start_x = 2400
        volc_pts = [(volc_start_x, WORLD_HEIGHT), (volc_start_x, self.get_terrain_y(volc_start_x))]
        for pt in self.terrain_points:
            if volc_start_x < pt[0] < WORLD_WIDTH:
                volc_pts.append(pt)
        volc_pts.append((WORLD_WIDTH, self.get_terrain_y(WORLD_WIDTH)))
        volc_pts.append((WORLD_WIDTH, WORLD_HEIGHT))
        
        screen_volc = [camera.apply(pt) for pt in volc_pts]
        COLOR_VOLCANO = (50, 45, 50)
        pygame.draw.polygon(surface, COLOR_VOLCANO, screen_volc)
        pygame.draw.lines(surface, (30, 25, 30), False, screen_volc[1:-2], 4)

        # Lava Cracks on the volcano slope
        cracks = [
            [(2900, self.get_terrain_y(2900)), (2930, 550), (2910, 600), (2950, 680)],
            [(3300, self.get_terrain_y(3300)), (3280, 420), (3320, 480), (3300, 550), (3360, 650)],
            [(4500, self.get_terrain_y(4500)), (4520, 380), (4490, 430), (4550, 520)],
        ]
        for crack in cracks:
            screen_crack = [camera.apply(pt) for pt in crack]
            pygame.draw.lines(surface, (255, 80, 10), False, screen_crack, 4)
            pygame.draw.lines(surface, (255, 200, 50), False, screen_crack, 2) # inner glow

        # 2. Draw Lake Water (Animated Waves)
        import time
        import math
        t = time.time() * 3.0
        lake_surface_pts = []
        for x in range(LAKE_ZONE_START, LAKE_ZONE_END + 10, 20):
            x = min(x, LAKE_ZONE_END)
            y = LAKE_WATER_LEVEL + math.sin(x * 0.05 + t) * 4
            lake_surface_pts.append((x, y))
            
        lake_poly = lake_surface_pts + [
            (LAKE_ZONE_END - 50, LAKE_WATER_LEVEL + 80),
            (LAKE_ZONE_START + 50, LAKE_WATER_LEVEL + 80)
        ]
        
        screen_lake_poly = [camera.apply(pt) for pt in lake_poly]
        pygame.draw.polygon(surface, COLOR_LAKE, screen_lake_poly)
        
        screen_surf_pts = [camera.apply(pt) for pt in lake_surface_pts]
        if len(screen_surf_pts) > 1:
            pygame.draw.lines(surface, COLOR_LAKE_SURFACE, False, screen_surf_pts, 3)
            
        # Optional: draw some underwater depth lines
        for offset_y in [20, 40, 60]:
            line_pts = [(x, y + offset_y) for x, y in lake_surface_pts[2:-2]]
            screen_line_pts = [camera.apply(pt) for pt in line_pts]
            if len(screen_line_pts) > 1:
                pygame.draw.lines(surface, (50, 150, 230), False, screen_line_pts, 2)

        # 3. Draw Concrete Helipad
        helipad_rect = pygame.Rect(HELIPAD_X, HELIPAD_Y, HELIPAD_WIDTH, 12)
        screen_pad = camera.apply(helipad_rect)
        pygame.draw.rect(surface, COLOR_HELIPAD, screen_pad)
        # Yellow "H" landing mark
        font = pygame.font.Font(None, 24)
        h_surf = font.render("[ H ] SHOP", True, COLOR_HELIPAD_MARKING)
        surface.blit(h_surf, (screen_pad.x + 35, screen_pad.y - 18))

        # 4. Draw Caldera Lava Pit (Glowing multi-layered pool)
        pool_y = CALDERA_Y - 20
        # Draw multiple rects with decreasing size and increasing brightness
        layers = [
            (0, 320, (180, 30, 10)),
            (6, 300, (230, 70, 20)),
            (12, 270, (255, 140, 30)),
            (18, 230, (255, 220, 80))
        ]
        for y_offset, width, color in layers:
            lava_rect = pygame.Rect(CALDERA_X_CENTER - width//2, pool_y + y_offset, width, 40 - y_offset)
            screen_lava = camera.apply(lava_rect)
            pygame.draw.rect(surface, color, screen_lava, border_radius=12)
