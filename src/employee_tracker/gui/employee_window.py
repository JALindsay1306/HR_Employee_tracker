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

class EmployeeWindow(tk.Tk):
    def __init__(self,parent:tk.Tk,tracker):
        super().__init__()
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

        right = tk.Frame(self)
        right.grid(row=0,column=1,padx=10,pady=10,sticky="n")

        tk.Label(right,text="Create / Edit Employee").grid(row=0,column=0,columnspan=2,pady=(0,10))

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

        tk.Button(right, text="Create", command=self.on_create).grid(row=6,column=0,columnspan=2,pady=10)

        self.refresh_list()

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
            print(data)
            self.tracker.create_employee(**data)
            self.refresh_list()
        except Exception as err:
            messagebox.showerror("Create employee failed",str(err))
    
    def on_select(self,event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.selected_employee_id = None
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

if __name__ == "__main__":
    tracker = Tracker()
    root = tk.Tk()
    root.withdraw()
    EmployeeWindow(root, tracker)
    root.mainloop()