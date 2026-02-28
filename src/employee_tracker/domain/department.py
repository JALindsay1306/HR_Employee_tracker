from dataclasses import dataclass
from employee_tracker.domain.employee import Employee
from employee_tracker.utils.ids import new_id
from employee_tracker.utils.ids import check_id

class Department:
    # initialise with name description as strings. Head of department should be an employee ID of an existing employee
    # Parent department does not currently have functionality, but plans are to incorporate this into the permissions structure (someone with the permissions to edit a department should be able to edit that department's children)
    # Members is a list of employee IDs showing who is in the department#
    # When creating a department, the ID is automatically generated following a set pattern but with a random hexidecimal indentifier
    # ID is available as an argument to allow for loading from storage, where because of relationships with other classes, this parameter should not change
    def __init__(self, name: str, description: str, head_of_department: str, parent_department: str = None, members: list = None,id: str = None):
        #Input validations, mostly reinforcing from arguments that these should be strings   
        if not isinstance(name,str):
            raise TypeError("Name must be a string")
        if not isinstance(description,str):
            raise TypeError("Description must be a string")
        # IDs of other classes are not checked here, but in the tracker module where there is more visibility
        if not isinstance(head_of_department,str):
            raise TypeError("Head of department must be a string")
        if not isinstance(parent_department,str) and parent_department != None:
            raise TypeError("Parent Department must be a str or none")  
        # If there is not an ID passed (when loading from storage) then a separate utility is called to create one in a standard format
        if id == None:
            self.id = new_id("dep")
        else:
            # If an ID is passed, then another utility checks its validity. This doesn't check whether it exists as an entity, but rather that the id is in the correct format
            if check_id(id,"dep"):
                self.id = id
            else:
                raise TypeError("Invalid ID")
        self._name = name
        self._description = description
        self._head_of_department = head_of_department
        #Members should default to None if none are added
        self._members = [] if members == None else members
        self._parent_department = parent_department
    #Properties are obfuscated to ensure control over access
    @property
    def members(self):
        return self._members
    # Same with setting of properties, this allows for controlling setting properties in certain circumstances
    # This was initially intended to be used as part of permission management, but ultimately that functionality was moved to the GUI level
    @members.setter
    def members(self,new_members):
        #passed list is validated as a list of employee ids
        if not isinstance(new_members,list):
            raise TypeError("members must be a list of employees")
        # Each ID checked for validity
        for id in new_members:
            if not check_id(id,"emp"):
                raise ValueError("all items in list should be valid employee ids")
        self._members = new_members
    def list_employees(self):
        if len(self._members) == 0:
            raise ValueError("No employees in department")
        return self._members
    def add_employee(self,employee):
        #validates employee before appending id (only id is kept in department object)
        if not isinstance (employee,Employee):
            raise TypeError("Must be a valid Employee object")
        # An employee can't be added to a department if they are already in it
        elif employee.id in self._members:
            raise ValueError(f"Employee ID {employee.id} already in {self.name}, cannot add again")
        self.members.append(employee.id)
    def remove_employee(self,employee_id):
        #validates id before removing employee if in members
        if not check_id(employee_id,"emp"):
            raise ValueError("invalid ID")
        elif employee_id not in self.members:
            raise ValueError(f"{employee_id} not in department, cannot remove")          
        else:
            # This message is not currently used, but I added this in to have ease of addition later
            self.members.remove(employee_id)
            if len(self.members) == 0:
                return "Last employee removed, department empty"
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,new_name):
        if not isinstance(new_name,str):
            raise TypeError("name must be a string")
        else:
            self._name = new_name
    @property
    def description(self):
        return self._description
    @description.setter
    def description(self,new_description):
        if not isinstance(new_description,str):
            raise TypeError("description must be a string")
        else:
            self._description = new_description
    @property
    def head_of_department(self):
        return self._head_of_department
    @head_of_department.setter
    def head_of_department(self,new_head_of_department):
        self._head_of_department = new_head_of_department

    def change_head_of_department(self,new_head):
         # Similar checks to adding employees (validating type and ID)
         if not isinstance(new_head,Employee):
             raise TypeError("head of department must be an employee")
         if not check_id(new_head.id,"emp"):
            raise ValueError("invalid ID")
         # Head of department can't be replaced with themselves
         elif new_head.id == self.head_of_department:
             raise ValueError(f"{new_head.name} ({new_head.id}) is already head of department")
         else:
             self.head_of_department = new_head.id

    @property
    def parent_department(self):
        return self._parent_department
    @parent_department.setter
    def parent_department(self,new_parent_department):
        self._parent_department = new_parent_department
    def set_parent_department(self,new_dep):
        # More type and ID checks before setting
        if not isinstance(new_dep,Department):
            raise TypeError("parent department must be a department")
        elif not check_id(new_dep.id,"dep"):
            raise ValueError("invalid ID")
        # A parent department can't be replaced with itself
        elif new_dep.id == self.parent_department:
            raise ValueError(f"{new_dep.name} ({new_dep.id}) is already the parent department")
        else:
            self.parent_department = new_dep.id
    def remove_parent_department(self):
        # Checks that there is a parent_department to remove first
        if self.parent_department == None:
            raise ValueError(f"{self.name} has no parent department to remove")
        self.parent_department = None
    def to_row(self):
        # Preparation of class for storage, including joining members by space
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
        # Class method so this can be called before a class object exists (it creates the object itself)
        # This is used so that a new class object can be created whilst forcing it to accept an ID that it cannot set itself
        
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