import tkinter as tk
from tkinter import messagebox, ttk


from employee_tracker.auth.login import login
from employee_tracker.gui.style import centre_window

# GUI to utilise login functionality
class LoginWindow(tk.Toplevel):
    def __init__(self,parent,tracker,on_success):
        super().__init__(parent)
        self.title("Login")
        self.tracker = tracker
        self.on_success = on_success

        self.resizable(False,False)

        #create ttk frame
        container = ttk.Frame(self, padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        container.columnconfigure(0, weight=1)
        

        ttk.Label(container, text="Sign in", style="Title.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 12))
        form = ttk.Frame(container)
        form.grid(row=1, column=0, sticky="ew")
        form.columnconfigure(0, weight=1)

        ttk.Label(form, text="Employee ID").grid(row=0, column=0, sticky="w")
        self.emp_id_var = tk.StringVar()
        emp_entry = ttk.Entry(form, textvariable=self.emp_id_var)
        emp_entry.grid(row=1, column=0, sticky="ew", pady=(2, 10))

        ttk.Label(form, text="Password").grid(row=2, column=0, sticky="w")
        self.password_var = tk.StringVar()
        pw_entry = ttk.Entry(form, textvariable=self.password_var, show="*")
        pw_entry.grid(row=3, column=0, sticky="ew", pady=(2, 0))

        btns = ttk.Frame(container)
        btns.grid(row=2, column=0, sticky="ew", pady=(14, 0))
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)

        ttk.Button(btns, text="Login", style="Primary.TButton", command=self.do_login).grid(row=0, column=0, sticky="ew")
        ttk.Button(btns, text="Quit", command=self.quit_app).grid(row=0, column=1, sticky="ew", padx=(10, 0))

        # Loads above parent as a dependent, grabs focus. If the user closes the login window then the full app closes
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.quit_app)

        # esc closes, return clicks Login
        self.bind("<Return>", lambda e: self.do_login())
        self.bind("<Escape>", lambda e: self.quit_app())

        centre_window(self, 360, 240)
        emp_entry.focus_set()

    def do_login(self):
        emp_id = self.emp_id_var.get().strip()
        pw = self.password_var.get()
        # calls login function with inputted information
        try:
            permissions = login(self.tracker, emp_id, pw)
        # Errors are either employee doesn't exist, or password is wrong
        except LookupError as e:
            messagebox.showerror("Login failed", str(e), parent=self)
            return
        except PermissionError as e:
            messagebox.showerror("Login failed", str(e), parent=self)
            return
        
        self.on_success(permissions,emp_id)
        self.destroy()

    # Quit app
    def quit_app(self):
        self.master.destroy()