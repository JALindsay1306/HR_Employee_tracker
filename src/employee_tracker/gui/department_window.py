import tkinter as tk
from datetime import date
from tkinter import messagebox

from employee_tracker.domain.tracker import Tracker
from employee_tracker.utils.ids import check_id
from employee_tracker.gui.add_members_window import AddMembersWindow

def parse_department_form(name: str, description: str, head_of_department: str, parent_department: str):
    name = name.strip()
    description = description.strip()
    head_of_department = head_of_department.strip()
    parent_department = parent_department.strip() or None

    if not name:
        raise ValueError("Name is required")
    if not description:
        raise ValueError("Description is required")
    if not head_of_department:
        raise ValueError("Head of Department is required")
    
    if not check_id(head_of_department,"emp"):
        raise ValueError("Head of department must be an employee ID")
    
    if parent_department is not None and not check_id(parent_department,"dep"):
        raise ValueError("Parent department must be a department ID")
    
    return dict(name=name,description=description,head_of_department=head_of_department,parent_department=parent_department)

class DepartmentWindow(tk.Toplevel):
    def __init__(self,parent:tk.Tk,tracker):
        super().__init__(parent)
        self.tracker = tracker
        self.title("Department")
        
        self.department_ids = []
        self.member_employee_ids = []
        self.selected_department_id = None
        self.selected_employee_id = None

        left = tk.Frame(self)
        left.grid(row=0,column=0,padx=10,pady=10,sticky="n")

        tk.Label(left,text="Departments").pack()
        self.listbox = tk.Listbox(left,width=35,height=12, exportselection=False)
        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>",self.on_select)

        self.bind("<Escape>", lambda e: self.deselect_department())

        centre = tk.Frame(self)
        centre.grid(row=0,column=1,padx=10,pady=10,sticky="n")

        self.form_title_label = tk.Label(centre, text="Create Department")
        self.form_title_label.grid(row=0, column=0, columnspan=2, pady=(0,10))

        tk.Label(centre, text="Name").grid(row=1,column=0,sticky="e")
        self.name_entry = tk.Entry(centre,width=25)
        self.name_entry.grid(row=1,column=1)

        tk.Label(centre,text="Description").grid(row=2, column=0,sticky="e")
        self.description_entry = tk.Entry(centre,width=25)
        self.description_entry.grid(row=2,column=1)

        tk.Label(centre, text="Head of Department").grid(row=3,column=0,sticky="e")
        self.head_of_department_entry = tk.Entry(centre,width=25)
        self.head_of_department_entry.grid(row=3,column=1)

        tk.Label(centre,text="Parent_Department").grid(row=4,column=0,sticky="e")
        self.parent_department_entry = tk.Entry(centre,width=25)
        self.parent_department_entry.grid(row=4,column=1)

        btn_row = 5

        self.create_button = tk.Button(centre, text="Create", command=self.on_create)
        self.create_button.grid(row=btn_row, column=0, columnspan=2, pady=10,sticky="ew")
        
        self.update_button = tk.Button(centre, text="Update", command=self.on_update)
        self.delete_button = tk.Button(centre, text="Delete", command=self.on_delete)

        self.update_button.grid(row=btn_row, column=0, pady=10, sticky="ew")
        self.delete_button.grid(row=btn_row, column=1, pady=10, sticky="ew")
        self.update_button.grid_remove()
        self.delete_button.grid_remove()

        self.new_button = tk.Button(centre, text="New/Deselect", command=self.deselect_department)
        self.new_button.grid(row=btn_row + 1, column=0, columnspan=2, pady=(0,5), sticky="ew")
        self.new_button.grid_remove()

        right = tk.Frame(self)
        right.grid(row=0,column=2,padx=10,pady=10,sticky="n")

        tk.Label(right,text="Department Members").pack()
        self.right_listbox = tk.Listbox(right,width=35,height=12, exportselection=False)
        self.right_listbox.pack()
        self.right_listbox.bind("<<ListboxSelect>>",self.on_select_member)

        btns = tk.Frame(right)
        btns.pack(pady=(10,0), fill="x")

        self.add_members_button = tk.Button(btns, text="Add members", command=self.open_add_members_window)
        self.add_members_button.pack(side="left", expand=True, fill="x")

        self.remove_member_button = tk.Button(btns, text="Remove member", command=self.on_remove_member)
        self.remove_member_button.pack(side="left", padx=(8, 0), expand=True, fill="x")

        self.refresh_list()
        self.set_mode_create()

    def clear_form(self):
        self.name_entry.delete(0,tk.END)
        self.description_entry.delete(0,tk.END)
        self.head_of_department_entry.delete(0,tk.END)
        self.parent_department_entry.delete(0,tk.END)

    def set_mode_create(self):
        self.selected_department_id = None
        self.form_title_label.config(text="Create Department")

        self.update_button.grid_remove()
        self.delete_button.grid_remove()
        self.new_button.grid_remove()
        self.create_button.grid()

    def set_mode_edit(self):
        self.form_title_label.config(text="Edit Department")

        self.create_button.grid_remove()
        self.update_button.grid()
        self.delete_button.grid()
        self.new_button.grid()

    def deselect_department(self):
        self.listbox.selection_clear(0,tk.END)
        self.clear_form()
        self.set_mode_create()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        self.department_ids = []
        for dep in self.tracker.list_departments():
            self.department_ids.append(dep.id)
            self.listbox.insert(tk.END, f"{dep.id} {dep.name} ({dep.description})")

    def refresh_members(self, dep):
        self.right_listbox.delete(0, tk.END)
        self.member_employee_ids = []
        self.selected_employee_id = None

        for emp_id in (dep.members or []):
            emp = self.tracker.employees.get(emp_id)
            if emp is None:
                self.member_employee_ids.append(emp_id)
                self.right_listbox.insert(tk.END, f"{emp_id} (missing employee)")
            else:
                self.member_employee_ids.append(emp.id)
                self.right_listbox.insert(tk.END, f"{emp.id} {emp.name} ({emp.role})")
       
    
    def on_create(self):
        try:
            data = parse_department_form(
                self.name_entry.get(),
                self.description_entry.get(),
                self.head_of_department_entry.get(),
                self.parent_department_entry.get(),
            )

            self.tracker.create_department(**data)
            self.refresh_list()

            self.clear_form()

            self.set_mode_create()
        except Exception as err:
            messagebox.showerror("Create department failed",str(err))
    
    def on_update(self):
        if self.selected_department_id is None:
            messagebox.showerror("Update department failed", "No department selected.")
            return

        try:
            data = parse_department_form(
                self.name_entry.get(),
                self.description_entry.get(),
                self.head_of_department_entry.get(),
                self.parent_department_entry.get(),
            )

            dep = self.tracker.department[self.selected_department_id]
            dep.name = data["name"]
            dep.description = data["description"]
            dep.head_of_department = data["head_of_department"]
            if data["parent_department"]:
                dep.parent_department = data["parent_department"]

            self.refresh_list()

            try:
                idx = self.department_ids.index(self.selected_department_id)
                self.listbox.selection_set(idx)
                self.listbox.activate(idx)
            except ValueError:
                pass

            self.set_mode_edit()
        except Exception as err:
            messagebox.showerror("Update department failed", str(err))

    def on_delete(self):
        if self.selected_department_id is None:
            messagebox.showerror("Delete department failed", "No department selected.")
            return
        
        if not messagebox.askyesno("Confirm delete", "Delete this department?"):
            return
        
        try:
            self.tracker.delete_department(self.selected_department_id)
            self.refresh_list()
            self.deselect_department()
        except Exception as err:
            messagebox.showerror("Delete department failed", str(err))

    def on_select(self,event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.set_mode_create()
            return
        
        idx = sel[0]
        dep_id = self.department_ids[idx]
        self.selected_department_id = dep_id
        self.selected_employee_id = None

        dep = self.tracker.departments[dep_id]

        self.name_entry.delete(0,tk.END)
        self.name_entry.insert(0,dep.name)

        self.description_entry.delete(0,tk.END)
        self.description_entry.insert(0,dep.description)

        self.head_of_department_entry.delete(0,tk.END)
        self.head_of_department_entry.insert(0,dep.head_of_department)

        self.parent_department_entry.delete(0,tk.END)
        self.parent_department_entry.insert(0,str(dep.parent_department))

        self.set_mode_edit()
        self.refresh_members(dep)

    def open_add_members_window(self):
        if self.selected_department_id is None:
            messagebox.showerror("Add members","Select a department first.")
            return
        AddMembersWindow(
            parent=self,
            tracker=self.tracker,
            dep_id=self.selected_department_id,
            on_done=self._refresh_selected_department_members
        )

    def on_select_member(self,event=None):
        sel = self.right_listbox.curselection()
        if not sel:
            self.selected_employee_id = None
            return
    
        idx = sel[0]
        self.selected_employee_id = self.member_employee_ids[idx]

    def on_remove_member(self):
        if self.selected_department_id is None:
            messagebox.showerror("Remove member failed", "No department selected")
            return
        if self.selected_employee_id is None:
            messagebox.showerror("Remove department member failed", "No employee selected.")
            return
        
        if not messagebox.askyesno("Confirm removal", "Remove this employee from the department?"):
            return
        
        try:
            self.tracker.departments[self.selected_department_id].remove_employee(self.selected_employee_id)
            self.refresh_members(self.tracker.departments[self.selected_department_id])
            self.selected_employee_id = None
            self.right_listbox.selection_clear(0, tk.END)
        except Exception as err:
            messagebox.showerror("Remove department member failed", str(err))
    
    def _refresh_selected_department_members(self):
        if self.selected_department_id is None:
            return
        dep = self.tracker.departments[self.selected_department_id]
        self.refresh_members(dep)


if __name__ == "__main__":
    tracker = Tracker()
    app = DepartmentWindow(None, tracker)
    app.mainloop()