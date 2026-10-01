"""
Main Game Engine & State Orchestrator (Dev 4)
Integrates all systems and coordinates the primary game loop:
- Physics & controls (Dev 1)
- Volcano countdown, hazards & particles (Dev 2)
- Map, water siphoning, caldera scoring & economy (Dev 3)
- Camera tracking, HUD & state machine (Dev 4)
"""
import sys
import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    COLOR_SKY_NORMAL, COLOR_SKY_HAZY, COLOR_SKY_CRITICAL
)
from src.core.state_machine import GameState
from src.core.camera import Camera
from src.entities.player import Player
from src.systems.volcano import VolcanoSystem
from src.systems.hazards import HazardManager
from src.systems.particles import ParticleManager
from src.world.map import WorldMap
from src.systems.economy import EconomySystem
from src.ui.hud import HUD
from src.ui.shop_menu import ShopMenu
from src.ui.main_menu import MainMenu

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU

        # Systems Initialization
        self.camera = Camera()
        self.player = Player()
        self.volcano = VolcanoSystem()
        self.hazard_mgr = HazardManager()
        self.particle_mgr = ParticleManager()
        self.world_map = WorldMap()
        self.economy = EconomySystem(starting_cash=100)
        self.hud = HUD()
        self.shop_menu = ShopMenu()
        self.main_menu = MainMenu()

        # Ephemeral states
        self.is_siphoning = False
        self.is_landed = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if self.state == GameState.MENU:
                action = self.main_menu.handle_event(event)
                if action and action.startswith("PLAY_"):
                    mode = action.split("_")[1]
                    if mode == "NORMAL":
                        self.volcano.heat_rate_multiplier = 1.0
                        self.hazard_mgr.hazard_rate_multiplier = 1.0
                    elif mode == "HARD":
                        self.volcano.heat_rate_multiplier = 1.5
                        self.hazard_mgr.hazard_rate_multiplier = 1.5
                    elif mode == "INSANE":
                        self.volcano.heat_rate_multiplier = 2.5
                        self.hazard_mgr.hazard_rate_multiplier = 2.5
                    self.state = GameState.PLAYING
                elif action == "QUIT":
                    self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.state == GameState.PLAYING:
                    self.running = False

                # Shop toggle when landed on helipad
                elif event.key == pygame.K_h:
                    if self.is_landed and self.state == GameState.PLAYING:
                        self.state = GameState.SHOP
                    elif self.state == GameState.SHOP:
                        self.state = GameState.PLAYING

                # Water Drop Release (Spacebar, S, Down Arrow, or Return)
                elif event.key in (pygame.K_SPACE, pygame.K_s, pygame.K_DOWN, pygame.K_RETURN) and self.state == GameState.PLAYING:
                    if self.player.water_tank.current_water > 0:
                        dropped_vol = self.player.water_tank.dump()
                        # Spawn water payload with forward momentum
                        self.particle_mgr.spawn_water_drop(
                            self.player.pos.x, self.player.pos.y + 10,
                            self.player.vel.x * 0.7, self.player.vel.y * 0.7 + 50.0,
                            dropped_vol
                        )

            # Delegate shop events when in shop
            if self.state == GameState.SHOP:
                if not self.shop_menu.handle_event(event, self.player, self.economy):
                    self.state = GameState.PLAYING

    def update(self, dt: float):
        if self.state == GameState.PLAYING:
            # 1. Update Player Input & Movement
            self.player.handle_input()
            self.player.update(dt)

            # Terrain Collision & Helipad Friction
            ground_y = self.world_map.get_terrain_y(self.player.pos.x)
            if self.player.pos.y >= ground_y - 10:
                self.player.pos.y = ground_y - 10
                
                # Check if above helipad
                helipad_rect = self.world_map.helipad_zone.rect
                on_helipad = (helipad_rect.left <= self.player.pos.x <= helipad_rect.right)
                
                if on_helipad:
                    # Shop pad: No damage, slow down so you don't slide off
                    self.player.vel.x *= 0.85
                    self.player.vel.y *= 0.85
                    if self.player.vel.length() < 30:
                        self.player.angular_velocity *= 0.5
                else:
                    # Normal terrain: Crash damage if speed is high
                    speed = self.player.vel.length()
                    if speed > 60:
                        # Take damage based on impact speed
                        damage = speed * 0.10
                        self.player.apply_damage(damage)
                        # Bounce / slow down
                        self.player.vel.y = -abs(self.player.vel.y) * 0.4
                        self.player.vel.x *= 0.5
                        # Camera shake on heavy impact
                        self.camera.add_shake(min(speed * 0.05, 8.0), 0.2)
                    else:
                        # Scrape against the ground gently
                        self.player.vel *= 0.9

            # 2. Check Lake Siphon Zone
            self.is_siphoning, stability = self.world_map.lake_zone.is_player_siphoning(self.player)
            if self.is_siphoning:
                self.player.water_tank.siphon(dt, stability)

            # 3. Check Helipad Landing
            self.is_landed = self.world_map.helipad_zone.is_player_landed(self.player)

            # 4. Update Volcano & Check Eruption
            self.volcano.update(dt)
            if self.volcano.has_erupted or self.player.hull <= 0:
                self.state = GameState.GAME_OVER

            # 5. Screen shake at Critical Mass
            if self.volcano.is_critical:
                self.camera.add_shake(4.0, 0.2)

            # 6. Environmental Hazards (Lava bombs & Updrafts)
            self.hazard_mgr.update(dt, self.volcano.threat_level, self.player)

            # 7. Falling Water Payload & Terrain/Caldera Collision Detection
            for payload in self.particle_mgr.water_payloads:
                if payload["alive"]:
                    # Check if reached ground at its current X position
                    ground_y = self.world_map.get_terrain_y(payload["pos"].x)
                    if payload["pos"].y >= ground_y:
                        payload["alive"] = False
                        
                        # Evaluate if the hit was inside the caldera
                        is_hit, is_direct, accuracy = self.world_map.caldera_zone.evaluate_payload_hit(payload["pos"])
                        if is_hit:
                            # Cool down the volcano
                            self.volcano.apply_cooling(payload["volume"], direct_hit=is_direct)
                            # Reward cash
                            self.economy.reward_drop(payload["volume"], accuracy, is_direct)

            self.particle_mgr.water_payloads = [p for p in self.particle_mgr.water_payloads if p["alive"]]

            # 8. Particle System
            self.particle_mgr.update(dt, self.volcano.threat_level, self.camera)

            # 9. Camera Follows Player
            self.camera.update(self.player.pos, dt)

            # 10. HUD
            self.hud.update(dt)

    def draw(self):
        if self.state == GameState.MENU:
            self.main_menu.draw(self.screen)
            pygame.display.flip()
            return

        # 1. Dynamic Sky Color according to Threat Level
        threat = self.volcano.threat_level
        if threat == 1:
            sky_color = COLOR_SKY_NORMAL
        elif threat in (2, 3):
            sky_color = COLOR_SKY_HAZY
        else:
            sky_color = COLOR_SKY_CRITICAL
            
        self.screen.fill(sky_color)

        # 2. Draw World Map (Lake, Helipad, Terrain, Caldera)
        self.world_map.draw(self.screen, self.camera)

        # 3. Draw Hazards & Updrafts
        self.hazard_mgr.draw(self.screen, self.camera, threat)

        # 4. Draw Particles & Water Drops
        self.particle_mgr.draw(self.screen, self.camera)

        # 5. Draw Player
        self.player.draw(self.screen, self.camera)

        # 6. Draw HUD
        self.hud.draw(self.screen, self.volcano, self.player, self.economy, self.is_siphoning, self.is_landed)

        # 7. Draw Shop Overlay if open
        if self.state == GameState.SHOP:
            self.shop_menu.draw(self.screen, self.player, self.economy)

        # 8. Draw Game Over Overlay
        elif self.state == GameState.GAME_OVER:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 230) if self.volcano.has_erupted else (50, 10, 10, 220))
            self.screen.blit(overlay, (0, 0))
            
            font = pygame.font.Font(None, 64)
            sub_font = pygame.font.Font(None, 32)
            
            msg = "THE CALDERA DETONATED!" if self.volcano.has_erupted else "VEHICLE DESTROYED!"
            color = (200, 20, 20) if self.volcano.has_erupted else (255, 255, 255)
            
            title = font.render(msg, True, color)
            self.screen.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 280))
            
            sub = sub_font.render("Press ESC to exit.", True, (120, 120, 120))
            self.screen.blit(sub, ((SCREEN_WIDTH - sub.get_width()) // 2, 360))

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            # Guard against large dt spike on lag/window drag
            dt = min(dt, 0.05)
            
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()
