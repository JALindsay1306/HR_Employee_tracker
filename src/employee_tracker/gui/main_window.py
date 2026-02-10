import tkinter as tk

from employee_tracker.domain.tracker import Tracker
from employee_tracker.gui.employee_window import EmployeeWindow


class MainWindow:
    def __init__(self,tracker:Tracker):
        self.tracker = tracker
        self.root = tk.Tk()
        self.root.title("HR Employee Tracker")

        tk.Label(self.root,text="HR Employee Tracker", font=("Sans Serif", 15)).pack(pady=10)

        tk.Button(self.root,text="Employees",width=20, command=self.open_employees).pack(pady=5)
        tk.Button(self.root, text="Departments", width=20,command=self.open_departments).pack(pady=5)

        tk.Button(self.root, text="Quit",width=20, command=self.root.destroy).pack(pady=15)

    def open_employees(self):
        EmployeeWindow(self.root,self.tracker)
    def open_departments(self):
        pass
    def run(self):
        self.root.mainloop()

def run_app():
    tracker = Tracker()
    MainWindow(tracker).run()

run_app()