from employee_tracker.domain.department import Department
from employee_tracker.utils.ids import check_id

class Permission:
    def __init__(self,name,department = None):
        if not isinstance(name,str):
            raise TypeError("Name must be a string")
        if (not isinstance(department,str)) and (department != None):
            raise TypeError("department must be a str")
        self.name = name
        self.department = department
    def change_name(self,new_name):
        if not isinstance(new_name,str):
            raise TypeError("name must be a string")
        elif new_name == self.name:
            raise ValueError(f"name is already {new_name}")
        self.name = new_name
    def list_departments(self):
        pass
    def add_department(self,new_department):
        if not isinstance(new_department,Department):
            raise TypeError("department must be a Department")
        elif not check_id(new_department.id,"dep"):
            raise ValueError("invalid ID")
        elif new_department.id == self.department:
            raise ValueError(f"{new_department.name} is already the department, cannot replace with itself")
        self.department = new_department.id
    def remove_department(self):
        if self.department == None:
            raise ValueError("no department to remove")
        self.department = None
