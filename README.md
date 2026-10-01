# 🎮 Gamejam Project

Welcome to the team Gamejam repository! This project is built using Python and [Pygame](https://www.pygame.org/).

Follow this guide to get the game running on your machine. No deep programming knowledge is required!

---

## 📌 1. Prerequisites (Do this once)

Before starting, make sure you have **Python 3.10+** installed:

1. Download Python from [python.org/downloads](https://www.python.org/downloads/).
2. ⚠️ **VERY IMPORTANT (Windows)**: When running the installer, make sure to check the box at the bottom that says **"Add python.exe to PATH"** before clicking Install.

---


## 💻 2. Manual Setup (Terminal)

If you prefer using the terminal or want to run commands manually, follow these steps:

### Step 1: Open Terminal in the project folder
- **Windows**: In File Explorer, navigate to this project folder, click in the address bar, type `cmd` (or `powershell`), and press **Enter**.
- **VS Code**: Press <kbd>Ctrl</kbd> + <kbd>`</kbd> (or `Terminal` > `New Terminal` in the top menu).

### Step 2: Create a Virtual Environment (`.venv`)
A virtual environment keeps all libraries isolated inside this project so they don't interfere with your computer.

- **Windows**:
  ```bat
  python -m venv .venv
  ```
  *(If `python` doesn't work, try `py -m venv .venv`)*

- **macOS / Linux**:
  ```bash
  python3 -m venv .venv
  ```

### Step 3: Activate the Virtual Environment
You should see `(.venv)` appear at the beginning of your terminal prompt line.

- **Windows (Command Prompt / CMD)**:
  ```bat
  .venv\Scripts\activate.bat
  ```

- **Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

- **macOS / Linux**:
  ```bash
  source .venv/bin/activate
  ```

### Step 4: Install Dependencies
Install Pygame and any other required libraries listed in [`requirements.txt`](file:///requirements.txt):
```bash
pip install -r requirements.txt
```

### Step 5: Run the Game
```bash
python main.py
```
*(You should see a window pop up showing that Pygame is working!)*

---

## 🧑‍💻 3. Working with VS Code

If your team is using [Visual Studio Code](https://code.visualstudio.com/):

1. Open the project folder in VS Code (`File` > `Open Folder...`).
2. Open [`main.py`](file:///main.py).
3. Select the Python interpreter:
   - Press <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> (or <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> on Mac).
   - Type **`Python: Select Interpreter`** and press **Enter**.
   - Select the one with **`('.venv': venv)`** in the path (e.g. `./.venv/Scripts/python.exe`).
4. Now whenever you open a new terminal in VS Code, it will automatically activate `.venv` for you! You can also click the ▶️ "Run Python File" button in the top right corner.

---

## 📦 4. Adding New Dependencies

If someone installs a new library during development:
1. Make sure your virtual environment is active.
2. Install the library:
   ```bash
   pip install <library-name>
   ```
3. Update [`requirements.txt`](file:///requirements.txt) so teammates can get it:
   ```bash
   pip freeze > requirements.txt
   ```
4. Commit and push [`requirements.txt`](file:///requirements.txt) to GitHub.
5. Other teammates simply pull and run:
   ```bash
   pip install -r requirements.txt
   ```

---

## ❓ 5. Common Issues & Troubleshooting

- **`'python' is not recognized as an internal or external command`**:
  Python is either not installed or was not added to your system PATH. Re-run the Python installer, choose "Modify", and ensure **"Add Python to environment variables"** is checked.
- **PowerShell error: `execution of scripts is disabled on this system`**:
  Run this command in PowerShell to allow running local scripts:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
  Then run `.venv\Scripts\Activate.ps1` again. Or simply use Command Prompt (`cmd`) or [`setup.bat`](file:///setup.bat).
- **Need to exit the virtual environment in terminal**:
  Type:
  ```bash
  deactivate
  ```