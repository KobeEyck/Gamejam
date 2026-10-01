"""
Player Vehicle & Flight Physics Model (Dev 1)
Implements FPV drone acro physics:
- Momentum, inertia, gravity
- Rotational pitch without auto-leveling
- Thrust vectoring
- Dynamic mass scaling based on water payload (heavy/sluggish when full, twitchy when empty)
"""
import os
import random
import math
import pygame
from src.settings import (
    GRAVITY, AIR_RESISTANCE, ANGULAR_DRAG, MAX_SPEED, 
    WORLD_WIDTH, WORLD_HEIGHT, HELIPAD_X, HELIPAD_WIDTH, HELIPAD_Y
)
from src.entities.vehicle import BUCKET_HELI, VehicleStats
from src.entities.water_tank import WaterTank

# Center of helipad shop deck
SHOP_SPAWN_X = HELIPAD_X + (HELIPAD_WIDTH / 2.0)
SHOP_SPAWN_Y = HELIPAD_Y - 30.0

class Player(pygame.sprite.Sprite):
    def __init__(self, x: float = SHOP_SPAWN_X, y: float = SHOP_SPAWN_Y, stats: VehicleStats = BUCKET_HELI):
        super().__init__()
        self.stats = stats
        self.water_tank = WaterTank(stats.water_capacity, stats.siphon_speed)
        
        # Position and motion vectors
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0.0, 0.0)
        self.angle = -90.0  # Facing upward initially in degrees (0 is right, -90 is up)
        self.angular_velocity = 0.0
        
        # Hull / Health
        self.max_hull = stats.max_hull
        self.hull = stats.max_hull
        
        # Upgrade multipliers
        self.thruster_level = 0
        self.shield_level = 0
        
        # Control states
        self.is_thrusting = False
        self.pitch_input = 0.0
        self.facing_right = True
        
        # Sprite loading
        self.sprite = None
        self.load_sprite()

    def load_sprite(self, sprite_name: str = None):
        """Loads or updates the vehicle sprite matching the current stats."""
        name = sprite_name or getattr(self.stats, "sprite_name", "ton.png")
        sprite_path = os.path.join("assets", "sprites", name)
        if os.path.exists(sprite_path):
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            self.width, self.height = self.sprite.get_size()
        else:
            self.sprite = None
            self.width = 54
            self.height = 36

    @property
    def total_mass(self) -> float:
        """
        Base mass + water mass.
        Full water payload increases mass by 35% (noticeable momentum without feeling like lead).
        """
        water_mass_factor = 1.0 + (self.water_tank.fill_ratio * 0.35)
        return self.stats.base_mass * water_mass_factor

    @property
    def current_thrust_power(self) -> float:
        bonus = 1.0 + (self.thruster_level * 0.25)
        # Governor scaling: calm 70% thrust when empty, spooling up to 100% when fully loaded
        load_scaling = 0.70 + (self.water_tank.fill_ratio * 0.30)
        return self.stats.max_thrust * bonus * load_scaling

    def handle_input(self):
        """Polls keyboard input for FPV drone acro controls."""
        keys = pygame.key.get_pressed()
        
        # Throttle (Thrust along vehicle forward vector)
        self.is_thrusting = keys[pygame.K_w] or keys[pygame.K_UP]
        
        # Pitch rotation (Left / Right tilt)
        self.pitch_input = 0.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.pitch_input -= 1.0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.pitch_input += 1.0

    def apply_damage(self, amount: float):
        """Applies damage with heat shield mitigation."""
        shield_reduction = max(0.2, 1.0 - (self.shield_level * 0.20))
        actual_damage = amount * shield_reduction
        self.hull = max(0.0, self.hull - actual_damage)

    def apply_external_force(self, force: pygame.Vector2, dt: float):
        """Applies external forces like thermal updrafts."""
        self.vel += (force / self.total_mass) * dt

    def update(self, dt: float):
        # 1. Pitch Rotation & Auto-Leveling
        # Snappy counter-steering: reset opposite angular momentum when switching direction
        if self.pitch_input != 0.0 and (self.pitch_input * self.angular_velocity < 0):
            self.angular_velocity = 0.0

        rot_accel = self.pitch_input * self.stats.max_pitch_rate
        self.angular_velocity += rot_accel * dt
        self.angular_velocity *= ANGULAR_DRAG
        self.angle += self.angular_velocity * dt

        # Very slow, gentle auto-leveling when player releases pitch keys (holds bank angle smoothly)
        if self.pitch_input == 0.0:
            angle_error = -90.0 - self.angle
            self.angle += angle_error * min(0.8 * dt, 1.0)
            self.angular_velocity *= 0.95

        # Clamp pitch to maximal tilt limit (±25° from upright -90° for realistic helicopter bank)
        MAX_TILT = 25.0
        min_angle = -90.0 - MAX_TILT
        max_angle = -90.0 + MAX_TILT
        if self.angle < min_angle:
            self.angle = min_angle
            self.angular_velocity = 0.0
        elif self.angle > max_angle:
            self.angle = max_angle
            self.angular_velocity = 0.0

        # 2. Thrust Vector Calculation
        rad = math.radians(self.angle)
        # Vector points where aircraft nose is aimed
        forward_dir = pygame.Vector2(math.cos(rad), math.sin(rad))

        if self.is_thrusting:
            thrust_accel = (forward_dir * self.current_thrust_power) / self.total_mass
            # High responsiveness when banked at 25 degrees
            thrust_accel.x *= 2.2
            thrust_accel.y *= 0.85
            self.vel += thrust_accel * dt
        elif self.pitch_input != 0.0:
            # Gentle horizontal-only push when steering without holding throttle (no climb)
            lateral_thrust = (forward_dir.x * self.current_thrust_power * 0.55) / self.total_mass
            self.vel.x += lateral_thrust * dt

        # 3. Gravity & Horizontal Stabilization
        self.vel.y += GRAVITY * dt
        self.vel.y *= max(0.0, 1.0 - 1.8 * dt)  # Vertical air cushioning
        #self.vel.x *= max(0.0, 1.0 - 0.22 * dt) # Low horizontal drag: coasts smoothly without throttle

        # When NOT pressing Left/Right, quickly brake sideways speed to almost nothing
        if self.pitch_input == 0.0:
            self.vel.x *= max(0.0, 1.0 - 1 * dt)
        else:
            self.vel.x *= max(0.0, 1.0 - 0.22 * dt)


        # Terminal velocity clamp for helicopter control
        if abs(self.vel.x) > MAX_SPEED:
            self.vel.x = math.copysign(MAX_SPEED, self.vel.x)
        if self.vel.y > 400.0:
            self.vel.y = 400.0
        elif self.vel.y < -350.0:
            self.vel.y = -350.0

        # 4. Integrate Position
        self.pos += self.vel * dt

        # Update facing orientation based on horizontal velocity
        if self.vel.x > 1:
            self.facing_right = True
        elif self.vel.x < -1:
            self.facing_right = False

        # 5. Boundaries Clamping
        self.pos.x = max(20, min(self.pos.x, WORLD_WIDTH - 20))
        self.pos.y = max(20, min(self.pos.y, WORLD_HEIGHT - 30))

    def draw(self, surface: pygame.Surface, camera):
        """Renders the player as a helicopter with a hanging bucket."""
        screen_pos = camera.apply(self.pos)
        
        rad = math.radians(self.angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        def transform(lx, ly):
            # lx is Roof (+)/Belly (-), ly is Nose (+)/Tail (-)
            rx = lx * cos_a - ly * sin_a + screen_pos[0]
            ry = lx * sin_a + ly * cos_a + screen_pos[1]
            return (rx, ry)


        if self.sprite:
            # Sprite naturally faces right with rotor on top
            base_sprite = self.sprite
            # Consistent tilt: pitches nose down in both flight directions
            tilt = -(self.angle + 90.0)
            if not self.facing_right:
                base_sprite = pygame.transform.flip(self.sprite, True, False)

            # Rotate sprite around center
            rotated_sprite = pygame.transform.rotate(base_sprite, tilt)
            rot_rect = rotated_sprite.get_rect(center=(int(screen_pos[0]), int(screen_pos[1])))
            surface.blit(rotated_sprite, rot_rect)

        else:
            # Fallback polygonal rendering
            rad = math.radians(self.angle)
            cos_a = math.cos(rad)
            sin_a = math.sin(rad)
            
            local_points = [
                (22, 0),    # Nose
                (-16, -10), # Top/Left wing
                (-12, 0),   # Body center indent
                (-16, 10),  # Bottom/Right wing
            ]
            
            transformed_points = []
            for lx, ly in local_points:
                rx = lx * cos_a - ly * sin_a + screen_pos[0]
                ry = lx * sin_a + ly * cos_a + screen_pos[1]
                transformed_points.append((rx, ry))
                
            body_color = (220, 220, 240) if self.water_tank.fill_ratio < 0.5 else (120, 180, 255)
            pygame.draw.polygon(surface, body_color, transformed_points)
            pygame.draw.polygon(surface, (40, 40, 60), transformed_points, 2)
            
            if self.is_thrusting:
                flame_tail_x = -26 * cos_a + screen_pos[0]
                flame_tail_y = -26 * sin_a + screen_pos[1]
                pygame.draw.line(surface, (255, 180, 50), 
                                 (-12 * cos_a + screen_pos[0], -12 * sin_a + screen_pos[1]), 
                                 (flame_tail_x, flame_tail_y), 4)

        # Draw water tank indicator cleanly beneath craft
        if self.water_tank.current_water > 0:
            fill_pct = self.water_tank.fill_ratio
            tank_w = 30
            tank_h = 5
            tank_offset_y = 46
            tank_rect = pygame.Rect(screen_pos[0] - tank_w // 2, screen_pos[1] + tank_offset_y, tank_w, tank_h)
            pygame.draw.rect(surface, (20, 25, 35), tank_rect, border_radius=2)
            fill_rect = pygame.Rect(screen_pos[0] - tank_w // 2, screen_pos[1] + tank_offset_y, int(tank_w * fill_pct), tank_h)
            pygame.draw.rect(surface, (60, 185, 255), fill_rect, border_radius=2)
            pygame.draw.rect(surface, (80, 120, 160), tank_rect, 1, border_radius=2)
