#!/usr/bin/env python3
"""
Gibrish to Hebrew Text Transformer
A Windows utility that transforms QWERTY-typed text to Hebrew letters
"""

import keyboard
import pyperclip
import tkinter as tk
from tkinter import messagebox
import threading
import pystray
from PIL import Image, ImageDraw, ImageFont
import json
import os

# QWERTY to Hebrew keyboard mapping
# Based on standard Hebrew keyboard layout (QWERTY positions to Hebrew letters)
QWERTY_TO_HEBREW = {
    # Top row
    'q': '/', 'Q': '/',
    'w': "'", 'W': "'",
    'e': 'ק', 'E': 'ק',
    'r': 'ר', 'R': 'ר',
    't': 'א', 'T': 'א',
    'y': 'ט', 'Y': 'ט',
    'u': 'ו', 'U': 'ו',
    'i': 'ן', 'I': 'ן',
    'o': 'ם', 'O': 'ם',
    'p': 'פ', 'P': 'פ',
    # Second row
    'a': 'ש', 'A': 'ש',
    's': 'ד', 'S': 'ד',
    'd': 'ג', 'D': 'ג',
    'f': 'כ', 'F': 'כ',
    'g': 'ע', 'G': 'ע',
    'h': 'י', 'H': 'י',
    'j': 'ח', 'J': 'ח',
    'k': 'ל', 'K': 'ל',
    'l': 'ך', 'L': 'ך',
    # Third row
    'z': 'ז', 'Z': 'ז',
    'x': 'ס', 'X': 'ס',
    'c': 'ב', 'C': 'ב',
    'v': 'ה', 'V': 'ה',
    'b': 'נ', 'B': 'נ',
    'n': 'מ', 'N': 'מ',
    'm': 'צ', 'M': 'צ',
    # Punctuation
    ',': 'ת', '<': 'ת',
    '.': 'ץ', '>': 'ץ',
    '/': '.',
    ';': 'ף', ':': 'ף',
    "'": ',', '"': ',',
    '[': ']', '{': '}',
    ']': '[', '}': '{',
    '\\': '\\', '|': '|',
    '`': ';', '~': ':',
    '-': '-', '_': '_',
    '=': '=', '+': '+',
}

# ---------------------------------------------------------------------------
# Config persistence
# ---------------------------------------------------------------------------

CONFIG_PATH = os.path.join(
    os.environ.get('APPDATA', os.path.expanduser('~')),
    'GibrishToHeb', 'config.json'
)
DEFAULT_HOTKEY = 'f8'

def load_hotkey():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f).get('hotkey', DEFAULT_HOTKEY)
    except Exception:
        return DEFAULT_HOTKEY

def save_hotkey(hotkey):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump({'hotkey': hotkey}, f)

# ---------------------------------------------------------------------------
# Mutable app state (shared between tray callbacks and hotkey logic)
# ---------------------------------------------------------------------------

state = {
    'hotkey': DEFAULT_HOTKEY,
    'icon': None,           # set in main() after icon is created
    'dialog_open': False,   # True while the Change Hotkey dialog is visible
}

# ---------------------------------------------------------------------------
# Core transformation
# ---------------------------------------------------------------------------

def transform_to_hebrew(text):
    result = []
    for char in text:
        if char in QWERTY_TO_HEBREW:
            hebrew_char = QWERTY_TO_HEBREW[char]
            result.append(hebrew_char if hebrew_char else char)
        elif char.isspace() or char.isdigit():
            result.append(char)
        else:
            result.append(char)
    return ''.join(result)

# ---------------------------------------------------------------------------
# Transform dialog (F8 / current hotkey)
# ---------------------------------------------------------------------------

