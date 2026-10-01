"""
Particle System (Dev 2)
Handles water droplets dumped from vehicle, ash storms, thruster exhaust, and impact splashes.
"""
import random
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

    def spawn_water_drop(self, x: float, y: float, vx: float, vy: float, volume: float):
        """Spawns falling water payload."""
        self.water_payloads.append({
            "pos": pygame.Vector2(x, y),
            "vel": pygame.Vector2(vx, vy),
            "volume": volume,
            "alive": True
        })

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
