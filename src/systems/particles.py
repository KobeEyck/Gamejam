"""
Particle System (Dev 2)
Handles water droplets dumped from vehicle, ash storms, thruster exhaust, and impact splashes.
"""
import random
import math
import pygame

class Particle:
    def __init__(self, x: float, y: float, vx: float, vy: float, color: tuple, size: float, life: float):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(vx, vy)
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life

    def update(self, dt: float) -> bool:
        self.pos += self.vel * dt
        self.life -= dt
        return self.life > 0

    def draw(self, surface: pygame.Surface, camera):
        screen_pos = camera.apply(self.pos)
        alpha_factor = max(0.0, self.life / self.max_life)
        curr_size = max(1.0, self.size * alpha_factor)
        pygame.draw.circle(surface, self.color, screen_pos, curr_size)


class ParticleManager:
    def __init__(self):
        self.particles = []
        self.water_payloads = []  # Physical water clumps dropping to caldera
        self.exhaust_timer = 0.0

    def spawn_water_drop(self, x: float, y: float, vx: float, vy: float, volume: float):
        """Spawns falling water payload."""
        self.water_payloads.append({
            "pos": pygame.Vector2(x, y),
            "vel": pygame.Vector2(vx, vy),
            "volume": volume,
            "alive": True
        })

    def spawn_exhaust(self, player, dt: float):
        """Spawns engine gas and smoke based on flight speed and hull condition."""
        self.exhaust_timer -= dt
        hull_ratio = player.hull / player.max_hull if player.max_hull > 0 else 0.0
        is_moving = player.vel.length_squared() > 10000.0
        is_damaged = hull_ratio < 0.35

        if not (player.is_thrusting or is_moving or is_damaged) or self.exhaust_timer > 0:
            return

        self.exhaust_timer = 0.035 if player.is_thrusting else 0.08
        angle = math.radians(player.angle)
        forward = pygame.Vector2(math.cos(angle), math.sin(angle))
        # The sprite is mirrored when flying left, so mirror the tail position too.
        tail_offset = pygame.Vector2(0, -36 if player.facing_right else 36)
        tail_direction = pygame.Vector2(
            tail_offset.x * math.cos(angle) - tail_offset.y * math.sin(angle),
            tail_offset.x * math.sin(angle) + tail_offset.y * math.cos(angle)
        ).normalize()
        exhaust_pos = player.pos + tail_direction
        exhaust_velocity = player.vel * 0.15 + tail_direction * random.uniform(20, 50)

        if player.is_thrusting:
            self.particles.append(Particle(
                exhaust_pos.x, exhaust_pos.y,
                exhaust_velocity.x + random.uniform(-12, 12),
                exhaust_velocity.y + random.uniform(-12, 12),
                random.choice([(210, 225, 235), (175, 205, 220), (235, 235, 225)]),
                random.uniform(2.0, 4.0),
                random.uniform(0.25, 0.45)
            ))

        if player.is_thrusting or is_damaged:
            smoke_size = random.uniform(4.0, 7.0) if is_damaged else random.uniform(2.5, 5.0)
            smoke_life = random.uniform(0.8, 1.3) if is_damaged else random.uniform(0.5, 0.9)
            self.particles.append(Particle(
                exhaust_pos.x + random.uniform(-4, 4),
                exhaust_pos.y + random.uniform(-4, 4),
                exhaust_velocity.x + random.uniform(-18, 18),
                exhaust_velocity.y + random.uniform(-18, 18) - 10,
                random.choice([(75, 75, 80), (95, 95, 100), (115, 110, 105)]),
                smoke_size,
                smoke_life
            ))

        if len(self.particles) > 500:
            self.particles = self.particles[-500:]

    def update(self, dt: float, threat_level: int, camera):
        # 1. Update general particles
        self.particles = [p for p in self.particles if p.update(dt)]

        # 2. Update falling water droplets
        for w in self.water_payloads:
            w["vel"].y += 450.0 * dt  # Water gravity
            w["pos"] += w["vel"] * dt
            # Spawn mist trail
            if random.random() < 0.4:
                self.particles.append(Particle(
                    w["pos"].x, w["pos"].y,
                    random.uniform(-10, 10), random.uniform(-20, 20),
                    (100, 180, 255), random.uniform(2, 4), 0.4
                ))

        # 3. Ash storm particles during Critical Mass (Threat Level 4)
        if threat_level == 4:
            for _ in range(3):
                # Spawn ash relative to camera view
                ash_x = camera.offset_x + random.uniform(0, camera.width)
                ash_y = camera.offset_y + random.uniform(0, camera.height)
                self.particles.append(Particle(
                    ash_x, ash_y,
                    random.uniform(-150, -40), random.uniform(30, 80),
                    (160, 150, 140), random.uniform(2, 5), random.uniform(1.0, 2.5)
                ))

    def draw(self, surface: pygame.Surface, camera):
        for p in self.particles:
            p.draw(surface, camera)
            
        for w in self.water_payloads:
            screen_pos = camera.apply(w["pos"])
            size = min(18, max(5, int(w["volume"] * 0.15)))
            pygame.draw.circle(surface, (60, 170, 255), screen_pos, size)
            pygame.draw.circle(surface, (180, 230, 255), screen_pos, size * 0.5)
