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

# --- Physics Constants ---
GRAVITY = 350.0            # Pixels / sec^2 downwards
AIR_RESISTANCE = 0.985     # Velocity damping per frame
ANGULAR_DRAG = 0.92        # Pitch rotation damping

# --- Colors (Curated Palette) ---
COLOR_SKY_NORMAL = (24, 28, 44)
COLOR_SKY_HAZY = (60, 32, 28)
COLOR_SKY_CRITICAL = (35, 12, 16)

COLOR_TERRAIN = (45, 42, 50)
COLOR_TERRAIN_OUTLINE = (75, 70, 85)

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
