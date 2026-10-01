"""
Helipad Upgrade & Fleet Shop (Dev 3)
Allows player to spend earned cash to buy upgrades or unlock new aircraft archetypes.
"""
import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.entities.vehicle import BUCKET_HELI, WATER_BOMBER, HEAVY_DROPSHIP

class ShopMenu:
    def __init__(self):
        if not pygame.get_init():
            pygame.init()
        pygame.font.init()

        self.title_font = pygame.font.Font(None, 48)
        self.item_font = pygame.font.Font(None, 28)
        self.hint_font = pygame.font.Font(None, 24)
        self.message = ""

    def _apply_vehicle(self, player, vehicle):
        player.stats = vehicle
        player.max_hull = vehicle.max_hull
        player.hull = vehicle.max_hull
        player.water_tank.capacity = vehicle.water_capacity
        player.water_tank.current_water = min(player.water_tank.current_water, vehicle.water_capacity)
        player.water_tank.base_siphon_speed = vehicle.siphon_speed

    def handle_event(self, event, player, economy) -> bool:
        """
        Handles key inputs while in shop.
        Returns False if player exits shop, True if staying in shop.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_e):
                return False  # Close shop

            # 1: Repair Hull ($50)
            elif event.key in (pygame.K_1, pygame.K_KP1):
                cost = 50
                if player.hull < player.max_hull:
                    if economy.spend(cost):
                        player.hull = player.max_hull
                        self.message = "Hull fully repaired!"
                    else:
                        self.message = "Not enough cash!"
                else:
                    self.message = "Hull is already at 100%!"

            # 2: Upgrade Intake Pumps ($150)
            elif event.key in (pygame.K_2, pygame.K_KP2):
                cost = 150 * (player.water_tank.pump_upgrade_level + 1)
                if economy.spend(cost):
                    player.water_tank.pump_upgrade_level += 1
                    self.message = f"Pump upgraded to Lvl {player.water_tank.pump_upgrade_level}!"
                else:
                    self.message = "Not enough cash!"

            # 3: Reinforced Heat Shielding ($200)
            elif event.key in (pygame.K_3, pygame.K_KP3):
                cost = 200 * (player.shield_level + 1)
                if economy.spend(cost):
                    player.shield_level += 1
                    self.message = f"Heat Shielding upgraded to Lvl {player.shield_level}!"
                else:
                    self.message = "Not enough cash!"

            # 4: Overclocked Thrusters ($250)
            elif event.key in (pygame.K_4, pygame.K_KP4):
                cost = 250 * (player.thruster_level + 1)
                if economy.spend(cost):
                    player.thruster_level += 1
                    self.message = f"Thrusters overclocked to Lvl {player.thruster_level}!"
                else:
                    self.message = "Not enough cash!"

            # 5: Buy starter Bucket Heli ($0)
            elif event.key in (pygame.K_5, pygame.K_KP5):
                if player.stats.name == BUCKET_HELI.name:
                    self.message = "You are already flying the Bucket Heli."
                elif economy.spend(BUCKET_HELI.cost):
                    self._apply_vehicle(player, BUCKET_HELI)
                    self.message = "Equipped Bucket Heli!"
                else:
                    self.message = "Not enough cash for Bucket Heli!"

            # 6: Buy Water Bomber ($1200)
            elif event.key in (pygame.K_6, pygame.K_KP6):
                if player.stats.name == WATER_BOMBER.name:
                    self.message = "You are already flying the Water Bomber."
                elif economy.spend(WATER_BOMBER.cost):
                    self._apply_vehicle(player, WATER_BOMBER)
                    self.message = "Equipped Water Bomber!"
                else:
                    self.message = "Not enough cash for Water Bomber!"

            # 7: Buy Heavy Dropship ($3500)
            elif event.key in (pygame.K_7, pygame.K_KP7):
                if player.stats.name == HEAVY_DROPSHIP.name:
                    self.message = "You are already flying the Heavy Dropship."
                elif economy.spend(HEAVY_DROPSHIP.cost):
                    self._apply_vehicle(player, HEAVY_DROPSHIP)
                    self.message = "Equipped Heavy Dropship!"
                else:
                    self.message = "Not enough cash for Heavy Dropship!"

        return True

    def draw(self, surface: pygame.Surface, player, economy):
        # Translucent backdrop
        backdrop = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        backdrop.fill((10, 12, 20, 220))
        surface.blit(backdrop, (0, 0))

        # Title
        title = self.title_font.render("BASE HELIPAD - UPGRADE DECK", True, (255, 215, 60))
        surface.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 70))

        # Current Funds
        cash_surf = self.item_font.render(f"Available Balance: ${economy.cash}", True, (100, 255, 140))
        surface.blit(cash_surf, ((SCREEN_WIDTH - cash_surf.get_width()) // 2, 120))

        # Shop Items list
        pump_cost = 150 * (player.water_tank.pump_upgrade_level + 1)
        shield_cost = 200 * (player.shield_level + 1)
        thrust_cost = 250 * (player.thruster_level + 1)

        items = [
            f"[1] Field Repair Hull ($50) - Current: {int(player.hull)}/{int(player.max_hull)}",
            f"[2] Intake Pumps Lvl {player.water_tank.pump_upgrade_level + 1} (${pump_cost}) - Faster lake siphoning",
            f"[3] Heat Shielding Lvl {player.shield_level + 1} (${shield_cost}) - Reduces lava bomb damage",
            f"[4] Overclock Thrusters Lvl {player.thruster_level + 1} (${thrust_cost}) - Fights updrafts & climbs faster",
            f"[5] Aircraft: Bucket Heli (${BUCKET_HELI.cost}) - Slow, low capacity, highly maneuverable. Good for learning the physics.",
            f"[6] Aircraft: Water Bomber (${WATER_BOMBER.cost}) - Fixed-wing. Cannot hover. Must skim the lake at high speeds to scoop water and perform intense dive-bomb maneuvers over the crater.",
            f"[7] Aircraft: Heavy Dropship (${HEAVY_DROPSHIP.cost}) - Dual-rotor sci-fi craft. Massive water capacity and heavy armor, but moves like a brick.",
        ]

        start_y = 180
        for i, item_text in enumerate(items):
            surf = self.item_font.render(item_text, True, (230, 230, 240))
            surface.blit(surf, (180, start_y + (i * 38)))

        # Feedback message
        if self.message:
            msg_surf = self.item_font.render(self.message, True, (255, 230, 100))
            surface.blit(msg_surf, ((SCREEN_WIDTH - msg_surf.get_width()) // 2, 480))

        # Exit instruction
        exit_surf = self.hint_font.render("Press [E], [H] or [ESC] to return to flight.", True, (160, 160, 180))
        surface.blit(exit_surf, ((SCREEN_WIDTH - exit_surf.get_width()) // 2, 540))
