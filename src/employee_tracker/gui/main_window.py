import tkinter as tk

from employee_tracker.domain.tracker import Tracker
from employee_tracker.gui.employee_window import EmployeeWindow
from employee_tracker.gui.department_window import DepartmentWindow


class MainWindow:
    def __init__(self,tracker:Tracker):
        self.tracker = tracker
        self.root = tk.Tk()
        self.root.title("HR Employee Tracker")

        tk.Label(self.root,text="HR Employee Tracker", font=("Sans Serif", 15)).pack(pady=10)

        tk.Button(self.root,text="Employees",width=20, command=self.open_employees).pack(pady=5)
        tk.Button(self.root, text="Departments", width=20,command=self.open_departments).pack(pady=5)

        tk.Button(self.root, text="Load",width=20, command=self.load).pack(pady=15)
        tk.Button(self.root, text="Save",width=20, command=self.save).pack(pady=15)
        tk.Button(self.root, text="Quit",width=20, command=self.root.destroy).pack(pady=15)

    def open_employees(self):
        EmployeeWindow(self.root,self.tracker)
    def open_departments(self):
        DepartmentWindow(self.root,self.tracker)
    def load(self):
        self.tracker = Tracker.load_from_storage()
    def save(self):
        self.tracker.save_to_storage()
    def run(self):
        self.root.mainloop()

def run_app():
    tracker = Tracker.load_or_create_sample()
    MainWindow(tracker).run()

run_app()