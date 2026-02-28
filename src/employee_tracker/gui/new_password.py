import tkinter as tk
from tkinter import messagebox, ttk

from employee_tracker.gui.style import centre_window

# Window for updating password
class PasswordDialog(tk.Toplevel):
    def __init__(self, parent, title = "Set Password"):
        super().__init__(parent)
        self.title(title)
        self.resizable(False,False)

        self.result = None

        container = ttk.Frame(self, padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        container.columnconfigure(0, weight=1)

        ttk.Label(container, text=title, style="Section.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))

        form = ttk.Frame(container)
        form.grid(row=1, column=0, sticky="ew")
        form.columnconfigure(0, weight=1)

        ttk.Label(form, text="New password").grid(row=0, column=0, sticky="w")
        self.pw1 = ttk.Entry(form, show="*")
        self.pw1.grid(row=1, column=0, sticky="ew", pady=(2, 10))

        ttk.Label(form, text="Confirm password").grid(row=2, column=0, sticky="w")
        self.pw2 = ttk.Entry(form, show="*")
        self.pw2.grid(row=3, column=0, sticky="ew", pady=(2, 0))

        btns = ttk.Frame(container)
        btns.grid(row=2, column=0, sticky="ew", pady=(14, 0))
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)

        ttk.Button(btns, text="Cancel", command=self.on_cancel).grid(row=0, column=0, sticky="ew")
        ttk.Button(btns, text="OK", style="Primary.TButton", command=self.on_ok).grid(row=0, column=1, sticky="ew", padx=(10, 0))

        self.transient(parent)
        self.grab_set()

        #Keybinds for buttons
        self.bind("<Return>", lambda e: self.on_ok())
        self.bind("<Escape>", lambda e: self.on_cancel())
        
        centre_window(self, 380, 260)

        self.pw1.focus_set()

        # helping centering
        if parent is not None:
            x = parent.winfo_rootx() + 50
            y = parent.winfo_rooty() + 50
            self.geometry(f"+{x}+{y}")

    # when OK is pressed, fields are checked, both for existence and matching
    def on_ok(self):
        pass1 = self.pw1.get()
        pass2 = self.pw2.get()

        if not pass1:
            messagebox.showerror("Password error", "Password cannot be empty.", parent=self)
            return
        if pass1 != pass2:
            messagebox.showerror("Password error", "Passwords do not match.", parent=self)
            return
    
        self.result = pass1
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

    def show(self):
        self.wait_window()
        return self.result
