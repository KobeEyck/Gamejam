"""
Global Configuration & Constants for Critical Caldera
Shared across all 4 developer modules.
"""
import pygame

# --- Display Settings ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Critical Caldera"

# --- World Dimensions ---
# The world is wider than the screen to allow cross-map ferry runs
WORLD_WIDTH = 5000
WORLD_HEIGHT = 1000

# World Landmarks (X coordinates)
LAKE_ZONE_START = 150
LAKE_ZONE_END = 800
LAKE_WATER_LEVEL = 700

HELIPAD_X = 950
HELIPAD_WIDTH = 180
HELIPAD_Y = 700

CALDERA_X_CENTER = 4200
CALDERA_CRATER_WIDTH = 500
CALDERA_Y = 650

# --- Physics Constants (Tuned for Helicopter Flight Model) ---
GRAVITY = 280.0            # Pixels / sec^2 downwards
AIR_RESISTANCE = 0.955     # Allows smooth forward cruising across the map
ANGULAR_DRAG = 0.80        # Rapid pitch stabilization when keys released
MAX_SPEED = 480.0          # Higher terminal speed cap for fast ferry runs

# --- Colors (Curated Palette) ---
COLOR_SKY_NORMAL = (130, 200, 250)      # Bright daylight blue sky
COLOR_SKY_HAZY = (220, 150, 100)        # Orange/dusty sunset-like sky (volcano ash)
COLOR_SKY_CRITICAL = (180, 60, 40)      # Ominous deep red sky

COLOR_TERRAIN = (110, 160, 80)          # Vibrant green grassy hills
COLOR_TERRAIN_OUTLINE = (60, 100, 40)   # Dark green terrain outline

COLOR_BG_LAYER1 = (140, 190, 220)       # Distant hazy mountains (atmospheric blue)
COLOR_BG_LAYER2 = (120, 175, 155)       # Mid-distance rolling hills

COLOR_LAKE = (40, 140, 220)
COLOR_LAKE_SURFACE = (80, 200, 255)

COLOR_LAVA = (255, 70, 20)
COLOR_LAVA_CORE = (255, 200, 60)

COLOR_HELIPAD = (90, 95, 105)
COLOR_HELIPAD_MARKING = (240, 200, 50)

COLOR_HUD_BG = (15, 15, 25, 200)
COLOR_HUD_TEXT = (240, 240, 250)
COLOR_HEAT_METER_BG = (50, 20, 20)
COLOR_HEAT_METER_FILL = (240, 50, 30)

COLOR_WATER_METER = (50, 160, 255)
COLOR_HULL_METER = (80, 220, 120)

# --- Threat Level Thresholds (Volcano Instability 0.0 - 1.0) ---
THREAT_LEVEL_1_MAX = 0.30
THREAT_LEVEL_2_MAX = 0.60
THREAT_LEVEL_3_MAX = 0.85
# Above 0.85 = Critical Mass

# Base volcano heating rate (% per second) - tuned for ~4-5 minute ferry runs
BASE_HEAT_RATE = 0.0035
