from dataclasses import dataclass
from employee_tracker.domain.employee import Employee
from employee_tracker.utils.ids import new_id
from employee_tracker.utils.ids import check_id

class Department:
    def __init__(self, name, description, head_of_department, parent_department = None, members = None,id = None):
        if not isinstance(name,str):
            raise TypeError("Name must be a string")
        if not isinstance(description,str):
            raise TypeError("Description must be a string")
        if not isinstance(head_of_department,str):
            raise TypeError("Head of department must be a string")
        if not isinstance(parent_department,str) and parent_department != None:
            raise TypeError("Parent Department must be a str or none")
        if id == None:
            self.id = new_id("dep")
            
        else:
            if check_id(id,"dep"):
                self.id = id
            else:
                raise TypeError("Invalid ID")
        self.name = name
        self.description = description
        self.head_of_department = head_of_department
        self.members = [] if members == None else members
        self.parent_department = parent_department
    def list_employees(self):
        if len(self.members) == 0:
            raise ValueError("No employees in department")
        return self.members
    def add_employee(self,employee):
        if not isinstance (employee,Employee):
            raise TypeError("Must be a valid Employee object")#
        elif employee.id in self.members:
            raise ValueError(f"Employee ID {employee.id} already in {self.name}, cannot add again")
        self.members.append(employee.id)
    def remove_employee(self,employee_id):
        if not check_id(employee_id,"emp"):
            raise ValueError("invalid ID")
        elif employee_id not in self.members:
            raise ValueError(f"{employee_id} not in department, cannot remove")          
        else:
            self.members.remove(employee_id)
            if len(self.members) == 0:
                return "Last employee removed, department empty"
    def update_name(self,new_name):
        if not isinstance(new_name,str):
            raise TypeError("name must be a string")
        else:
            self.name = new_name
    def update_description(self,new_description):
        if not isinstance(new_description,str):
            raise TypeError("description must be a string")
        else:
            self.description = new_description
    def change_head_of_department(self,new_head):
         if not isinstance(new_head,Employee):
             raise TypeError("head of department must be an employee")
         if not check_id(new_head.id,"emp"):
            raise ValueError("invalid ID")
         elif new_head.id == self.head_of_department:
             raise ValueError(f"{new_head.name} ({new_head.id}) is already head of department")
         else:
             self.head_of_department = new_head.id
    def set_parent_department(self,new_dep):
        if not isinstance(new_dep,Department):
            raise TypeError("parent department must be a department")
        elif not check_id(new_dep.id,"dep"):
            raise ValueError("invalid ID")
        elif new_dep.id == self.parent_department:
            raise ValueError(f"{new_dep.name} ({new_dep.id}) is already the parent department")
        else:
            self.parent_department = new_dep.id
    def remove_parent_department(self):
        if self.parent_department == None:
            raise ValueError(f"{self.name} has no parent department to remove")
        self.parent_department = None
    def to_row(self):
        return {
            "id":self.id,
            "name":self.name,
            "description":self.description,
            "head_of_department":self.head_of_department,
            "parent_department":self.parent_department,
            "members":" ".join(self.members) 
        }
    @classmethod
    def from_row(cls, row: dict) -> "Department":
        
        mems = row.get("members", "")
        members = mems.split() if mems else []

        return cls(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            head_of_department=row["head_of_department"],
            parent_department=row["parent_department"],
            members=members,
        )