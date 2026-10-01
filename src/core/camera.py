"""
Camera System (Dev 4)
Handles horizontal and vertical scrolling following the player, 
clamping to the world bounds, and screen shake mechanics.
"""
import random
import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT

class Camera:
    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT):
        self.width = width
        self.height = height
        self.offset_x = 0.0
        self.offset_y = 0.0
        
        # Smooth follow lerp factor (0.0 to 1.0)
        self.lerp_speed = 5.0
        
        # Screen shake
        self.shake_time = 0.0
        self.shake_intensity = 0.0

    def add_shake(self, intensity: float, duration: float):
        """Trigger camera screen shake (e.g. from lava bombs or critical heat)."""
        self.shake_intensity = max(self.shake_intensity, intensity)
        self.shake_time = max(self.shake_time, duration)

    def update(self, target_pos: pygame.Vector2, dt: float):
        """Smoothly lerps the camera towards the target position."""
        target_x = target_pos.x - self.width / 2
        target_y = target_pos.y - self.height / 2
        
        # Smooth interpolation
        self.offset_x += (target_x - self.offset_x) * min(self.lerp_speed * dt, 1.0)
        self.offset_y += (target_y - self.offset_y) * min(self.lerp_speed * dt, 1.0)
        
        # Clamp camera within world boundaries
        self.offset_x = max(0, min(self.offset_x, WORLD_WIDTH - self.width))
        self.offset_y = max(0, min(self.offset_y, WORLD_HEIGHT - self.height))
        
        # Decay screen shake
        if self.shake_time > 0:
            self.shake_time -= dt
            if self.shake_time <= 0:
                self.shake_intensity = 0.0

    def apply(self, world_rect_or_pos):
        """Applies camera offset to a Rect or Vector2 / tuple for rendering."""
        shake_x = 0
        shake_y = 0
        if self.shake_time > 0:
            shake_x = random.uniform(-self.shake_intensity, self.shake_intensity)
            shake_y = random.uniform(-self.shake_intensity, self.shake_intensity)

        if isinstance(world_rect_or_pos, pygame.Rect):
            return world_rect_or_pos.move(-self.offset_x + shake_x, -self.offset_y + shake_y)
        elif isinstance(world_rect_or_pos, (pygame.Vector2, tuple, list)):
            return (
                world_rect_or_pos[0] - self.offset_x + shake_x,
                world_rect_or_pos[1] - self.offset_y + shake_y
            )
        return world_rect_or_pos
