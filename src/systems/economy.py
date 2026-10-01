"""
Economy & Upgrades System (Dev 3)
Tracks player currency, computes rewards for water delivery accuracy,
and processes upgrades/purchases.
"""
from src.entities.vehicle import BUCKET_HELI, WATER_BOMBER, HEAVY_DROPSHIP, VehicleStats

class EconomySystem:
    def __init__(self, starting_cash: int = 0):
        self.cash = starting_cash
        self.total_delivered_water = 0.0

    def reward_drop(self, volume: float, accuracy: float, direct_hit: bool) -> int:
        """
        Calculates cash payout:
        Base pay = volume * 2.0
        Multiplier = accuracy * (1.5 if direct_hit else 1.0)
        """
        bonus_mult = 1.6 if direct_hit else 1.0
        payout = int(volume * 2.2 * accuracy * bonus_mult)
        self.cash += payout
        self.total_delivered_water += volume
        return payout

    def can_afford(self, amount: int) -> bool:
        return self.cash >= amount

    def spend(self, amount: int) -> bool:
        if self.can_afford(amount):
            self.cash -= amount
            return True
        return False
