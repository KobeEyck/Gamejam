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
        
        # Fonts for airport signs and markings
        self.font_small = pygame.font.Font(None, 16)
        self.font_h = pygame.font.Font(None, 24)

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
            # Airstrip, Helipad & Hangar Tarmac Apron (Flat ground from X: 860 to 1420)
            (860, HELIPAD_Y),
            (1420, HELIPAD_Y),
            # Gentle rise
            (1700, 680),
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
            
        lake_poly = [(LAKE_ZONE_START, LAKE_WATER_LEVEL)] + lake_surface_pts + [
            (LAKE_ZONE_END, LAKE_WATER_LEVEL),
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

        # 3. Draw Airstrip, Aircraft Hangar, Low-Profile ATC Post & Runway Lights
        self._draw_airport_facilities(surface, camera)

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

    def _draw_airport_facilities(self, surface: pygame.Surface, camera):
        import time
        import math
        t = time.time()

        # 1. Paved Airstrip / Runway (Runs across X: 870 to 1420 at Y: 698)
        runway_rect = pygame.Rect(870, 697, 550, 7)
        screen_runway = camera.apply(runway_rect)
        pygame.draw.rect(surface, (42, 45, 50), screen_runway)
        pygame.draw.line(surface, (65, 70, 78), screen_runway.topleft, screen_runway.topright, 2)

        # Runway Threshold "Piano Keys" (White bars on left approach threshold: X = 880 to 925)
        for bx in range(880, 925, 6):
            bar_rect = camera.apply(pygame.Rect(bx, 698, 4, 5))
            pygame.draw.rect(surface, (235, 238, 245), bar_rect)

        # Runway Centerline Dashes (- - - from X: 940 to 1400)
        for dx in range(940, 1400, 32):
            dash_rect = camera.apply(pygame.Rect(dx, 699, 18, 3))
            pygame.draw.rect(surface, (230, 232, 238), dash_rect)

        # Yellow taxi line guiding across runway into the helipad center
        taxi_p1 = camera.apply((950, 700))
        taxi_p2 = camera.apply((1040, 700))
        taxi_p3 = camera.apply((1140, 700))
        pygame.draw.lines(surface, (235, 195, 45), False, [taxi_p1, taxi_p2, taxi_p3], 2)

        # 2. Aircraft Hangar (X: 1145 to 1305, Y: 638 to 700)
        hangar_x, hangar_y, hangar_w, hangar_h = 1145, 638, 160, 62
        screen_hangar = camera.apply(pygame.Rect(hangar_x, hangar_y, hangar_w, hangar_h))

        # Hangar outer frame / corrugated metal walls
        pygame.draw.rect(surface, (135, 145, 158), screen_hangar, border_top_left_radius=12, border_top_right_radius=12)
        # Corrugated steel vertical texture seams
        for cx in range(hangar_x + 8, hangar_x + hangar_w, 10):
            p1 = camera.apply((cx, hangar_y + 4))
            p2 = camera.apply((cx, hangar_y + hangar_h))
            pygame.draw.line(surface, (110, 120, 132), p1, p2, 1)

        # Arched roof trim & fascia
        roof_arch = pygame.Rect(hangar_x - 3, hangar_y - 3, hangar_w + 6, 8)
        pygame.draw.rect(surface, (85, 92, 102), camera.apply(roof_arch), border_top_left_radius=6, border_top_right_radius=6)

        # Hangar Bay Door (Open interior bay)
        door_w, door_h = 118, 48
        door_x = hangar_x + (hangar_w - door_w) // 2
        door_y = hangar_y + hangar_h - door_h
        screen_door = camera.apply(pygame.Rect(door_x, door_y, door_w, door_h))

        # Deep interior bay shadow
        pygame.draw.rect(surface, (32, 35, 42), screen_door)
        # Interior steel trusses
        for tx in range(screen_door.left + 15, screen_door.right - 10, 24):
            pygame.draw.line(surface, (55, 60, 72), (tx, screen_door.top), (tx + 12, screen_door.bottom), 2)
            pygame.draw.line(surface, (55, 60, 72), (tx + 12, screen_door.top), (tx, screen_door.bottom), 2)

        # Warm interior floodlight cast
        light_glow = (math.sin(t * 2.0) + 1.0) * 0.08 + 0.92
        lamp_pts = [
            (screen_door.centerx, screen_door.top + 2),
            (screen_door.left + 10, screen_door.bottom),
            (screen_door.right - 10, screen_door.bottom)
        ]
        # Soft yellow interior light cone
        lamp_surf = pygame.Surface((screen_door.w, screen_door.h), pygame.SRCALPHA)
        rel_pts = [(p[0] - screen_door.x, p[1] - screen_door.y) for p in lamp_pts]
        pygame.draw.polygon(lamp_surf, (255, 210, 90, int(45 * light_glow)), rel_pts)
        surface.blit(lamp_surf, screen_door.topleft)

        # Overhead floodlight fixture
        pygame.draw.circle(surface, (255, 230, 150), (screen_door.centerx, screen_door.top + 3), 3)

        # Yellow/Black Hazard chevron warning stripes along hangar threshold
        for hx in range(door_x, door_x + door_w - 6, 8):
            ch_rect = camera.apply(pygame.Rect(hx, 698, 4, 3))
            pygame.draw.rect(surface, (235, 195, 30), ch_rect)

        # Hangar Door frame outline
        pygame.draw.rect(surface, (60, 65, 75), screen_door, 3)

        # Structural steel beam above the bay
        beam_rect = camera.apply(pygame.Rect(door_x + 10, hangar_y + 6, door_w - 20, 4))
        pygame.draw.rect(surface, (75, 82, 92), beam_rect)

        # 3. Compact ATC Flight Operations Post (X: 1090 to 1125, Y: 672 to 700 - height only 28px!)
        post_x, post_y, post_w, post_h = 1090, 672, 35, 28
        screen_post = camera.apply(pygame.Rect(post_x, post_y, post_w, post_h))
        # Post walls
        pygame.draw.rect(surface, (165, 175, 185), screen_post)
        pygame.draw.rect(surface, (60, 65, 72), screen_post, 1)

        # Panoramic Observation Windows (Wrap-around glass)
        post_win = camera.apply(pygame.Rect(post_x + 3, post_y + 5, post_w - 6, 12))
        pygame.draw.rect(surface, (70, 170, 220), post_win)
        pygame.draw.rect(surface, (40, 48, 56), post_win, 1)
        # Window mullion
        pygame.draw.line(surface, (40, 48, 56), (post_win.centerx, post_win.top), (post_win.centerx, post_win.bottom), 1)

        # Post flat roof & lip
        post_roof = camera.apply(pygame.Rect(post_x - 2, post_y - 2, post_w + 4, 4))
        pygame.draw.rect(surface, (55, 60, 68), post_roof)

        # Compact Mini Antenna & Hazard Beacon
        antenna_base = camera.apply((post_x + post_w // 2, post_y - 2))
        antenna_tip = camera.apply((post_x + post_w // 2, post_y - 10))
        pygame.draw.line(surface, (80, 85, 95), antenna_base, antenna_tip, 2)

        beacon_pulse = (math.sin(t * 5.0) + 1.0) / 2.0
        if beacon_pulse > 0.4:
            pygame.draw.circle(surface, (255, 50, 50), antenna_tip, 2)
            halo = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(halo, (255, 50, 50, int(130 * beacon_pulse)), (5, 5), 4)
            surface.blit(halo, (antenna_tip[0] - 5, antenna_tip[1] - 5))

        # 4. Windsock at Runway Threshold (X: 885, Y: 700)
        pole_bottom = camera.apply((885, 700))
        pole_top = camera.apply((885, 664))
        pygame.draw.line(surface, (120, 125, 135), pole_bottom, pole_top, 2)
        pygame.draw.circle(surface, (60, 65, 70), pole_top, 2)

        wind_flutter = math.sin(t * 7.0) * 3.0
        sock_p1 = pole_top
        sock_p2 = (pole_top[0] + 7, pole_top[1] - 1 + wind_flutter * 0.3)
        sock_p3 = (pole_top[0] + 15, pole_top[1] + 1 + wind_flutter * 0.6)
        sock_p4 = (pole_top[0] + 22, pole_top[1] + 3 + wind_flutter)

        pygame.draw.polygon(surface, (245, 100, 25), [
            (sock_p1[0], sock_p1[1] - 4), (sock_p2[0], sock_p2[1] - 3),
            (sock_p2[0], sock_p2[1] + 3), (sock_p1[0], sock_p1[1] + 4)
        ])
        pygame.draw.polygon(surface, (240, 240, 245), [
            (sock_p2[0], sock_p2[1] - 3), (sock_p3[0], sock_p3[1] - 2),
            (sock_p3[0], sock_p3[1] + 2), (sock_p2[0], sock_p2[1] + 3)
        ])
        pygame.draw.polygon(surface, (245, 100, 25), [
            (sock_p3[0], sock_p3[1] - 2), (sock_p4[0], sock_p4[1] - 1),
            (sock_p4[0], sock_p4[1] + 1), (sock_p3[0], sock_p3[1] + 2)
        ])

        # 5. Runway Edge & Approach Lights
        lights = [
            (875, 697, (60, 255, 100)),   # Green approach threshold
            (930, 697, (255, 240, 180)),  # White runway light
            (980, 697, (255, 190, 40)),   # Amber pad light
            (1040, 697, (255, 190, 40)),  # Amber pad light
            (1100, 697, (255, 190, 40)),  # Amber pad light
            (1200, 697, (255, 240, 180)),  # White runway light
            (1300, 697, (255, 240, 180)),  # White runway light
            (1400, 697, (255, 70, 60)),    # Red runway end
        ]
        light_glow = (math.sin(t * 3.0) + 1.0) * 0.15 + 0.70
        for lx, ly, col in lights:
            slight = camera.apply((lx, ly))
            pygame.draw.line(surface, (40, 40, 45), slight, (slight[0], slight[1] + 3), 2)
            glow_c = (
                min(255, max(0, int(col[0] * light_glow))),
                min(255, max(0, int(col[1] * light_glow))),
                min(255, max(0, int(col[2] * light_glow)))
            )
            pygame.draw.circle(surface, glow_c, slight, 3)

        # 6. Ground Equipment: JET-A Fuel Cart & Tool Pallets
        # Fuel cart parked at X: 1130, Y: 686
        tank_rect = camera.apply(pygame.Rect(1128, 686, 14, 12))
        pygame.draw.rect(surface, (235, 235, 240), tank_rect, border_radius=3)
        pygame.draw.line(surface, (220, 45, 45), (tank_rect.x, tank_rect.y + 4), (tank_rect.right, tank_rect.y + 4), 2)
        pygame.draw.circle(surface, (30, 30, 30), (tank_rect.x + 3, tank_rect.bottom), 2)
        pygame.draw.circle(surface, (30, 30, 30), (tank_rect.right - 3, tank_rect.bottom), 2)

        # Staged cargo boxes at X: 1312, Y: 688
        c1 = camera.apply(pygame.Rect(1312, 688, 10, 10))
        c2 = camera.apply(pygame.Rect(1324, 686, 12, 12))
        pygame.draw.rect(surface, (140, 105, 70), c1)
        pygame.draw.rect(surface, (70, 50, 30), c1, 1)
        pygame.draw.rect(surface, (120, 90, 60), c2)
        pygame.draw.rect(surface, (60, 45, 25), c2, 1)
