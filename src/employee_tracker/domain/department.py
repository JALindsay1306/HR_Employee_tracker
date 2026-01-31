from dataclasses import dataclass
from employee_tracker.domain.employee import Employee
from employee_tracker.utils.ids import new_id

class Department:
    def __init__(self, name, description, head_of_department, members = None):
        if not isinstance(name,str):
            raise TypeError("Name must be a string")
        if not isinstance(description,str):
            raise TypeError("Description must be a string")
        if not isinstance(head_of_department,Employee):
            raise TypeError("Head of department must be a valid Employee object")
        self.id = new_id("dep")
        self.name = name
        self.description = description
        self.head_of_department = head_of_department
        self.members = members
    def add_employee(self,employee):
        pass