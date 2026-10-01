"""
Water Tank & Payload Management (Dev 1)
Tracks current water weight, filling via siphon, and dumping water drops into the caldera.
"""

class WaterTank:
    def __init__(self, capacity: float = 100.0, siphon_speed: float = 30.0):
        self.capacity = capacity
        self.current_water = 0.0
        self.base_siphon_speed = siphon_speed
        
        # Upgrade multiplier from shop
        self.pump_upgrade_level = 0

    @property
    def fill_ratio(self) -> float:
        return self.current_water / self.capacity if self.capacity > 0 else 0.0

    @property
    def is_full(self) -> bool:
        return self.current_water >= self.capacity

    @property
    def effective_siphon_speed(self) -> float:
        # Each pump upgrade adds 35% speed
        multiplier = 1.0 + (self.pump_upgrade_level * 0.35)
        return self.base_siphon_speed * multiplier

    def siphon(self, dt: float, stability_multiplier: float = 1.0) -> float:
        """
        Fills the tank. Rewarded if player is hovering stably (stability_multiplier > 1.0).
        Returns the amount of water added this tick.
        """
        fill_amount = self.effective_siphon_speed * stability_multiplier * dt
        previous = self.current_water
        self.current_water = min(self.capacity, self.current_water + fill_amount)
        return self.current_water - previous

    def dump(self) -> float:
        """
        Releases the payload.
        Returns the volume of water dumped.
        """
        amount_released = self.current_water
        self.current_water = 0.0
        return amount_released
