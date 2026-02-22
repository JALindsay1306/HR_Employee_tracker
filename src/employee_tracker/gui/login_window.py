import tkinter as tk
from tkinter import messagebox

from employee_tracker.auth.login import login

class LoginWindow(tk.Toplevel):
    def __init__(self,parent,tracker,on_success):
        super().__init__(parent)
        self.title("Login")
        self.tracker = tracker
        self.on_success = on_success

        self.resizable(False,False)

        tk.Label(self, text="Employee ID").grid(row=0,column=0,padx=10,pady=8,sticky="e")
        tk.Label(self, text="Password").grid(row=1,column=0, padx=0,pady=8,sticky="e")

        self.emp_id_var = tk.StringVar()
        self.password_var = tk.StringVar()

        emp_entry = tk.Entry(self,textvariable=self.emp_id_var, width=28)
        pw_entry = tk.Entry(self, textvariable=self.password_var, width=28, show="*")
        emp_entry.grid(row=0, column=1, padx=10, pady=8)
        pw_entry.grid(row=1,column=1, padx=10, pady=8)

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Login", width=10, command=self._do_login).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Quite", width=10, command=self._quit_app).pack(side="left", padx=6)

        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._quit_app)

        emp_entry.focus_set()
        self.bind("<Return>", lambda:)