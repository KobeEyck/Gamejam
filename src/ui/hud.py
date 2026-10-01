"""
Heads-Up Display / HUD (Dev 4)
Renders:
1. Massive Pulsing Instability Meter at top of screen
2. Threat Level indicator & warning banner
3. Water tank capacity & siphon progress
4. Hull integrity bar
5. Cash display and flight telemetry
"""
import math
import pygame
from src.settings import (
    SCREEN_WIDTH,
    COLOR_HUD_BG,
    COLOR_HUD_TEXT,
    COLOR_HEAT_METER_BG,
    COLOR_HEAT_METER_FILL,
    COLOR_WATER_METER,
    COLOR_HULL_METER
)

class HUD:
    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 34)
        self.alert_font = pygame.font.Font(None, 40)
        self.pulse_timer = 0.0

    def update(self, dt: float):
        self.pulse_timer += dt * 4.0

    def draw(self, surface: pygame.Surface, volcano, player, economy, siphoning: bool, landed: bool):
        # 1. Top Instability Meter (The Core Countdown)
        meter_w = 500
        meter_h = 24
        meter_x = (SCREEN_WIDTH - meter_w) // 2
        meter_y = 20

        # Background bar
        pygame.draw.rect(surface, (20, 20, 30), (meter_x - 4, meter_y - 4, meter_w + 8, meter_h + 8), border_radius=6)
        pygame.draw.rect(surface, COLOR_HEAT_METER_BG, (meter_x, meter_y, meter_w, meter_h), border_radius=4)
        
        # Fill bar
        fill_width = int(meter_w * min(1.0, volcano.instability))
        
        # Dynamic color (glows/pulses red at high threat)
        fill_color = COLOR_HEAT_METER_FILL
        if volcano.is_critical:
            pulse = (math.sin(self.pulse_timer) + 1) * 0.5
            fill_color = (
                int(255 * (0.8 + 0.2 * pulse)),
                int(40 * (1 - pulse)),
                int(30 * (1 - pulse))
            )
            
        pygame.draw.rect(surface, fill_color, (meter_x, meter_y, fill_width, meter_h), border_radius=4)
        pygame.draw.rect(surface, (255, 255, 255), (meter_x, meter_y, meter_w, meter_h), 2, border_radius=4)

        # Heat % text & Threat Level
        heat_pct_text = f"VOLCANO INSTABILITY: {int(volcano.instability * 100)}% (THREAT LVL {volcano.threat_level})"
        heat_surf = self.font.render(heat_pct_text, True, COLOR_HUD_TEXT)
        surface.blit(heat_surf, (meter_x + (meter_w - heat_surf.get_width()) // 2, meter_y + 4))

        # 2. Bottom-Left: Water Payload Tank & Hull
        panel_x = 24
        panel_y = 620
        panel_w = 260
        panel_h = 80
        panel_bg = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_bg.fill(COLOR_HUD_BG)
        surface.blit(panel_bg, (panel_x, panel_y))

        # Hull bar
        hull_ratio = player.hull / player.max_hull if player.max_hull > 0 else 0
        hull_text = self.font.render(f"HULL: {int(player.hull)}/{int(player.max_hull)}", True, (220, 220, 220))
        surface.blit(hull_text, (panel_x + 10, panel_y + 8))
        pygame.draw.rect(surface, (40, 40, 50), (panel_x + 110, panel_y + 10, 135, 12), border_radius=3)
        pygame.draw.rect(surface, COLOR_HULL_METER, (panel_x + 110, panel_y + 10, int(135 * hull_ratio), 12), border_radius=3)

        # Water tank bar
        tank_ratio = player.water_tank.fill_ratio
        water_text = self.font.render(f"WATER: {int(player.water_tank.current_water)}/{int(player.water_tank.capacity)}L", True, (180, 220, 255))
        surface.blit(water_text, (panel_x + 10, panel_y + 36))
        pygame.draw.rect(surface, (20, 40, 60), (panel_x + 110, panel_y + 38, 135, 14), border_radius=3)
        pygame.draw.rect(surface, COLOR_WATER_METER, (panel_x + 110, panel_y + 38, int(135 * tank_ratio), 14), border_radius=3)
        
        # Total mass indicator
        mass_text = self.font.render(f"AIRCRAFT MASS: {player.total_mass:.1f}x", True, (170, 170, 190))
        surface.blit(mass_text, (panel_x + 10, panel_y + 58))

        # 3. Top-Right: Cash Counter
        cash_surf = self.large_font.render(f"${economy.cash}", True, (100, 255, 140))
        surface.blit(cash_surf, (SCREEN_WIDTH - cash_surf.get_width() - 30, 22))

        # 4. Context Prompts (Siphoning, Landing)
        if siphoning:
            siphon_label = self.font.render("PUMP ACTIVE - SIPHONING WATER", True, (120, 240, 255))
            surface.blit(siphon_label, (SCREEN_WIDTH // 2 - siphon_label.get_width() // 2, 70))
        elif landed:
            land_label = self.font.render("LANDED ON HELIPAD - PRESS [E] TO OPEN SHOP / REPAIR", True, (255, 230, 80))
            surface.blit(land_label, (SCREEN_WIDTH // 2 - land_label.get_width() // 2, 70))

        # 5. Critical Mass Warning
        if volcano.is_critical:
            warn_surf = self.alert_font.render("! CRITICAL MASS DETECTED - ERUPTION IMMINENT !", True, (255, 60, 60))
            surface.blit(warn_surf, (SCREEN_WIDTH // 2 - warn_surf.get_width() // 2, 100))
