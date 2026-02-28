import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from employee_tracker.domain.tracker import Tracker
from employee_tracker.gui.new_password import PasswordDialog
from employee_tracker.gui.style import centre_window

### AI DECLARATION - ChatGPT was used in the creation of GUI elements, given the creator's lack of experience in front-end

# Parsing field inputs
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

# Employee window creation with a ttk style
class EmployeeWindow(tk.Toplevel):
    def __init__(self,parent:tk.Tk,tracker,permissions=None, logged_in_user = None):
        super().__init__(parent)
        self.tracker = tracker
        self.title("Employees")
        self.permissions = permissions or []
        self.logged_in_user = logged_in_user
        
        self.employee_ids = []
        self.selected_employee_id = None

        container = ttk.Frame(self, padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        ttk.Label(container, text="Employees", style="Title.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))

        content = ttk.Frame(container)
        content.grid(row=1, column=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        # Left: list
        left = ttk.LabelFrame(content, text="Employee list", padding=10)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(0, weight=1)

        self.listbox = tk.Listbox(left, width=35, height=14, exportselection=False)
        self.listbox.grid(row=0, column=0, sticky="nsew")
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Right: form
        right = ttk.LabelFrame(content, text="Details", padding=10)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)

        self.form_title_label = ttk.Label(right, text="Create Employee", style="Section.TLabel")
        self.form_title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        form = ttk.Frame(right)
        form.grid(row=1, column=0, sticky="ew")
        form.columnconfigure(0, weight=1)

        # Adding fields for form
        def add_field(r, label):
            ttk.Label(form, text=label).grid(row=r, column=0, sticky="w")
            entry = ttk.Entry(form)
            entry.grid(row=r + 1, column=0, sticky="ew", pady=(2, 10))
            return entry

        self.name_entry = add_field(0, "Name")
        self.role_entry = add_field(2, "Role")
        self.start_date_entry = add_field(4, "Start date (YYYY-MM-DD)")
        self.salary_entry = add_field(6, "Salary")
        self.address_entry = add_field(8, "Address")

        # Buttons
        btns = ttk.Frame(right)
        btns.grid(row=2, column=0, sticky="ew", pady=(0, 0))
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)
        btns.columnconfigure(2, weight=1)

        self.create_button = ttk.Button(btns, text="Create", style="Primary.TButton", command=self.on_create)

        self.update_button = ttk.Button(btns, text="Update", style="Primary.TButton", command=self.on_update)
        self.update_password_button = ttk.Button(btns, text="New password", command=self.update_password)
        self.delete_button = ttk.Button(btns, text="Delete", command=self.on_delete)

        self.create_button.grid(row=0, column=0, columnspan=3, sticky="ew")

        self.update_button.grid(row=0, column=0, sticky="ew")
        self.update_password_button.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        self.delete_button.grid(row=0, column=2, sticky="ew", padx=(10, 0))

        self.new_button = ttk.Button(right, text="New / Deselect", command=self.deselect_employee)
        self.new_button.grid(row=3, column=0, sticky="ew", pady=(10, 0))

        # Esc key deselects
        self.bind("<Escape>", lambda e: self.deselect_employee())

        centre_window(self, 860, 540)
        self.refresh_list()
        self.set_mode_create()

    # Applies view/edit permissions to each form field based on the
    # selected employee and the current user's role.
    def apply_parameter_permissions(self):
        view, edit = self.parameter_view_write()

        def apply(entry:tk.Entry, parameter: str, value: str):
            if parameter in view:
                self.set_entry_value(entry,value,editable=(parameter in edit))
            else:
                self.set_entry_hidden(entry)

        if self.selected_employee_id is None:
            can_create = self.has_perms(["hr_write"])
            if not can_create:
                apply(self.name_entry, "name", "")
                apply(self.role_entry, "role", "")
                apply(self.start_date_entry, "start_date", "")
                apply(self.salary_entry, "salary", "")
                apply(self.address_entry, "address", "")
                return

            self.set_entry_value(self.name_entry, "", editable=True)
            self.set_entry_value(self.role_entry, "", editable=True)
            self.set_entry_value(self.start_date_entry, "", editable=True)
            self.set_entry_value(self.salary_entry, "", editable=True)
            self.set_entry_value(self.address_entry, "", editable=True)
            return
        
        emp = self.tracker.employees[self.selected_employee_id]
        apply(self.name_entry, "name", emp.name)
        apply(self.role_entry, "role", emp.role)
        apply(self.start_date_entry, "start_date", emp.start_date.isoformat())
        apply(self.salary_entry, "salary", str(emp.salary))
        apply(self.address_entry, "address", emp.address)

    # This checks permissions and sets both read and write values
    # it_admin has all functionality
    # hr_write can do everything except master password changes
    # finance_edit can see and change salary
    # hr_read can see but not change address
    # payroll can see but not change salary
    # regular users can only see name and role of others.
    # regular users can see all their own details and change their own password
    def parameter_view_write(self):
        all_parameters = {"name", "role", "start_date", "salary", "address"}

        if self.logged_in_user is not None and self.selected_employee_id == self.logged_in_user:
            view = set(all_parameters)
        else:
            if self.has_perms(["hr_write"]):
                view = set(all_parameters)
            elif self.has_perms(["payroll","finance_edit"]):
                view = {"name", "role", "salary"}
            elif self.has_perms(["hr_read"]):
                view = {"name", "role", "address"}
            else:
                view = {"name", "role"}

        if self.has_perms(["hr_write"]):
            edit = set(all_parameters)
        elif "finance_edit" in self.permissions:
            edit = {"salary"}
        else:
            edit = set()

        return view, edit
    
    # Sets the value of an entry widget and configures whether it is editable or disabled.
    def set_entry_value(self,entry: tk.Entry, value: str, editable: bool):
        entry.config(state="normal")
        entry.delete(0,tk.END)
        entry.insert(0, value)
        entry.config(state=("normal" if editable else "disabled"))

    # Masks a field by setting its value to "Hidden" and optionally disabling editing.
    def set_entry_hidden(self,entry: tk.Entry, editable: bool = False):
        self.set_entry_value(entry, "Hidden", editable=editable)
    
    # Returns True if the user has at least one of the required permissions,
    # with "it_admin" acting as a superuser override.
    def has_perms(self,required:list) -> bool:
        if "it_admin" in self.permissions:
            return True
        return any(permission in self.permissions for permission in required)
            
    # Clearing of all input fields
    def clear_form(self):
        self.name_entry.delete(0,tk.END)
        self.role_entry.delete(0,tk.END)
        self.start_date_entry.delete(0,tk.END)
        self.salary_entry.delete(0,tk.END)
        self.address_entry.delete(0,tk.END)

    # Similar to in department window, create mode
    def set_mode_create(self):
        self.selected_employee_id = None
        self.form_title_label.config(text="Create Employee")

        self.update_button.grid_remove()
        self.update_password_button.grid_remove()
        self.delete_button.grid_remove()
        self.new_button.grid_remove()
        self.create_button.grid()
        self.apply_parameter_permissions()

    # Edit/view individual departments, changing buttons appropriately
    def set_mode_edit(self):
        self.form_title_label.config(text="Edit Employee")

        self.create_button.grid_remove()
        self.update_button.grid()
        self.update_password_button.grid()
        self.delete_button.grid()
        self.new_button.grid()
        self.apply_parameter_permissions()

    # Revert to create when deselecting
    def deselect_employee(self):
        self.listbox.selection_clear(0,tk.END)
        self.clear_form()
        self.set_mode_create()

    # Refresh method for when changes are made
    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        self.employee_ids = []
        for emp in self.tracker.list_employees():
            self.employee_ids.append(emp.id)
            self.listbox.insert(tk.END, f"{emp.id} {emp.name} ({emp.role})")

    # A method to open the update password method, checks that either it_admin permission is present, or that the user is editing themself
    def update_password(self):
        print(self.selected_employee_id,self.logged_in_user)
        emp_id = self.selected_employee_id
        if emp_id is None:
            messagebox.showerror("Update password failed","No employee selected.")
            return
        can_admin_edit = self.has_perms([])
        can_self_edit = (self.logged_in_user is not None and self.logged_in_user == emp_id)
        if not (can_admin_edit or can_self_edit):
            messagebox.showerror("Update password failed", "You do not have permission to edit this password") 
            return
        emp_id = self.selected_employee_id
        if emp_id is None:
            messagebox.showerror("Change password failed", "No employee selected.")
            return
        # launches password and captures new hash value if successful
        pass_create = PasswordDialog(self, title="Change Password")
        password = pass_create.show()
        if password is None:
            return
        
        # uses employee method to update hash 
        self.tracker.employees[emp_id].password_hash = password
        messagebox.showinfo("Updated","Password updated")

    # Creating new employee, checks that permissions exist
    def on_create(self):
        # checking for hr_write (has_perms always checks for it_admin regardless)
        if not self.has_perms(["hr_write"]):
            messagebox.showerror("Create employee failed", "You do not have permission to create an Employee")
            return
        try:
            data = parse_employee_form(
                self.name_entry.get(),
                self.role_entry.get(),
                self.start_date_entry.get(),
                self.salary_entry.get(),
                self.address_entry.get(),
            )
        except Exception as err:
            messagebox.showerror("Create employee failed",str(err))
            return

        pass_create = PasswordDialog(self, title="Set New Employee Password")
        password = pass_create.show()
        if password is None:
            return
        
        try:
            self.tracker.create_employee(password=password, **data)

            self.refresh_list()
            self.clear_form()
            self.set_mode_create()

        except Exception as err:
            messagebox.showerror("Create employee failed", str(err))
    
    # updating employee information
    def on_update(self):
        if self.selected_employee_id is None:
            messagebox.showerror("Update employee failed", "No employee selected.")
            return
        
        view, edit = self.parameter_view_write()
        if not edit:
            messagebox.showerror("Update employee failed", "You do not have permission to edit this employee.")
            return

        emp = self.tracker.employees[self.selected_employee_id]
        
        # Only update fields that have been changed
        try:
            if "name" in edit:
                name = self.name_entry.get().strip()
                if not name:
                   raise ValueError("Name is required")
                if emp.name != name:
                   emp.name = name

            if "role" in edit:
                role = self.role_entry.get().strip()
                if not role:
                   raise ValueError("Role is required")
                if emp.role != role:
                    emp.role = role
            
            if "start_date" in edit:
                try:
                    if emp.start_date != date.fromisoformat(self.start_date_entry.get().strip()):
                        emp.start_date = date.fromisoformat(self.start_date_entry.get().strip())
                except ValueError as err:
                    raise ValueError("Start date must be YYYY-MM-DD") from err
                
            if "salary" in edit:
                try:
                    if emp.salary != int(self.salary_entry.get().strip()):
                        emp.salary = int(self.salary_entry.get().strip())
                except ValueError as err:
                    raise ValueError("Salary must be an integer") from err
                
            if "address" in edit:
                address = self.address_entry.get().strip()
                if not address:#
                    raise ValueError("Address is required")
                if emp.address != address:#
                    emp.address = address
            
            self.refresh_list()

            try:
                idx = self.employee_ids.index(self.selected_employee_id)
                self.listbox.selection_set(idx)
                self.listbox.activate(idx)
                messagebox.showinfo("Updated","Employee file updated.")
            except ValueError:
                pass

        except Exception as err:
            messagebox.showerror("Update employee failed", str(err))

    # remove employee, checking permissions
    def on_delete(self):
        if not self.has_perms(["hr_write"]):
            messagebox.showerror("Delete employee failed", "You do not have permission to delete employees.")
            return
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

    # switching to edit mode when employee created
    def on_select(self,event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.set_mode_create()
            return
        
        idx = sel[0]
        self.selected_employee_id = self.employee_ids[idx]
        self.set_mode_edit()
    
    def refresh(self):
        self.refresh_list()
        self.deselect_employee()

# for use when loaded independently
if __name__ == "__main__":
    tracker = Tracker()
    root = tk.Tk()
    app = EmployeeWindow(root, tracker, permissions = [], logged_in_user = None)
    app.mainloop()