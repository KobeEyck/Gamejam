"""
Helipad Upgrade & Fleet Shop (Dev 3)
Allows player to spend earned cash to buy upgrades or unlock new aircraft archetypes.
"""
import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.entities.vehicle import WATER_BOMBER, HEAVY_DROPSHIP

class ShopMenu:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 48)
        self.item_font = pygame.font.Font(None, 28)
        self.hint_font = pygame.font.Font(None, 24)
        self.message = ""

    def handle_event(self, event, player, economy) -> bool:
        """
        Handles key inputs while in shop.
        Returns False if player exits shop, True if staying in shop.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_e):
                return False  # Close shop
                
            # 1: Repair Hull ($50)
            elif event.key == pygame.K_1:
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
            elif event.key == pygame.K_2:
                cost = 150 * (player.water_tank.pump_upgrade_level + 1)
                if economy.spend(cost):
                    player.water_tank.pump_upgrade_level += 1
                    self.message = f"Pump upgraded to Lvl {player.water_tank.pump_upgrade_level}!"
                else:
                    self.message = "Not enough cash!"

            # 3: Reinforced Heat Shielding ($200)
            elif event.key == pygame.K_3:
                cost = 200 * (player.shield_level + 1)
                if economy.spend(cost):
                    player.shield_level += 1
                    self.message = f"Heat Shielding upgraded to Lvl {player.shield_level}!"
                else:
                    self.message = "Not enough cash!"

            # 4: Overclocked Thrusters ($250)
            elif event.key == pygame.K_4:
                cost = 250 * (player.thruster_level + 1)
                if economy.spend(cost):
                    player.thruster_level += 1
                    self.message = f"Thrusters overclocked to Lvl {player.thruster_level}!"
                else:
                    self.message = "Not enough cash!"

            # 5: Buy Water Bomber ($1200)
            elif event.key == pygame.K_5:
                if economy.spend(WATER_BOMBER.cost):
                    player.stats = WATER_BOMBER
                    player.max_hull = WATER_BOMBER.max_hull
                    player.hull = WATER_BOMBER.max_hull
                    player.water_tank.capacity = WATER_BOMBER.water_capacity
                    player.water_tank.base_siphon_speed = WATER_BOMBER.siphon_speed
                    self.message = "Equipped Water Bomber!"
                else:
                    self.message = "Not enough cash for Water Bomber!"

            # 6: Buy Heavy Dropship ($3500)
            elif event.key == pygame.K_6:
                if economy.spend(HEAVY_DROPSHIP.cost):
                    player.stats = HEAVY_DROPSHIP
                    player.max_hull = HEAVY_DROPSHIP.max_hull
                    player.hull = HEAVY_DROPSHIP.max_hull
                    player.water_tank.capacity = HEAVY_DROPSHIP.water_capacity
                    player.water_tank.base_siphon_speed = HEAVY_DROPSHIP.siphon_speed
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
            f"[5] Aircraft: Water Bomber (${WATER_BOMBER.cost}) - Fixed-wing high payload",
            f"[6] Aircraft: Heavy Dropship (${HEAVY_DROPSHIP.cost}) - Dual-rotor massive tank",
        ]

        start_y = 180
        for i, item_text in enumerate(items):
            surf = self.item_font.render(item_text, True, (230, 230, 240))
            surface.blit(surf, (280, start_y + (i * 45)))

        # Feedback message
        if self.message:
            msg_surf = self.item_font.render(self.message, True, (255, 230, 100))
            surface.blit(msg_surf, ((SCREEN_WIDTH - msg_surf.get_width()) // 2, 480))

        # Exit instruction
        exit_surf = self.hint_font.render("Press [E] or [ESC] to return to flight.", True, (160, 160, 180))
        surface.blit(exit_surf, ((SCREEN_WIDTH - exit_surf.get_width()) // 2, 540))
