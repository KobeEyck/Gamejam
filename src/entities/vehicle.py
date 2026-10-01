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
    description="Agile and lightweight starter helicopter. Low capacity, high maneuverability.",
    base_mass=1.0,
    max_thrust=750.0,
    max_pitch_rate=220.0,
    water_capacity=100.0,
    max_hull=100.0,
    siphon_speed=30.0,
    cost=0
)

WATER_BOMBER = VehicleStats(
    name="Water Bomber",
    description="Fixed-wing high-speed aircraft. High payload, requires momentum.",
    base_mass=2.2,
    max_thrust=1100.0,
    max_pitch_rate=140.0,
    water_capacity=300.0,
    max_hull=150.0,
    siphon_speed=65.0,
    cost=1200
)

HEAVY_DROPSHIP = VehicleStats(
    name="Heavy Dropship",
    description="Dual-rotor armored beast. Massive water capacity, moves like a brick.",
    base_mass=4.5,
    max_thrust=1800.0,
    max_pitch_rate=90.0,
    water_capacity=800.0,
    max_hull=350.0,
    siphon_speed=120.0,
    cost=3500
)
