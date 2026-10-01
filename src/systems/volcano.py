"""
Volcano Core & Threat Escalation System (Dev 2)
Tracks the Instability Meter (0.0 to 1.0), escalates through Threat Levels 1 to 4,
and computes cooling when water payloads hit the caldera.
"""
from src.settings import (
    BASE_HEAT_RATE, 
    THREAT_LEVEL_1_MAX, 
    THREAT_LEVEL_2_MAX, 
    THREAT_LEVEL_3_MAX
)

class VolcanoSystem:
    def __init__(self):
        # 0.0 = completely cool, 1.0 = detonation (game over)
        self.instability: float = 0.15
        self.heat_rate_multiplier: float = 1.0
        
    @property
    def threat_level(self) -> int:
        """
        Returns Threat Level 1 to 4:
        Level 1: 0 - 30% (Clear skies)
        Level 2: 30 - 60% (Lava bombs)
        Level 3: 60 - 85% (Thermal updrafts)
        Level 4: 85 - 100% (Critical Mass / Ash storm / Shake)
        """
        if self.instability < THREAT_LEVEL_1_MAX:
            return 1
        elif self.instability < THREAT_LEVEL_2_MAX:
            return 2
        elif self.instability < THREAT_LEVEL_3_MAX:
            return 3
        else:
            return 4

    @property
    def is_critical(self) -> bool:
        return self.threat_level == 4

    @property
    def has_erupted(self) -> bool:
        return self.instability >= 1.0

    def apply_cooling(self, water_amount: float, direct_hit: bool = True) -> float:
        """
        Reduces instability based on water dropped.
        Direct hits in crater center yield full cooling; glancing hits yield 30%.
        Returns the percentage cooled.
        """
        cooling_factor = 0.0025 if direct_hit else 0.0008
        cooling = water_amount * cooling_factor
        previous = self.instability
        self.instability = max(0.0, self.instability - cooling)
        return previous - self.instability

    def update(self, dt: float):
        """Accelerating countdown to eruption."""
        # Instability accelerates as threat level rises
        acceleration = 1.0 + (self.threat_level * 0.15)
        self.instability += BASE_HEAT_RATE * self.heat_rate_multiplier * acceleration * dt
        self.instability = min(1.0, self.instability)
