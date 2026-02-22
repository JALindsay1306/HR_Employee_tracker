import tkinter as tk
from datetime import date
from tkinter import messagebox

from employee_tracker.domain.tracker import Tracker

def parse_employee_form(name: str, role: str, start_date_str: str, salary_str: str, address: str):
    name = name.strip()
    role = role.strip()
    address = address.strip()

    if not name:
        raise ValueError("Name is required")
    if not role:
        raise ValueError("Role is required")
    if not address:
        raise ValueError("Address is required")
    
    try:
        start_date = date.fromisoformat(start_date_str.strip())
    except ValueError as err:
        raise ValueError("Start date must be YYYY-MM-DD") from err

    try:
        salary = int(salary_str.strip())
    except ValueError as err:
        raise ValueError("Salary must be an integer") from err
    
    return dict(name=name,role=role,start_date=start_date,salary=salary,address=address)

class EmployeeWindow(tk.Toplevel):
    def __init__(self,parent:tk.Tk,tracker):
        super().__init__(parent)
        self.tracker = tracker
        self.title("Employees")
        
        self.employee_ids = []
        self.selected_employee_id = None

        left = tk.Frame(self)
        left.grid(row=0,column=0,padx=10,pady=10,sticky="n")

        tk.Label(left,text="Employees").pack()
        self.listbox = tk.Listbox(left,width=35,height=12)
        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>",self.on_select)

        self.bind("<Escape>", lambda e: self.deselect_employee())

        right = tk.Frame(self)
        right.grid(row=0,column=1,padx=10,pady=10,sticky="n")

        self.form_title_label = tk.Label(right, text="Create Employee")
        self.form_title_label.grid(row=0, column=0, columnspan=2, pady=(0,10))

        tk.Label(right, text="Name").grid(row=1,column=0,sticky="e")
        self.name_entry = tk.Entry(right,width=25)
        self.name_entry.grid(row=1,column=1)

        tk.Label(right,text="Role").grid(row=2, column=0,sticky="e")
        self.role_entry = tk.Entry(right,width=25)
        self.role_entry.grid(row=2,column=1)

        tk.Label(right, text="Start date (YYYY-MM-DD)").grid(row=3,column=0,sticky="e")
        self.start_date_entry = tk.Entry(right,width=25)
        self.start_date_entry.grid(row=3,column=1)

        tk.Label(right,text="Salary").grid(row=4,column=0,sticky="e")
        self.salary_entry = tk.Entry(right,width=25)
        self.salary_entry.grid(row=4,column=1)

        tk.Label(right, text="Address").grid(row=5,column=0,sticky="e")
        self.address_entry = tk.Entry(right,width=25)
        self.address_entry.grid(row=5,column=1)

        btn_row = 6

        self.create_button = tk.Button(right, text="Create", command=self.on_create)
        self.create_button.grid(row=btn_row, column=0, columnspan=2, pady=10,sticky="ew")
        
        self.update_button = tk.Button(right, text="Update", command=self.on_update)
        self.delete_button = tk.Button(right, text="Delete", command=self.on_delete)

        self.update_button.grid(row=btn_row, column=0, pady=10, sticky="ew")
        self.delete_button.grid(row=btn_row, column=1, pady=10, sticky="ew")
        self.update_button.grid_remove()
        self.delete_button.grid_remove()

        self.new_button = tk.Button(right, text="New/Deselect", command=self.deselect_employee)
        self.new_button.grid(row=btn_row + 1, column=0, columnspan=2, pady=(0,5), sticky="ew")
        self.new_button.grid_remove()


        self.refresh_list()
        self.set_mode_create()

    def clear_form(self):
        self.name_entry.delete(0,tk.END)
        self.role_entry.delete(0,tk.END)
        self.start_date_entry.delete(0,tk.END)
        self.salary_entry.delete(0,tk.END)
        self.address_entry.delete(0,tk.END)

    def set_mode_create(self):
        self.selected_employee_id = None
        self.form_title_label.config(text="Create Employee")

        self.update_button.grid_remove()
        self.delete_button.grid_remove()
        self.new_button.grid_remove()
        self.create_button.grid()

    def set_mode_edit(self):
        self.form_title_label.config(text="Edit Employee")

        self.create_button.grid_remove()
        self.update_button.grid()
        self.delete_button.grid()
        self.new_button.grid()

    def deselect_employee(self):
        self.listbox.selection_clear(0,tk.END)
        self.clear_form()
        self.set_mode_create()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        self.employee_ids = []
        for emp in self.tracker.list_employees():
            self.employee_ids.append(emp.id)
            self.listbox.insert(tk.END, f"{emp.id} {emp.name} ({emp.role})")

    def on_create(self):
        try:
            data = parse_employee_form(
                self.name_entry.get(),
                self.role_entry.get(),
                self.start_date_entry.get(),
                self.salary_entry.get(),
                self.address_entry.get(),
            )

            self.tracker.create_employee(**data)
            self.refresh_list()

            self.clear_form()

            self.set_mode_create()
        except Exception as err:
            messagebox.showerror("Create employee failed",str(err))
    
    def on_update(self):
        if self.selected_employee_id is None:
            messagebox.showerror("Update employee failed", "No employee selected.")
            return

        try:
            data = parse_employee_form(
                self.name_entry.get(),
                self.role_entry.get(),
                self.start_date_entry.get(),
                self.salary_entry.get(),
                self.address_entry.get()
            )

            emp = self.tracker.employees[self.selected_employee_id]
            emp.name = data["name"]
            emp.role = data["role"]
            emp.start_date = data["start_date"]
            emp.salary = data["salary"]
            emp.address = data["address"]

            self.refresh_list()

            try:
                idx - self.employee_ids.index(self.selected_employee_id)
                self.listbox.selection_set(idx)
                self.listbox.activate(idx)
            except ValueError:
                pass

            self.set_mode_edit()
        except Exception as err:
            messagebox.showerror("Update employee failed", str(err))

    def on_delete(self):
        if self.selected_employee_id is None:
            messagebox.showerror("Delete employee failed", "No employee selected.")
            return
        
        if not messagebox.askyesno("Confirm delete", "Delete this employee?"):
            return
        
        try:
            self.tracker.delete_employee(self.selected_employee_id)
            self.refresh_list()
            self.deselect_employee()
        except Exception as err:
            messagebox.showerror("Delete employee failed", str(err))

    def on_select(self,event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.set_mode_create()
            return
        
        idx = sel[0]
        emp_id = self.employee_ids[idx]
        self.selected_employee_id = emp_id

        emp = self.tracker.employees[emp_id]

        self.name_entry.delete(0,tk.END)
        self.name_entry.insert(0,emp.name)

        self.role_entry.delete(0,tk.END)
        self.role_entry.insert(0,emp.role)

        self.start_date_entry.delete(0,tk.END)
        self.start_date_entry.insert(0,emp.start_date.isoformat())

        self.salary_entry.delete(0,tk.END)
        self.salary_entry.insert(0,str(emp.salary))

        self.address_entry.delete(0,tk.END)
        self.address_entry.insert(0,emp.address)

        self.set_mode_edit()

if __name__ == "__main__":
    tracker = Tracker()
    app = EmployeeWindow(None, tracker)
    app.mainloop()