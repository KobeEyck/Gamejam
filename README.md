# Critical Caldera 🌋

A 2D Physics-Survival / Action-Logistics game built with Pygame for the Gamejam.

---

## 🎮 Flight Controls

- **Pitch Rotation**: `A` / `D` or `Left` / `Right` (FPV drone acro mode — no auto-leveling!)
- **Thruster / Throttle**: `W`, `Up Arrow`, or `Spacebar` (Accelerates in the direction the nose is pointed)
- **Drop Water Payload**: `S`, `Down Arrow`, or `Enter`
- **Shop / Upgrades**: Land gently on the Helipad and press `E`
- **Exit**: `Esc`

---

## 👥 4-Developer Team Architecture & File Ownership

To work concurrently without git merge conflicts, each developer works inside their dedicated folder:

### 🚁 Developer 1: Flight Physics & Vehicles
- **Folder**: [`src/entities/`](file:///src/entities/)
- **Files**:
  - [`player.py`](file:///src/entities/player.py) — FPV flight physics, momentum, inertia, gravity, dynamic mass calculation (doubles mass when full of water).
  - [`vehicle.py`](file:///src/entities/vehicle.py) — Aircraft stats & archetypes (Bucket Heli, Water Bomber, Heavy Dropship).
  - [`water_tank.py`](file:///src/entities/water_tank.py) — Water capacity, siphon mechanics, dumping.

### 🌋 Developer 2: Volcano System & Environmental Hazards
- **Folder**: [`src/systems/`](file:///src/systems/)
- **Files**:
  - [`volcano.py`](file:///src/systems/volcano.py) — Instability Meter (0–100%), cooling calculations, Threat Levels 1 to 4.
  - [`hazards.py`](file:///src/systems/hazards.py) — Parabolic Lava Bombs (Threat Lvl 2+), Thermal Updraft columns (Threat Lvl 3+).
  - [`particles.py`](file:///src/systems/particles.py) — Water drops, mist trails, ash storm particles (Threat Lvl 4 Critical Mass).

### 🗺️ Developer 3: World, Logistics & Economy/Shop
- **Folder**: [`src/world/`](file:///src/world/) & [`src/ui/shop_menu.py`](file:///src/ui/shop_menu.py)
- **Files**:
  - [`map.py`](file:///src/world/map.py) — Terrain contour, Lake on left, Helipad, glowing Caldera crater on right.
  - [`zones.py`](file:///src/world/zones.py) — Lake hovering detection (stability bonus), helipad landing detection, caldera drop precision scoring.
  - [`economy.py`](file:///src/systems/economy.py) — Cash balance, drop rewards, upgrade purchasing.
  - [`shop_menu.py`](file:///src/ui/shop_menu.py) — Upgrade menu for pumps, heat shields, thrusters, and new aircraft.

### 🖥️ Developer 4: Core Engine, Camera & HUD
- **Folder**: [`src/core/`](file:///src/core/), [`src/ui/hud.py`](file:///src/ui/hud.py), [`main.py`](file:///main.py)
- **Files**:
  - [`game.py`](file:///src/core/game.py) — Main game loop, delta time (`dt`), subsystem coordinator.
  - [`camera.py`](file:///src/core/camera.py) — Horizontal/vertical tracking camera with screen shake.
  - [`hud.py`](file:///src/ui/hud.py) — Pulsing Instability Meter bar, water tank gauge, hull bar, cash counter, warning alerts.
  - [`settings.py`](file:///src/settings.py) — Shared constants, screen size, world bounds, physics constants, colors.

---

## 🌿 Recommended Git Workflow

1. **Branch per developer**:
   - `git checkout -b dev1/flight-physics`
   - `git checkout -b dev2/volcano-hazards`
   - `git checkout -b dev3/world-economy`
   - `git checkout -b dev4/core-hud`
2. **Pull request / Merge**:
   - Because file boundaries are strictly separated, merging into `main` will be smooth and conflict-free!