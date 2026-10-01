"""
Vehicle Archetypes and Upgrade Specifications (Dev 1)
Defines vehicle classes (Starter Bucket Heli, Water Bomber, Heavy Dropship)
and their progression statistics.
"""
from dataclasses import dataclass

@dataclass
class VehicleStats:
    name: str
    description: str
    base_mass: float             # kg equivalent (determines responsiveness)
    max_thrust: float            # Max acceleration force
    max_pitch_rate: float        # Deg/sec rotational agility
    water_capacity: float        # Liters / gallons
    max_hull: float              # Health
    siphon_speed: float          # Water fill rate / sec
    cost: int                    # Price in shop (0 for starter)

# Vehicle presets
BUCKET_HELI = VehicleStats(
    name="Bucket Heli",
    description="Slow, low capacity, but highly maneuverable. Good for learning the physics.",
    base_mass=1.0,
    max_thrust=720.0,
    max_pitch_rate=360.0,
    water_capacity=50.0,
    max_hull=100.0,
    siphon_speed=30.0,
    cost=0
)

WATER_BOMBER = VehicleStats(
    name="Water Bomber",
    description="Fixed-wing aircraft. Cannot hover. Must skim the lake at high speeds to scoop water and perform intense dive-bomb maneuvers over the crater. Carries massive payloads but requires a long turning radius.",
    base_mass=2.0,
    max_thrust=1100.0,
    max_pitch_rate=180.0,
    water_capacity=300.0,
    max_hull=150.0,
    siphon_speed=65.0,
    cost=1200
)

HEAVY_DROPSHIP = VehicleStats(
    name="Heavy Dropship",
    description="Dual-rotor sci-fi craft. Massive water capacity and heavy armor to tank lava rocks but moves like a brick.",
    base_mass=3.8,
    max_thrust=1850.0,
    max_pitch_rate=130.0,
    water_capacity=800.0,
    max_hull=350.0,
    siphon_speed=120.0,
    cost=3500
)
