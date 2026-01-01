# Gibrish to Hebrew Text Transformer

A Windows utility that transforms QWERTY-typed text to Hebrew letters. This is useful when you accidentally typed Hebrew text with the keyboard set to English or with Caps Lock enabled.

## Features

- **Hotkey activation**: Press F8 to activate the transformation menu
- **Quick transformation**: Select text, press F8, and choose "Transform to Hebrew"
- **Resident utility**: Runs in the background and stays active
- **QWERTY to Hebrew mapping**: Automatically converts English QWERTY keyboard positions to Hebrew letters

## Installation

1. Make sure you have Python 3.7 or higher installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the utility:
   ```bash
   python gibrish_to_heb.py
   ```

2. Select the text you want to transform in any application

3. Press **F8** to open the transformation menu

4. Click "Transform to Hebrew" or press Enter to transform the selected text

5. The text will be automatically replaced with Hebrew letters based on QWERTY keyboard positions

## Example

If you typed `aukji` (intending to write "שולחן" but with English keyboard), the utility will transform it correctly.

## Keyboard Mapping

The utility maps QWERTY keyboard positions to Hebrew letters based on the standard Hebrew keyboard layout:
- `a` → `ש`, `s` → `ד`, `d` → `ג`, `f` → `כ`, etc.
- Numbers, spaces, and punctuation are preserved
- Works with both uppercase and lowercase letters

## Requirements

- Python 3.7+
- Windows OS
- Administrator privileges (required for keyboard hook on some systems)

## Exit

Press **Ctrl+C** in the terminal to exit the utility.

## Note

On first run, Windows may prompt for administrator permissions as the keyboard library requires elevated privileges to register global hotkeys.

