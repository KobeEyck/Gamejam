"""
Player Vehicle & Flight Physics Model (Dev 1)
Implements FPV drone acro physics:
- Momentum, inertia, gravity
- Rotational pitch without auto-leveling
- Thrust vectoring
- Dynamic mass scaling based on water payload (heavy/sluggish when full, twitchy when empty)
"""
import math
import pygame
from src.settings import GRAVITY, AIR_RESISTANCE, ANGULAR_DRAG, WORLD_WIDTH, WORLD_HEIGHT
from src.entities.vehicle import BUCKET_HELI, VehicleStats
from src.entities.water_tank import WaterTank

class Player(pygame.sprite.Sprite):
    def __init__(self, x: float = 950.0, y: float = 650.0, stats: VehicleStats = BUCKET_HELI):
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
        
        # Dimensions for drawing / collisions
        self.width = 44
        self.height = 20

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
        return self.stats.max_thrust * bonus

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
        # 1. Pitch Rotation (Acro style: user changes angular velocity)
        rot_accel = self.pitch_input * self.stats.max_pitch_rate
        self.angular_velocity += rot_accel * dt
        self.angular_velocity *= ANGULAR_DRAG
        self.angle += self.angular_velocity * dt
        
        # Keep angle between -180 and 180
        self.angle = (self.angle + 180) % 360 - 180

        # 2. Thrust Vector Calculation
        rad = math.radians(self.angle)
        # Vector points where aircraft nose is aimed
        forward_dir = pygame.Vector2(math.cos(rad), math.sin(rad))

        if self.is_thrusting:
            thrust_accel = (forward_dir * self.current_thrust_power) / self.total_mass
            self.vel += thrust_accel * dt

        # 3. Gravity & Drag
        gravity_force = pygame.Vector2(0, GRAVITY)
        self.vel += gravity_force * dt
        self.vel *= AIR_RESISTANCE

        # 4. Integrate Position
        self.pos += self.vel * dt

        # 5. Boundaries Clamping
        self.pos.x = max(20, min(self.pos.x, WORLD_WIDTH - 20))
        self.pos.y = max(20, min(self.pos.y, WORLD_HEIGHT - 30))

    def draw(self, surface: pygame.Surface, camera):
        """Renders the player aircraft rotated according to pitch."""
        screen_pos = camera.apply(self.pos)
        
        # Build base polygonal shape of vehicle
        rad = math.radians(self.angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        # Local offsets: nose, left-wing, right-wing, rear
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
            
        # Draw vehicle body
        body_color = (220, 220, 240) if self.water_tank.fill_ratio < 0.5 else (120, 180, 255)
        pygame.draw.polygon(surface, body_color, transformed_points)
        pygame.draw.polygon(surface, (40, 40, 60), transformed_points, 2)
        
        # Draw thruster flame if active
        if self.is_thrusting:
            flame_tail_x = -26 * cos_a + screen_pos[0]
            flame_tail_y = -26 * sin_a + screen_pos[1]
            pygame.draw.line(surface, (255, 180, 50), 
                             (-12 * cos_a + screen_pos[0], -12 * sin_a + screen_pos[1]), 
                             (flame_tail_x, flame_tail_y), 4)
            
        # Draw water tank indicator beneath craft
        if self.water_tank.current_water > 0:
            fill_pct = self.water_tank.fill_ratio
            tank_w = 24
            tank_h = 4
            tank_rect = pygame.Rect(screen_pos[0] - tank_w // 2, screen_pos[1] + 16, tank_w, tank_h)
            pygame.draw.rect(surface, (30, 30, 40), tank_rect)
            fill_rect = pygame.Rect(screen_pos[0] - tank_w // 2, screen_pos[1] + 16, int(tank_w * fill_pct), tank_h)
            pygame.draw.rect(surface, (60, 170, 255), fill_rect)
