import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from employee_tracker.domain.tracker import Tracker
from employee_tracker.gui.employee_window import EmployeeWindow
from employee_tracker.gui.department_window import DepartmentWindow
from employee_tracker.gui.login_window import LoginWindow
from employee_tracker.gui.style import apply_style, centre_window

# Top level window
### AI DECLARATION - ChatGPT was used in the creation of GUI elements, given the creator's lack of experience in front-end
class MainWindow:
    def __init__(self,tracker:Tracker):
        self.tracker = tracker
        self.active_emp_id = None
        self.active_permissions = []
        self._child_windows = []

        self.root = tk.Tk()
        self.root.title("HR Employee Tracker")

        # Ensure style is applied
        apply_style(self.root)
        centre_window(self.root,420,420)

        container = ttk.Frame(self.root, padding=18)
        container.grid(row=0, column=0,sticky="nsew")
        self.root.rowconfigure(0,weight=1)
        self.root.columnconfigure(0,weight=1)

        container.columnconfigure(0,weight=1)

        ttk.Label(container,text="HR Employee Tracker", style="Title.TLabel").grid(row=0,column=0,sticky="w")

        self.status_var = tk.StringVar(value="Not signed in")
        ttk.Label(container, textvariable=self.status_var).grid(row=1,column=0,sticky="w",pady=(2,14))

        actions = ttk.LabelFrame(container, text="Actions", padding=12)
        actions.grid(row=2, column=0, sticky="ew")
        actions.columnconfigure(0,weight=1)

        # Links to open other windows
        self.btn_employees = ttk.Button(actions, text="Employees", command=self.open_employees)
        self.btn_departments = ttk.Button(actions, text="Departments", command=self.open_departments)
        
        self.btn_employees.grid(row=0,column=0, sticky="ew", pady=(0,8))
        self.btn_departments.grid(row=1,column=0,sticky="ew")

        storage = ttk.LabelFrame(container, text="Storage", padding=12)
        storage.grid(row=3, column=0, sticky="ew", pady=(12,0))
        storage.columnconfigure(0,weight=1)
        storage.columnconfigure(1,weight=1)

        self.btn_load = ttk.Button(storage, text="Load", command=self.load)
        self.btn_save = ttk.Button(storage, text="Save", command=self.save)
        self.btn_load.grid(row=0, column=0, sticky="ew")
        self.btn_save.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        session = ttk.Frame(container)
        session.grid(row=4, column=0, sticky="ew", pady=(18, 0))
        session.columnconfigure(0, weight=1)
        session.columnconfigure(1, weight=1)

        self.btn_logout = ttk.Button(session, text="Logout", command=self.logout)
        self.btn_quit = ttk.Button(session, text="Quit", command=self.root.destroy)
        self.btn_logout.grid(row=0, column=0, sticky="ew")
        self.btn_quit.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        # Login is automatically false, and login window is called
        self.set_logged_in(False)
        self.root.after(0,self.show_login)

    # When login window is successfully used, buttons are enabled
    def set_logged_in(self,is_logged_in:bool):
        state = "normal" if is_logged_in else "disabled"
        self.btn_employees.config(state=state)
        self.btn_departments.config(state=state)
        self.btn_load.config(state=state)
        self.btn_save.config(state=state)

    # Logging out disables buttons and resets window
    def logout(self):
        self.logged_in_user = None
        self.active_permissions = []
        self.root.title("HR Employee Tracker")
        self.status_var.set("Not signed in")
        self.set_logged_in(False)
        self.root.after(0,self.show_login)

    # Opens login
    def show_login(self):
        LoginWindow(self.root, self.tracker,self.on_login_success)

    # Window is refreshed when a new user logs in, permissions are stored ready for usage by other windows
    def on_login_success(self, permissions, emp_id):
        self.active_permissions = permissions or []
        self.logged_in_user = emp_id
        self.set_logged_in(True)

        self.root.title(f"HR Employee Tracker - Logged in as {emp_id}")
        perms = ", ".join(self.active_permissions) if self. active_permissions else "none"
        self.status_var.set(f"signed in as {emp_id} - Permissions: {perms}")

    # opening employees as a child window, ensuring part of the same app
    def open_employees(self):
        win = EmployeeWindow(self.root,self.tracker,self.active_permissions,self.logged_in_user)
        self._track_child(win)

    # opening departments as a child window, ensuring part of the same app
    def open_departments(self):
        win = DepartmentWindow(self.root,self.tracker,self.active_permissions,self.logged_in_user)
        self._track_child(win)

    # Calls load function within tracker. Also updates all child windows with new information
    def load(self):
        try:
            self.tracker.reload_from_storage()
            for w in list(self._child_windows):
                if hasattr(w, "refresh"):
                    w.refresh()
            messagebox.showinfo("Loaded", "Data loaded successfully")
        except Exception as err:
            messagebox.showerror("Load Error", err)

    # calls save method of tracker
    def save(self):
        try:
            self.tracker.save_to_storage()
            messagebox.showinfo("Saved", "Data saved successfully")
        except Exception as err:
            messagebox.showerror("Save Error", err)
    
    # tk run
    def run(self):
        self.root.mainloop()
    
    # Part of ensuring loaded changes are viewed by child windows
     ### AI Declaration - track_child was added as a suggestion from an LLM. Helping to create a seamless app where data can be loaded to everywhere
    def _track_child(self, w):
        self._child_windows.append(w)
        w.bind("<Destroy>", lambda e, win=w: self._untrack_child(win))

    def _untrack_child(self, win):
        self._child_windows = [w for w in self._child_windows if w is not win]

def run_app():
    # uses load_or_create to account for missing data
    tracker = Tracker.load_or_create_sample()
    MainWindow(tracker).run()

if __name__ == "__main__":
    run_app()