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
    sprite_name: str             # Asset filename in assets/sprites/

# Vehicle presets
BUCKET_HELI = VehicleStats(
    name="Bucket Heli",
    description="Slow, low capacity, but highly maneuverable. Good for learning the physics.",
    base_mass=1.0,
    max_thrust=750.0,
    max_pitch_rate=360.0,
    water_capacity=150.0,
    max_hull=100.0,
    siphon_speed=30.0,
    cost=0,
    sprite_name="ton.png"
)

WATER_BOMBER = VehicleStats(
    name="Water Bomber",
    description="Emergency rescue helicopter. Fast twin-turbine climb with high water capacity and strong cruising speed.",
    base_mass=1.5,
    max_thrust=1500.0,
    max_pitch_rate=350.0,
    water_capacity=300.0,
    max_hull=150.0,
    siphon_speed=65.0,
    cost=1200,
    sprite_name="helicopter.png"
)

HEAVY_DROPSHIP = VehicleStats(
    name="Heavy Dropship",
    description="Dual-rotor sci-fi craft. Massive water capacity and heavy armor to tank lava rocks, backed by immense turboshaft power.",
    base_mass=2.6,
    max_thrust=3000.0,
    max_pitch_rate=300.0,
    water_capacity=600.0,
    max_hull=350.0,
    siphon_speed=120.0,
    cost=3500,
    sprite_name="Airlane.png"
)
