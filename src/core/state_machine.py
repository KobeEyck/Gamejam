"""
Game State Definitions (Dev 4)
Handles the transitions between Menu, In-Game, Helipad Shop, Game Over, and Victory.
"""
from enum import Enum, auto

class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    SHOP = auto()
    GAME_OVER = auto()
    VICTORY = auto()
