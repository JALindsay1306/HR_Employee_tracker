import tkinter as tk
from tkinter import messagebox, ttk

from employee_tracker.domain.tracker import Tracker
from employee_tracker.gui.style import centre_window

class AddMembersWindow(tk.Toplevel):
    def __init__(self,parent:tk.Tk,tracker:Tracker,dep_id:str,on_done=None):
        super().__init__(parent)
        self.tracker = tracker
        self.dep_id = dep_id
        self.on_done = on_done

        self.title("Add Department Members")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        container = ttk.Frame(self, padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        container.columnconfigure(0, weight=1)

        ttk.Label(container, text="Add members", style="Title.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))

        search_frame = ttk.LabelFrame(container, text="Search", padding=10)
        search_frame.grid(row=1, column=0, sticky="ew")
        search_frame.columnconfigure(0, weight=1)

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_employee_list())

        list_frame = ttk.LabelFrame(container, text="Employees (Ctrl/Shift-click to multi-select)", padding=10)
        list_frame.grid(row=2, column=0, sticky="nsew", pady=(12, 0))
        list_frame.columnconfigure(0, weight=1)

        self.emp_listbox = tk.Listbox(list_frame, width=55, height=14, selectmode=tk.EXTENDED, exportselection=False)
        self.emp_listbox.grid(row=0, column=0, sticky="nsew")

        self.emp_ids = []

        btns = ttk.Frame(container)
        btns.grid(row=3, column=0, sticky="ew", pady=(14, 0))
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)

        ttk.Button(btns, text="Add selected", style="Primary.TButton", command=self.on_add_selected).grid(row=0, column=0, sticky="ew")
        ttk.Button(btns, text="Close", command=self.destroy).grid(row=0, column=1, sticky="ew", padx=(10, 0))

        self.bind("<Escape>", lambda e: self.destroy())

        centre_window(self, 520, 520)
        self.refresh_employee_list()
        self.search_entry.focus_set()

    def refresh_employee_list(self):
        search = self.search_entry.get().strip().lower()

        dep = self.tracker.departments[self.dep_id]
        current_members = set(dep.members or [])

        self.emp_listbox.delete(0, tk.END)
        self.emp_ids = []

        for emp in self.tracker.list_employees():
            search_bucket = f"{emp.name} {emp.role}".lower()
            if search and search not in search_bucket:
                continue
            
            if emp.id in current_members:
                continue

            self.emp_ids.append(emp.id)
            self.emp_listbox.insert(tk.END, f"{emp.id} {emp.name} ({emp.role})")

    def on_add_selected(self):
        selected = self.emp_listbox.curselection()
        if not selected:
            messagebox.showerror("Add members", "Select at least one employee to add.")
            return
        
        dep = self.tracker.departments[self.dep_id]
        current_members = set(dep.members or [])

        added = 0
        errors = []

        for idx in selected:
            emp_id = self.emp_ids[idx]

            if emp_id in current_members:
                continue

            try:
                self.tracker.add_employee_to_department(self.dep_id,emp_id)
                added += 1
            except Exception as err:
                errors.append(f"{emp_id}: {err}")
            
        self.refresh_employee_list()

        if self.on_done:
            self.on_done()
        
        if errors:
            messagebox.showerror("Some additions failed", "\n".join(errors))
        else:
            messagebox.showinfo("Added", f"Added {added} employees(s).")