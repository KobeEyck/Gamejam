"""
Interactive World Zones (Dev 3)
Defines zones for:
1. Lake Siphon Zone (rewards still hover)
2. Concrete Helipad (landing opens shop)
3. Caldera Crater Zone (evaluates water drop accuracy: bullseye vs glancing)
"""
import math
import pygame
from src.settings import (
    LAKE_ZONE_START, LAKE_ZONE_END, LAKE_WATER_LEVEL,
    HELIPAD_X, HELIPAD_WIDTH, HELIPAD_Y,
    CALDERA_X_CENTER, CALDERA_CRATER_WIDTH, CALDERA_Y
)

class LakeZone:
    def __init__(self):
        self.rect = pygame.Rect(LAKE_ZONE_START, LAKE_WATER_LEVEL - 80, LAKE_ZONE_END - LAKE_ZONE_START, 120)

    def is_player_siphoning(self, player) -> tuple[bool, float]:
        """
        Checks if player is low enough over the lake to siphon.
        Returns: (in_zone, stability_multiplier)
        Hovering perfectly still (low speed) yields up to 2.0x faster fill.
        """
        if self.rect.collidepoint(player.pos.x, player.pos.y):
            speed = player.vel.length()
            # Hover stability multiplier: faster if player maintains low speed
            stability = max(1.0, 2.2 - (speed / 80.0))
            return True, stability
        return False, 0.0


class HelipadZone:
    def __init__(self):
        # Generous bounds covering the entire airport runway and approach margins
        self.rect = pygame.Rect(HELIPAD_X - 15, HELIPAD_Y - 45, HELIPAD_WIDTH + 30, 65)

    def is_player_landed(self, player) -> bool:
        """
        Landed if inside airport runway rect, speed is low / taxiing, and craft is reasonably upright.
        """
        if self.rect.collidepoint(player.pos.x, player.pos.y):
            speed = player.vel.length()
            # Allow gentle touchdown or taxiing along the runway
            if speed < 90.0 and -140 < player.angle < -40:
                return True
        return False


class CalderaZone:
    def __init__(self):
        self.center_x = CALDERA_X_CENTER
        self.crater_width = CALDERA_CRATER_WIDTH
        self.y = CALDERA_Y

    def evaluate_payload_hit(self, hit_pos: pygame.Vector2) -> tuple[bool, bool, float]:
        """
        Evaluates water drop hit.
        Returns: (is_hit, is_direct_bullseye, payout_score)
        """
        dist_from_center = abs(hit_pos.x - self.center_x)
        half_width = self.crater_width / 2

        if dist_from_center <= half_width:
            # Direct bullseye in inner 40% of crater
            is_direct = dist_from_center <= (half_width * 0.4)
            # Accuracy multiplier (1.0 in center down to 0.3 on edge)
            accuracy = 1.0 - (dist_from_center / half_width) * 0.7
            return True, is_direct, accuracy
        return False, False, 0.0
