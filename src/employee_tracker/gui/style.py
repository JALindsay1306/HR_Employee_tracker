import tkinter as tk
from tkinter import ttk

def apply_style(root: tk.Misc):
    style = ttk.Style(root)

    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    root.option_add("*Font", ("Segoe UI",10))

    style.configure("TButton", padding=(10,6))
    style.configure("TEntry", padding=(6,4))
    style.configure("TLabel", padding=(0,2))

    style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
    style.configure("Section.TLabel", font=("Segoe UI", 11, "bold"))
    style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))

    root.option_add("*Listbox.Font",("Segoe UI", 10))
    root.option_add("*Listbox.BorderWidth",0)
    root.option_add("*Listbox.HighlightThickness", 1)

def centre_window(win: tk.Misc, width: int, height: int):
    win.update_idletasks()
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

