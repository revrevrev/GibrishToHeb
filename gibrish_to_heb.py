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
    'i': 'י', 'I': 'י',
    'o': 'ן', 'O': 'ן',
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
    '/': '.', '?': '.',
    ';': 'ף', ':': 'ף',
    "'": ',', '"': ',',
    '[': ']', '{': '}',
    ']': '[', '}': '{',
    '\\': '\\', '|': '|',
    '`': ';', '~': ':',
    '-': '-', '_': '_',
    '=': '=', '+': '+',
}

def transform_to_hebrew(text):
    """
    Transform QWERTY-typed text to Hebrew letters
    """
    result = []
    for char in text:
        if char in QWERTY_TO_HEBREW:
            hebrew_char = QWERTY_TO_HEBREW[char]
            result.append(hebrew_char if hebrew_char else char)
        elif char.isspace():
            result.append(char)  # Preserve spaces
        elif char.isdigit():
            result.append(char)  # Preserve numbers
        else:
            result.append(char)  # Keep unknown characters as-is
    return ''.join(result)

def show_transform_menu():
    """Show a popup menu to transform selected text"""
    import time
    
    # Get current clipboard content (to restore later if needed)
    try:
        original_clipboard = pyperclip.paste()
    except:
        original_clipboard = ""
    
    # Store the original selected text by copying it
    # We use Ctrl+C which typically preserves selection in most Windows apps
    keyboard.send('ctrl+c')
    
    # Wait a bit for clipboard to update
    time.sleep(0.15)
    
    # Get the copied text
    try:
        selected_text = pyperclip.paste()
        
        if not selected_text or not selected_text.strip():
            # Create a simple info window
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            messagebox.showinfo("Info", "No text selected.\n\nPlease select text and press F8 again.")
            root.destroy()
            return
        
        # Create popup window with transform option
        root = tk.Tk()
        root.title("Transform to Hebrew")
        root.attributes('-topmost', True)
        root.resizable(False, False)
        
        # Center the window
        root.update_idletasks()
        width = 400
        height = 150
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Show preview of selected text (truncated)
        preview_text = selected_text[:60] + ('...' if len(selected_text) > 60 else '')
        preview_label = tk.Label(
            root, 
            text=f"Selected text:\n{preview_text}",
            wraplength=350,
            justify='left',
            padx=10,
            pady=5
        )
        preview_label.pack(pady=5)
        
        def perform_transform():
            try:
                # Transform the text
                hebrew_text = transform_to_hebrew(selected_text)
                
                # Copy transformed text to clipboard
                pyperclip.copy(hebrew_text)
                
                # Close the menu window first to return focus to the original application
                root.destroy()
                
                # Give a small delay for the window to close and focus to return to the original app
                time.sleep(0.25)
                
                # Replace the selected text with transformed text
                # Strategy: Delete key removes selected text (if selection still exists)
                # Then paste the transformed text
                # This works in most Windows applications
                keyboard.send('delete')
                time.sleep(0.08)
                keyboard.send('ctrl+v')
                
            except Exception as e:
                root.destroy()
                error_root = tk.Tk()
                error_root.withdraw()
                error_root.attributes('-topmost', True)
                messagebox.showerror("Error", f"An error occurred:\n{str(e)}", parent=error_root)
                error_root.destroy()
                # Restore original clipboard on error
                pyperclip.copy(original_clipboard)
        
        def cancel():
            # Restore original clipboard
            pyperclip.copy(original_clipboard)
            root.destroy()
        
        # Transform button
        transform_btn = tk.Button(
            root,
            text="Transform to Hebrew",
            command=perform_transform,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=5
        )
        transform_btn.pack(pady=5)
        
        # Cancel button
        cancel_btn = tk.Button(
            root,
            text="Cancel",
            command=cancel,
            padx=20,
            pady=5
        )
        cancel_btn.pack(pady=5)
        
        # Make Enter key trigger transform, Escape to cancel
        root.bind('<Return>', lambda e: perform_transform())
        root.bind('<Escape>', lambda e: cancel())
        transform_btn.focus_set()
        
        root.mainloop()
    
    except Exception as e:
        error_root = tk.Tk()
        error_root.withdraw()
        error_root.attributes('-topmost', True)
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}", parent=error_root)
        error_root.destroy()
        # Restore original clipboard on error
        pyperclip.copy(original_clipboard)

def on_hotkey_pressed():
    """Callback when F8 is pressed"""
    # Run in a separate thread to avoid blocking
    thread = threading.Thread(target=show_transform_menu, daemon=True)
    thread.start()

def main():
    """Main function to set up hotkey and run the utility"""
    print("Gibrish to Hebrew Transformer")
    print("Press F8 to transform selected text to Hebrew")
    print("Press Ctrl+C to exit")
    
    # Register F8 hotkey
    keyboard.add_hotkey('f8', on_hotkey_pressed)
    
    try:
        # Keep the program running
        keyboard.wait('ctrl+c')
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        keyboard.unhook_all()

if __name__ == "__main__":
    main()


