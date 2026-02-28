import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from employee_tracker.domain.tracker import Tracker
from employee_tracker.utils.ids import check_id
from employee_tracker.gui.add_members_window import AddMembersWindow
from employee_tracker.gui.style import centre_window

# Function for error handling of fields for creation of new departments. This is in addition to the validation in the Department constructor
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


# ttk window creation passing in tracker, user and permissions
class DepartmentWindow(tk.Toplevel):
    def __init__(self,parent:tk.Tk,tracker, permissions, logged_in_user):
        super().__init__(parent)
        self.tracker = tracker
        self.title("Department")
        self.permissions = permissions or []
        self.logged_in_user = logged_in_user
        
        self.department_ids = []
        self.member_employee_ids = []
        self.selected_department_id = None
        self.selected_employee_id = None

        # Creation of master frame
        container = ttk.Frame(self, padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        ttk.Label(container, text="Departments", style="Title.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Main content frame
        content = ttk.Frame(container)
        content.grid(row=1, column=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=2)
        content.columnconfigure(2, weight=2)
        content.rowconfigure(0, weight=1)

        # Left: department list
        left = ttk.LabelFrame(content, text="Departments", padding=10)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(0, weight=1)

        self.listbox = tk.Listbox(left, width=35, height=14, exportselection=False)
        self.listbox.grid(row=0, column=0, sticky="nsew")
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Centre: form
        centre = ttk.LabelFrame(content, text="Details", padding=10)
        centre.grid(row=0, column=1, sticky="nsew", padx=(0, 12))
        centre.columnconfigure(0, weight=1)

        self.form_title_label = ttk.Label(centre, text="Create Department", style="Section.TLabel")
        self.form_title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        form = ttk.Frame(centre)
        form.grid(row=1, column=0, sticky="ew")
        form.columnconfigure(0, weight=1)

        # Function to populate form fields

        def add_field(r, label):
            ttk.Label(form, text=label).grid(row=r, column=0, sticky="w")
            entry = ttk.Entry(form)
            entry.grid(row=r + 1, column=0, sticky="ew", pady=(2, 10))
            return entry

        self.name_entry = add_field(0, "Name")
        self.description_entry = add_field(2, "Description")
        self.head_of_department_entry = add_field(4, "Head of Department (emp####)")
        self.parent_department_entry = add_field(6, "Parent Department (dep####)")

        # Buttons
        btns = ttk.Frame(centre)
        btns.grid(row=2, column=0, sticky="ew", pady=(0, 0))
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)

        self.create_button = ttk.Button(btns, text="Create", style="Primary.TButton", command=self.on_create)
        self.update_button = ttk.Button(btns, text="Update", style="Primary.TButton", command=self.on_update)
        self.delete_button = ttk.Button(btns, text="Delete", command=self.on_delete)

        self.create_button.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.update_button.grid(row=0, column=0, sticky="ew")
        self.delete_button.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        self.new_button = ttk.Button(centre, text="New / Deselect", command=self.deselect_department)
        self.new_button.grid(row=3, column=0, sticky="ew", pady=(10, 0))

        # Right: members
        right = ttk.LabelFrame(content, text="Department Members", padding=10)
        right.grid(row=0, column=2, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)

        self.right_listbox = tk.Listbox(right, width=35, height=14, exportselection=False)
        self.right_listbox.grid(row=0, column=0, sticky="nsew")
        self.right_listbox.bind("<<ListboxSelect>>", self.on_select_member)

        member_btns = ttk.Frame(right)
        member_btns.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        member_btns.columnconfigure(0, weight=1)
        member_btns.columnconfigure(1, weight=1)

        # Buttons to add and remove members, both calling methods
        self.add_members_button = ttk.Button(member_btns, text="Add members", command=self.open_add_members_window)
        self.remove_member_button = ttk.Button(member_btns, text="Remove member", command=self.on_remove_member)
        self.add_members_button.grid(row=0, column=0, sticky="ew")
        self.remove_member_button.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        self.bind("<Escape>", lambda e: self.deselect_department())

        centre_window(self, 980, 520)
        self.refresh_list()
        self.set_mode_create()

    # Permission checker
    def has_perms(self,add_employee = False) -> bool:
        # First checks if it_admin or hr_write (super permissions) are presnt
        if any(p in self.permissions for p in ["it_admin", "hr_write"]):
            return True
        if add_employee:
            # Then, for add employee, checks if the logged in user is the department head
            if self.selected_department_id is None:
                return False
            dep = self.tracker.departments.get(self.selected_department_id)
            if dep is None:
                return False
            return dep.head_of_department == self.logged_in_user
        return False

    # Clears the form of text
    def clear_form(self):
        self.name_entry.delete(0,tk.END)
        self.description_entry.delete(0,tk.END)
        self.head_of_department_entry.delete(0,tk.END)
        self.parent_department_entry.delete(0,tk.END)

    # Switches from viewing details of existing departments to a form to create a new one
    def set_mode_create(self):
        self.selected_department_id = None
        self.form_title_label.config(text="Create Department")

        self.update_button.grid_remove()
        self.delete_button.grid_remove()
        self.new_button.grid_remove()
        self.create_button.grid()

        self.right_listbox.delete(0, tk.END)
        self.member_employee_ids = []
        self.selected_employee_id = None

    # Switches back to viewing and editing (with permission) departments
    def set_mode_edit(self):
        self.form_title_label.config(text="Edit Department")

        self.create_button.grid_remove()
        self.update_button.grid()
        self.delete_button.grid()
        self.new_button.grid()

    # When no department is selected, create mode is the default
    def deselect_department(self):
        self.listbox.selection_clear(0,tk.END)
        self.clear_form()
        self.set_mode_create()

    # When the list changes (new addition or edit/delete), the list is refreshed to stay current
    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        self.department_ids = []
        for dep in self.tracker.list_departments():
            self.department_ids.append(dep.id)
            self.listbox.insert(tk.END, f"{dep.id} {dep.name} ({dep.description})")

    # Similar to the above, but for the list of employees in a department
    def refresh_members(self, dep):
        self.right_listbox.delete(0, tk.END)
        self.member_employee_ids = []
        self.selected_employee_id = None

        for emp_id in (dep.members or []):
            emp = self.tracker.employees.get(emp_id)
            if emp is None:
                # error handling for a listed employee id that doesn't exist
                self.member_employee_ids.append(emp_id)
                self.right_listbox.insert(tk.END, f"{emp_id} (missing employee)")
            else:
                self.member_employee_ids.append(emp.id)
                self.right_listbox.insert(tk.END, f"{emp.id} {emp.name} ({emp.role})")
       
    
    # Called when finished entering details for a new department, and create is clicked
    def on_create(self):

        #Error handling for lack of permissions
        if not self.has_perms():
            messagebox.showerror("Create department failed", "You do not have permission to create a department")
            return
        
        # Parse input
        try:
            data = parse_department_form(
                self.name_entry.get(),
                self.description_entry.get(),
                self.head_of_department_entry.get(),
                self.parent_department_entry.get(),
            )

            # utlise create department method in tracker, before refreshing list, clearing form and reverting to create
            self.tracker.create_department(**data)

            self.refresh_list()
            self.clear_form()
            self.set_mode_create()

        except Exception as err:
            messagebox.showerror("Create department failed",str(err))
    
    # Update method with error handling as in above method
    def on_update(self):
        if not self.has_perms():
            messagebox.showerror("Update department failed", "You do not have permission to edit a department")
            return
        # Error handling if deselected
        if self.selected_department_id is None:
            messagebox.showerror("Update department failed", "No department selected.")
            return
        
        dep = self.tracker.departments[self.selected_department_id]

        try:
            data = parse_department_form(
                self.name_entry.get(),
                self.description_entry.get(),
                self.head_of_department_entry.get(),
                self.parent_department_entry.get()
            )
            # Only the fields that have been changed are updated, preventing any data from being overwritten by itself unnecessarily
            if dep.name != data["name"]:
                dep.name = data["name"]

            if dep.description != data["description"]:
                dep.description = data["description"]

            if dep.head_of_department != data["head_of_department"]:
                dep.head_of_department = data["head_of_department"]

            if dep.parent_department != data["parent_department"]:
                dep.parent_department = data["parent_department"]

            self.refresh_list()

            try:
                idx = self.department_ids.index(self.selected_department_id)
                self.listbox.selection_set(idx)
                self.listbox.activate(idx)
            except ValueError:
                pass
            # Refreshes members and sets mode to edit
            self.set_mode_edit()
            self.refresh_members(dep)

        except Exception as err:
            messagebox.showerror("Update department failed", str(err))

    # Delete department with similar error handling to above
    def on_delete(self):
        if not self.has_perms():
            messagebox.showerror("Delete department failed", "You do not have permission to delete a department")
            return
        
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

    # When a department is selected, its info is shown in form fields, and employees are listed
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

    # add members window is opened with correct inputs
    def open_add_members_window(self):
        if not self.has_perms(add_employee=True):
            messagebox.showerror("Add members", "You do not have permission to add members to this department.")
            return
        if self.selected_department_id is None:
            messagebox.showerror("Add members","Select a department first.")
            return
        # when add members reports "on_done", list is refreshed with new data
        AddMembersWindow(
            parent=self,
            tracker=self.tracker,
            dep_id=self.selected_department_id,
            on_done=self._refresh_selected_department_members
        )

    # selecting an employee prepares in case of using delete
    def on_select_member(self,event=None):
        sel = self.right_listbox.curselection()
        if not sel:
            self.selected_employee_id = None
            return
    
        idx = sel[0]
        self.selected_employee_id = self.member_employee_ids[idx]

    # remove employee calling tracker method, with error handling for permissions and missing data
    def on_remove_member(self):
        print(self.logged_in_user,self.tracker.departments[self.selected_department_id].head_of_department)
        if not self.has_perms(add_employee=True):
            messagebox.showerror("Remove member failed", "You do not have permission to remove members from this department.")
            return
        if self.selected_department_id is None:
            messagebox.showerror("Remove member failed", "No department selected")
            return
        if self.selected_employee_id is None:
            messagebox.showerror("Remove department member failed", "No employee selected.")
            return
        # user is asked for confirmation
        if not messagebox.askyesno("Confirm removal", "Remove this employee from the department?"):
            return
        
        try:
            # tracker method called, list refreshed and selected employee reset
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
    def refresh(self):
        self.refresh_list()
        self.deselect_department()

# For use when window is opened independently
if __name__ == "__main__":
    tracker = Tracker()
    root = tk.Tk()
    root.withdraw()
    app = DepartmentWindow(root, tracker, logged_in_user="emp0001", permissions=[])
    app.mainloop()