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

        # 1. Draw Helicopter Body
        heli_body = [
            transform(-5, 18),   # Lower nose
            transform(5, 18),    # Upper nose
            transform(10, 8),    # Cockpit top
            transform(10, -8),   # Engine top
            transform(2, -12),   # Upper tail base
            transform(2, -35),   # Tail end top
            transform(-2, -35),  # Tail end bottom
            transform(-2, -12),  # Lower tail base
            transform(-8, -5),   # Belly rear
            transform(-8, 8),    # Belly front
        ]
        
        body_color = (220, 60, 50) if self.water_tank.fill_ratio < 0.5 else (180, 40, 30)
        pygame.draw.polygon(surface, body_color, heli_body)
        pygame.draw.polygon(surface, (40, 40, 40), heli_body, 2)
        
        # Cockpit window
        window = [
            transform(5, 17),
            transform(9, 8),
            transform(3, 8),
            transform(-1, 17),
        ]
        pygame.draw.polygon(surface, (150, 220, 255), window)
        
        # Skids (Landing gear)
        pygame.draw.line(surface, (100, 100, 100), transform(-8, 6), transform(-14, 6), 2)
        pygame.draw.line(surface, (100, 100, 100), transform(-8, -6), transform(-14, -6), 2)
        pygame.draw.line(surface, (150, 150, 150), transform(-14, 12), transform(-14, -12), 3)

        # Main Rotor
        pygame.draw.line(surface, (80, 80, 80), transform(10, -2), transform(16, -2), 3) # Mast
        import time
        blade_span = 24 if not self.is_thrusting else 24 * abs(math.cos(time.time() * 30))
        pygame.draw.line(surface, (200, 200, 200), transform(16, -blade_span), transform(16, blade_span), 2)
        
        # Tail Rotor
        tail_span = 8 * abs(math.cos(time.time() * 30)) if self.is_thrusting else 8
        pygame.draw.line(surface, (180, 180, 180), transform(0, -35), transform(tail_span, -35), 2)
        pygame.draw.line(surface, (180, 180, 180), transform(0, -35), transform(-tail_span, -35), 2)

        # 2. Draw Hanging Water Bucket
        # Attachment point at belly center
        attach_x, attach_y = transform(-8, 0)
        bucket_y_top = attach_y + 35
        
        # Draw cable
        pygame.draw.line(surface, (80, 80, 80), (attach_x, attach_y), (attach_x, bucket_y_top), 2)
        
        # Bucket dimensions
        bw_top = 12
        bw_bot = 8
        bh = 18
        
        bucket_pts = [
            (attach_x - bw_top, bucket_y_top),
            (attach_x + bw_top, bucket_y_top),
            (attach_x + bw_bot, bucket_y_top + bh),
            (attach_x - bw_bot, bucket_y_top + bh)
        ]
        
        # Draw Water inside bucket
        fill = self.water_tank.fill_ratio
        if fill > 0:
            w_h = bh * fill
            w_y = bucket_y_top + bh - w_h
            w_top_half = bw_bot + (bw_top - bw_bot) * fill
            water_pts = [
                (attach_x - w_top_half, w_y),
                (attach_x + w_top_half, w_y),
                (attach_x + bw_bot, bucket_y_top + bh),
                (attach_x - bw_bot, bucket_y_top + bh)
            ]
            pygame.draw.polygon(surface, (60, 170, 255), water_pts)
            
        # Draw Bucket Outline
        pygame.draw.polygon(surface, (200, 100, 30), bucket_pts, 2)