def show_transform_menu():
    import time
    import ctypes

    try:
        original_clipboard = pyperclip.paste()
    except Exception:
        original_clipboard = ""

    # Release any modifiers still held from the hotkey so the injected Ctrl+C
    # isn't seen as e.g. Ctrl+Alt+C by the target app.
    for mod in ('alt', 'ctrl', 'shift', 'left windows', 'right windows'):
        try:
            if keyboard.is_pressed(mod):
                keyboard.release(mod)
        except Exception:
            pass
    time.sleep(0.05)

    user32 = ctypes.windll.user32
    seq_before = user32.GetClipboardSequenceNumber()

    keyboard.send('ctrl+c')

    # Poll until Windows registers a clipboard write (sequence number changes),
    # or give up after ~1000 ms.  Using the sequence number is reliable even
    # when the selected text happens to equal the previous clipboard content.
    selected_text = original_clipboard
    for _ in range(20):
        time.sleep(0.05)
        if user32.GetClipboardSequenceNumber() != seq_before:
            try:
                selected_text = pyperclip.paste()
            except Exception:
                selected_text = original_clipboard
            break

    try:
        if not selected_text or not selected_text.strip() or selected_text == original_clipboard:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            hotkey_display = state['hotkey'].upper()
            messagebox.showinfo(
                "Info",
                f"No text selected.\n\nPlease select text and press {hotkey_display} again."
            )
            root.destroy()
            return

        hebrew_text = transform_to_hebrew(selected_text)

        # ── Design tokens (from HTML reference) ───────────────────────
        SURFACE    = '#FFFFFF'
        BORDER     = '#D8DAE3'
        SOURCE_BG  = '#F4F5F8'
        SRC_FG     = '#6B7080'
        MUTED      = '#8B8FA8'
        TEXT_COLOR = '#1E2030'
        ACCENT     = '#3B5BDB'
        ACCENT_DK  = '#2F4DC8'
        ACCENT_LT  = '#E8EEFF'
        WIN_W      = 520

        root = tk.Tk()
        root.title("המרת כתיב גיבריש לעברית")
        root.configure(bg=SURFACE)
        root.attributes('-topmost', True)
        root.resizable(False, False)

        # ── Header ────────────────────────────────────────────────────
        header = tk.Frame(root, bg=SURFACE, padx=24, pady=20)
        header.pack(fill='x')

        # Icon badge (32×32, accent-lt bg, canvas-drawn icon)
        badge = tk.Canvas(header, width=32, height=32,
                          bg=ACCENT_LT, highlightthickness=0, bd=0)
        badge.pack(side='left')
        # Left three horizontal lines (document/text icon)
        for y_pos in (9, 16, 23):
            badge.create_line(5, y_pos, 16 if y_pos == 9 else (14 if y_pos == 16 else 11),
                              y_pos, fill=ACCENT, width=2, capstyle='round')
        # Right aleph-like shape
        badge.create_line(22, 7,  28, 19, fill=ACCENT, width=2, capstyle='round')
        badge.create_line(22, 7,  16, 19, fill=ACCENT, width=2, capstyle='round')
        badge.create_line(17, 14, 27, 14, fill=ACCENT, width=2, capstyle='round')

        tk.Label(
            header, text='המרת כתיב גיבריש לעברית',
            bg=SURFACE, fg=TEXT_COLOR,
            font=('Segoe UI', 12, 'bold'),
            anchor='w',
        ).pack(side='left', padx=(10, 0))

        tk.Frame(root, bg=BORDER, height=1).pack(fill='x')

        # ── Body ──────────────────────────────────────────────────────
        body = tk.Frame(root, bg=SURFACE, padx=24, pady=20)
        body.pack(fill='x')

        # Source block
        src_border = tk.Frame(body, bg=BORDER)
        src_border.pack(fill='x')
        src_inner = tk.Frame(src_border, bg=SOURCE_BG, padx=14, pady=12)
        src_inner.pack(fill='x', padx=1, pady=1)

        src_h = min(max(1, selected_text.count('\n') + 1), 4)
        src_widget = tk.Text(
            src_inner, height=src_h,
            bg=SOURCE_BG, fg=SRC_FG,
            font=('Segoe UI', 10),
            wrap='word', relief='flat', bd=0, highlightthickness=0,
            cursor='arrow', padx=0, pady=0, spacing1=2, spacing3=2,
        )
        src_widget.insert('1.0', selected_text)
        src_widget.configure(state='disabled')
        src_widget.pack(fill='x')

        # Arrow divider with horizontal rules
        div = tk.Frame(body, bg=SURFACE)
        div.pack(fill='x', pady=10)
        div.columnconfigure(0, weight=1)
        div.columnconfigure(2, weight=1)
        tk.Frame(div, bg=BORDER, height=1).grid(row=0, column=0, sticky='ew', pady=6)
        tk.Label(div, text='↓', bg=SURFACE, fg=MUTED,
                 font=('Segoe UI', 11)).grid(row=0, column=1, padx=8)
        tk.Frame(div, bg=BORDER, height=1).grid(row=0, column=2, sticky='ew', pady=6)

        # Result block (editable)
        res_border = tk.Frame(body, bg=ACCENT)
        res_border.pack(fill='x')
        res_inner = tk.Frame(res_border, bg=ACCENT_LT, padx=14, pady=12)
        res_inner.pack(fill='x', padx=2, pady=2)

        heb_h = min(max(2, hebrew_text.count('\n') + 2), 5)
        result_widget = tk.Text(
            res_inner, height=heb_h,
            bg=ACCENT_LT, fg=TEXT_COLOR,
            font=('David', 14),  # Windows Hebrew system font
            wrap='word', relief='flat', bd=0, highlightthickness=0,
            cursor='xterm', padx=0, pady=0, spacing1=2, spacing3=4,
            insertbackground=ACCENT,
        )
        result_widget.tag_configure('rtl', justify='right')
        result_widget.insert('1.0', hebrew_text)
        result_widget.tag_add('rtl', '1.0', 'end')
        result_widget.pack(fill='x')
        result_widget.focus_set()
        result_widget.mark_set('insert', 'end')

        tk.Frame(root, bg=BORDER, height=1).pack(fill='x')

        # ── Footer ────────────────────────────────────────────────────
        footer = tk.Frame(root, bg=SURFACE, padx=24, pady=14)
        footer.pack(fill='x')

        def perform_transform():
            edited = result_widget.get('1.0', 'end-1c')
            try:
                pyperclip.copy(edited)
                root.destroy()
                time.sleep(0.25)
                keyboard.send('delete')
                time.sleep(0.08)
                keyboard.send('ctrl+v')
                # Restore original clipboard so next hotkey press can detect
                # a new selection even if it matches the just-pasted Hebrew text.
                time.sleep(0.15)
                pyperclip.copy(original_clipboard)
            except Exception as e:
                root.destroy()
                error_root = tk.Tk()
                error_root.withdraw()
                error_root.attributes('-topmost', True)
                messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
                error_root.destroy()
                pyperclip.copy(original_clipboard)

        def cancel():
            pyperclip.copy(original_clipboard)
            root.destroy()

        # Buttons — centered, בצע on the right
        btn_frame = tk.Frame(footer, bg=SURFACE)
        btn_frame.pack(anchor='center')

        tk.Button(
            btn_frame, text='בטל',
            bg=SURFACE, fg=MUTED,
            font=('Segoe UI', 10),
            padx=20, pady=5,
            relief='solid', bd=1,
            highlightbackground=BORDER, highlightthickness=0,
            cursor='hand2', command=cancel,
            activebackground='#EEEEF2', activeforeground=TEXT_COLOR,
        ).pack(side='left', padx=(0, 8))

        tk.Button(
            btn_frame, text='בצע',
            bg=ACCENT, fg='white',
            font=('Segoe UI', 10, 'bold'),
            padx=20, pady=5,
            relief='flat', bd=0,
            cursor='hand2', command=perform_transform,
            activebackground=ACCENT_DK, activeforeground='white',
        ).pack(side='left')

        root.bind('<Return>', lambda e: perform_transform())
        root.bind('<Escape>', lambda e: cancel())

        root.update_idletasks()
        h = root.winfo_reqheight()
        x = (root.winfo_screenwidth()  // 2) - (WIN_W // 2)
        y = (root.winfo_screenheight() // 2) - (h // 2)
        root.geometry(f'{WIN_W}x{h}+{x}+{y}')

        root.mainloop()

    except Exception as e:
        error_root = tk.Tk()
        error_root.withdraw()
        error_root.attributes('-topmost', True)
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        error_root.destroy()
        pyperclip.copy(original_clipboard)

def on_hotkey_pressed():
    if state['dialog_open']:
        return
    thread = threading.Thread(target=show_transform_menu, daemon=True)
    thread.start()

# ---------------------------------------------------------------------------
# Change Hotkey dialog
# ---------------------------------------------------------------------------

# Tkinter keysym → keyboard-library name for keys that differ
_KEYSYM_MAP = {
    'return': 'enter',
    'prior': 'page_up',
    'next': 'page_down',
    'escape': 'esc',
    'backspace': 'backspace',
    'tab': 'tab',
    'space': 'space',
    'home': 'home',
    'end': 'end',
    'delete': 'delete',
    'insert': 'insert',
    'up': 'up',
    'down': 'down',
    'left': 'left',
    'right': 'right',
    'print': 'print_screen',
    'scroll_lock': 'scroll_lock',
    'pause': 'pause',
    'num_lock': 'num_lock',
}

# Keys that are modifiers themselves — ignore as the sole key
_MODIFIER_KEYSYMS = {
    'control_l', 'control_r', 'shift_l', 'shift_r',
    'alt_l', 'alt_r', 'super_l', 'super_r',
    'meta_l', 'meta_r', 'caps_lock', 'mode_switch',
}

# Keys that must not be used as a bare hotkey (without a modifier)
_BARE_BLOCKED = {
    'home', 'end', 'delete', 'backspace', 'insert',
    'print_screen', 'scroll_lock', 'pause', 'num_lock',
    'space', 'tab', 'enter', 'esc',
    'up', 'down', 'left', 'right',
    'page_up', 'page_down',
    # punctuation / numpad symbols (Tkinter returns full names, not single chars)
    'slash', 'asterisk', 'minus', 'plus',
    'kp_divide', 'kp_multiply', 'kp_subtract', 'kp_add',
}

def _parse_tkinter_event(event):
    """Convert a Tkinter KeyPress event into a keyboard-library hotkey string."""
    keysym = event.keysym.lower()
    if keysym in _MODIFIER_KEYSYMS:
        return None  # lone modifier, ignore

    parts = []
    if event.state & 0x4:    # Ctrl
        parts.append('ctrl')
    if event.state & 0x1:    # Shift
        parts.append('shift')
    if event.state & 0x20000:  # Alt (Windows Tkinter)
        parts.append('alt')

    key = _KEYSYM_MAP.get(keysym, keysym)

    # Reject bare regular characters (letters, digits, punctuation) with no modifier.
    # Also reject the explicitly blocked special keys above.
    if not parts and (len(key) == 1 or key in _BARE_BLOCKED):
        return None

    parts.append(key)
    return '+'.join(parts)


def show_change_hotkey_dialog():
    state['dialog_open'] = True
    root = tk.Tk()
    root.title("Change Hotkey")
    root.attributes('-topmost', True)
    root.resizable(False, False)

    root.update_idletasks()
    width, height = 340, 170
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    captured = [state['hotkey']]   # mutable, updated by key capture

    tk.Label(root, text="Press the key combination you want to use:",
             font=('Arial', 10), pady=6).pack()

    display_var = tk.StringVar(value=state['hotkey'].upper())
    display_label = tk.Label(
        root,
        textvariable=display_var,
        font=('Arial', 14, 'bold'),
        relief='sunken',
        width=18,
        pady=6,
        cursor='xterm',
    )
    display_label.pack(padx=20, pady=4)
    display_label.focus_set()

    def on_key(event):
        hotkey = _parse_tkinter_event(event)
        if hotkey:
            captured[0] = hotkey
            display_var.set(hotkey.upper())

    display_label.bind('<KeyPress>', on_key)
    display_label.bind('<Escape>', lambda e: cancel())

    def save():
        state['dialog_open'] = False
        new_hotkey = captured[0]
        root.destroy()
        _apply_new_hotkey(new_hotkey)

    def cancel():
        state['dialog_open'] = False
        root.destroy()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(
        btn_frame, text="Save", command=save,
        bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'),
        padx=16,
    ).pack(side='left', padx=6)
    tk.Button(
        btn_frame, text="Cancel", command=cancel,
        padx=16,
    ).pack(side='left', padx=6)

    root.bind('<Escape>', lambda e: cancel())
    root.mainloop()


def _apply_new_hotkey(new_hotkey):
    """Re-register the keyboard hook and persist the new hotkey."""
    try:
        keyboard.remove_hotkey(state['hotkey'])
    except Exception:
        keyboard.unhook_all()

    state['hotkey'] = new_hotkey
    keyboard.add_hotkey(new_hotkey, on_hotkey_pressed)
    save_hotkey(new_hotkey)

    # Update tray tooltip and force menu label refresh
    if state['icon']:
        state['icon'].title = f'Gibrish to Hebrew ({new_hotkey.upper()})'
        state['icon'].update_menu()


def on_change_hotkey(icon, item):
    thread = threading.Thread(target=show_change_hotkey_dialog, daemon=True)
    thread.start()

# ---------------------------------------------------------------------------
# Instructions dialog
# ---------------------------------------------------------------------------

def show_instructions_dialog():
    hotkey = state['hotkey'].upper()
    text = (
        "הוראות שימוש:\n\n"
        "  1. בחר טקסט בכל יישום\n"
        "  2. לחץ על מקש הקיצור לפתיחת חלון ההמרה\n"
        "  3. לחץ \"בצע\" לביצוע ההמרה, או \"בטל\" לביטול\n"
        "  4. הטקסט יוחלף אוטומטית באותיות עבריות\n\n"
        "התוכנית פועלת ברקע כאייקון במגש המערכת.\n"
        "לחיצה ימנית על האייקון מאפשרת שינוי מקש הקיצור או יציאה מהתוכנית.\n\n"
        f"מקש הקיצור שנבחר: {hotkey}"
    )
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    messagebox.showinfo("הוראות שימוש", text)
    root.destroy()

def on_instructions(icon, item):
    thread = threading.Thread(target=show_instructions_dialog, daemon=True)
    thread.start()

# ---------------------------------------------------------------------------
# Tray icon
# ---------------------------------------------------------------------------

def create_tray_icon_image():
    size = 64
    img = Image.new('RGB', (size, size), color=(45, 45, 45))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 60, 60], fill=(76, 175, 80))
    try:
        font = ImageFont.truetype('arial.ttf', 36)
        draw.text((18, 12), 'ה', font=font, fill=(255, 255, 255))
    except Exception:
        font = ImageFont.load_default()
        draw.text((26, 24), 'H', font=font, fill=(255, 255, 255))
    return img


def main():
    state['hotkey'] = load_hotkey()
    keyboard.add_hotkey(state['hotkey'], on_hotkey_pressed)

    def on_exit(icon, item):
        keyboard.unhook_all()
        icon.stop()

    # Use a callable for the label so it always reflects the current hotkey
    menu = pystray.Menu(
        pystray.MenuItem(
            lambda item: f"Gibrish \u2192 Hebrew  ({state['hotkey'].upper()})",
            None, enabled=False
        ),
        pystray.MenuItem('Change Hotkey', on_change_hotkey),
        pystray.MenuItem('Instructions', on_instructions),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Exit', on_exit),
    )
    icon = pystray.Icon(
        name='GibrishToHeb',
        icon=create_tray_icon_image(),
        title=f"Gibrish to Hebrew ({state['hotkey'].upper()})",
        menu=menu,
    )
    state['icon'] = icon

    try:
        icon.run()
    except KeyboardInterrupt:
        keyboard.unhook_all()


if __name__ == "__main__":
    main()
