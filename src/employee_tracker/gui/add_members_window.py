import tkinter as tk
from tkinter import messagebox

from employee_tracker.domain.tracker import Tracker

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

        top = tk.Frame(self)
        top.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(top, text="Search Employees").grid(row=0, column=0, sticky="w")
        self.search_entry = tk.Entry(top, width=30)
        self.search_entry.grid(row=1, column=0, sticky="ew", pady=(2,0))
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_employee_list())

        mid = tk.Frame(self)
        mid.grid(row=1, column=0, padx=10, pady=(0,10), sticky="nsew")

        tk.Label(mid, text="All employees (Ctrl/Shift-click to multi-select)").pack(anchor="w")
        self.emp_listbox = tk.Listbox(mid, width=50, height=14, selectmode=tk.EXTENDED)
        self.emp_listbox.pack()

        self.emp_ids = []

        bottom = tk.Frame(self)
        bottom.grid(row=2, column=0, padx=10, pady=(0,10), sticky="ew")

        self.add_button = tk.Button(bottom, text="Add Selected", command=self.on_add_selected)
        self.add_button.grid(row=0, column=0,sticky="ew")

        self.close_button = tk.Button(bottom, text="Close", command=self.destroy)
        self.close_button.grid(row=0, column=1, padx=(10,0), sticky="ew")

        bottom.grid_columnconfigure(0,weight=1)
        bottom.grid_columnconfigure(1,weight=1)

        self.refresh_employee_list()

        self.bind("<Escape>", lambda e: self.destroy())

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