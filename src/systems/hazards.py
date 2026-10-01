"""
Environmental Hazards System (Dev 2)
Implements:
1. Parabolic Lava Bombs (Threat Level 2+)
2. Thermal Updraft columns pushing aircraft upward (Threat Level 3+)
"""
import random
import pygame
from src.settings import (
    CALDERA_X_CENTER, 
    CALDERA_Y, 
    GRAVITY, 
    COLOR_LAVA, 
    COLOR_LAVA_CORE
)

class LavaBomb:
    def __init__(self, x: float, y: float, vel: pygame.Vector2):
        self.pos = pygame.Vector2(x, y)
        self.vel = vel
        self.radius = random.uniform(6, 12)
        self.damage = 25.0
        self.alive = True

    def update(self, dt: float):
        self.vel.y += GRAVITY * 0.8 * dt
        self.pos += self.vel * dt
        # Despawn if it falls below the caldera/ground level
        if self.pos.y > CALDERA_Y + 100:
            self.alive = False

    def draw(self, surface: pygame.Surface, camera):
        screen_pos = camera.apply(self.pos)
        pygame.draw.circle(surface, COLOR_LAVA, screen_pos, self.radius)
        pygame.draw.circle(surface, COLOR_LAVA_CORE, screen_pos, self.radius * 0.5)


class ThermalUpdraft:
    def __init__(self, x: float, width: float = 250, force: float = 450.0):
        self.x = x
        self.width = width
        self.force = force  # Upward push in pixels/sec^2

    def check_and_apply(self, player, dt: float):
        """Pushes the player upward if inside the updraft column."""
        if self.x <= player.pos.x <= self.x + self.width:
            upward_force = pygame.Vector2(0, -self.force)
            player.apply_external_force(upward_force, dt)

    def draw(self, surface: pygame.Surface, camera):
        """Draws faint convection currents."""
        rect = pygame.Rect(self.x, 0, self.width, 1000)
        screen_rect = camera.apply(rect)
        # Create subtle translucent overlay
        overlay = pygame.Surface((self.width, 1000), pygame.SRCALPHA)
        overlay.fill((255, 120, 40, 20))
        surface.blit(overlay, screen_rect.topleft)


class HazardManager:
    def __init__(self):
        self.lava_bombs = []
        self.updrafts = [
            ThermalUpdraft(x=3200, width=280, force=450.0),
            ThermalUpdraft(x=3800, width=320, force=550.0),
        ]
        self.spawn_timer = 0.0

    def update(self, dt: float, threat_level: int, player):
        # 1. Update existing Lava Bombs
        for bomb in self.lava_bombs:
            bomb.update(dt)
            # Check collision with player
            if bomb.alive:
                dist = player.pos.distance_to(bomb.pos)
                if dist < (player.width / 2 + bomb.radius):
                    bomb.alive = False
                    player.apply_damage(bomb.damage)
                    # Vaporize 50% water if hit
                    player.water_tank.current_water *= 0.5
                    
        self.lava_bombs = [b for b in self.lava_bombs if b.alive]

        # 2. Spawn Lava Bombs if Threat Level >= 2
        if threat_level >= 2:
            self.spawn_timer += dt
            spawn_interval = 2.5 if threat_level == 2 else (1.4 if threat_level == 3 else 0.7)
            if self.spawn_timer >= spawn_interval:
                self.spawn_timer = 0.0
                # Parabolic ejection from caldera
                spawn_x = CALDERA_X_CENTER + random.uniform(-150, 150)
                vx = random.uniform(-400, 100)
                vy = random.uniform(-750, -500)
                self.lava_bombs.append(LavaBomb(spawn_x, CALDERA_Y - 20, pygame.Vector2(vx, vy)))

        # 3. Apply Updrafts if Threat Level >= 3
        if threat_level >= 3:
            for updraft in self.updrafts:
                updraft.check_and_apply(player, dt)

    def draw(self, surface: pygame.Surface, camera, threat_level: int):
        # Draw updrafts if active
        if threat_level >= 3:
            for updraft in self.updrafts:
                updraft.draw(surface, camera)
                
        # Draw lava bombs
        for bomb in self.lava_bombs:
            bomb.draw(surface, camera)
