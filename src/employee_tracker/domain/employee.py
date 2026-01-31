from dataclasses import dataclass
from datetime import date
from employee_tracker.utils.ids import new_id

class Employee:
    def __init__(self,name,role, start_date,salary,address,permissions = None, enabled = True):
        if not isinstance(name,str):
            raise TypeError("Name must be a string")
        if not isinstance(role,str):
            raise TypeError("Role must be a string")
        if not isinstance(salary,int):
            raise TypeError("Salary must be an integer")
        if not isinstance(address,str):
            raise TypeError("Address must be a string")
        self.id = new_id("emp")
        self.name = name
        self.role = role
        self.start_date = start_date
        self.permissions = permissions
        self.salary = salary
        self.address = address
        self.enabled = True
    def salary_bump(self,uplift_percentage):
        self.salary = round(self.salary * (1 + uplift_percentage/100))
    def enable_disable(self):
        self.enabled = not self.enabled