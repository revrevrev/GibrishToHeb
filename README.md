# Gibrish to Hebrew Text Transformer

A Windows utility that transforms QWERTY-typed text to Hebrew letters. Useful when you accidentally typed Hebrew text with the keyboard set to English or with Caps Lock enabled.

## Features

- **System tray icon**: Runs silently in the background as a tray icon (green circle with ה)
- **Configurable hotkey**: Default is F8; change it any time from the tray menu — persisted across restarts
- **Transform preview**: Before replacing, shows original → Hebrew so you can confirm or cancel
- **QWERTY to Hebrew mapping**: Converts English QWERTY keyboard positions to Hebrew letters

## Quick Start (No Python Required)

Download `GibrishToHeb_Setup.exe` and run it. The installer will:
- Install the program to your user profile (no admin required)
- Add it to Windows startup so it runs automatically on login
- Create a Start Menu shortcut and an uninstaller

> **Note:** Windows may ask for administrator privileges on first run. This is required for global hotkey detection.

---

## Usage

1. Select the text you want to transform in any application.
2. Press the hotkey (default **F8**) to open the transform dialog.
3. A preview shows the original text and the Hebrew result.
4. Click **בצע** (or press Enter) to replace the text, or **בטל** (or Escape) to cancel.

## Tray Icon

Right-click the tray icon for these options:

| Option | Description |
|---|---|
| **Change Hotkey** | Opens a dialog — just press the key combination you want, then Save. Supports F-keys, Ctrl/Alt/Shift combos, etc. |
| **Instructions** | Shows usage instructions in Hebrew |
| **Exit** | Quits the program |

The tray tooltip always shows the currently active hotkey, e.g. `Gibrish to Hebrew (F8)`.

## Hotkey Rules

- **Bare F-keys** (F1–F12) are allowed.
- **Modifier combos** (Ctrl+, Alt+, Shift+) with any key are allowed.
- **Bare letters, digits, arrow keys, Backspace, Enter, Esc, Space, Tab** are blocked to avoid conflicting with normal typing.
- The chosen hotkey is saved to `%APPDATA%\GibrishToHeb\config.json` and reloaded on next launch.

## Example

If you typed `aukji` intending to write `שולחן` (with the wrong keyboard language), the utility converts it correctly.

## Keyboard Mapping

Based on the standard Hebrew keyboard layout:
- `a` → `ש`, `s` → `ד`, `d` → `ג`, `f` → `כ`, `g` → `ע` …
- Numbers, spaces, and unrecognised characters are preserved as-is.
- Both uppercase and lowercase input map to the same Hebrew letter.

## Requirements

- Windows OS
- Administrator privileges may be required for global hotkey detection

## Installation (from source)

1. Python 3.7+ with pip
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   python gibrish_to_heb.py
   ```

## Building from Source

**Prerequisites (build machine only):**
- Python 3.7+ with pip
- [Inno Setup 6](https://jrsoftware.org/isdl.php) (free) — only needed to build the installer

Run:
```bash
build.bat
```

This will:
1. Build the exe via PyInstaller
2. Compile `dist\GibrishToHeb_Setup.exe` via Inno Setup

> **Antivirus note:** PyInstaller-packed executables are sometimes flagged by AV software as a false positive. The file is safe.
