from dataclasses import dataclass
from employee_tracker.domain.employee import Employee
from employee_tracker.utils.ids import new_id

class Department:
    def __init__(self, name, description, head_of_department, parent_department = None, members = None):
        if not isinstance(name,str):
            raise TypeError("Name must be a string")
        if not isinstance(description,str):
            raise TypeError("Description must be a string")
        if not isinstance(head_of_department,Employee):
            raise TypeError("Head of department must be a valid Employee object")
        if not isinstance(parent_department,Department) and parent_department != None:
            raise TypeError("Parent Department must be a valid department or none")
        self.id = new_id("dep")
        self.name = name
        self.description = description
        self.head_of_department = head_of_department
        self.members = members
        self.parent_department = parent_department
    def add_employee(self,employee):
        pass