from employee_tracker.domain.employee import Employee
from employee_tracker.domain.department import Department
from employee_tracker.domain.permission import Permission

class Tracker:
    def __init__(self):
        self.employees = {}
        self.departments = {}
        self.permissions = {}
    def create_employee(self,name,role, start_date,salary,address,permissions = None):
        emp = Employee(name,role,start_date,salary,address,permissions)
        self.employees[emp.id] = emp
        return emp