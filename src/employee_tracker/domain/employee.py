from dataclasses import dataclass
from datetime import date
from employee_tracker.utils.ids import new_id
from employee_tracker.utils.value_checkers import check_new_value


class Employee:
    def __init__(self,name,role, start_date,salary,address,permissions = None):
        if not isinstance(name,str):
            raise TypeError("Name must be a string")
        if not isinstance(role,str):
            raise TypeError("Role must be a string")
        if not isinstance(start_date,date):
            raise TypeError("start_date must be a date")
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
    def change_name(self,new_name):
        if check_new_value(new_name,"name",str,self.name):
            self.name = new_name
    def change_role(self,new_role):
        if check_new_value(new_role,"role",str,self.role):
            self.role = new_role
    def change_salary(self,new_salary):
        if check_new_value(new_salary,"salary",int,self.salary):
            self.salary = new_salary
    def change_address(self,new_address):
        if check_new_value(new_address,"address",str,self.address):
            self.address = new_address
    def add_permission(self,permission):
        from employee_tracker.domain.permission import Permission
        if not isinstance(permission,Permission):
            raise TypeError("This value is not a permission, please check and try again")
        else:
            if check_new_value(permission.name,"permission",str):
                if self.permissions == None:
                    self.permissions = [permission.name]
                elif permission.name in self.permissions:
                    raise ValueError(f"{self.name} already has the permission {permission.name}, cannot add again")
                else:
                    self.permissions.append(permission.name)
    def remove_permission(self,permission):
        from employee_tracker.domain.permission import Permission
        if not isinstance(permission,Permission):
            raise TypeError("This value is not a permission, please check and try again")
        elif permission.name not in self.permissions:
            raise ValueError(f"{self.name} does not have the permission {permission.name} to remove")
        else:
            self.permissions.remove(permission.name)
    def wipe_permissions(self): 
        if self.permissions == None:
            raise ValueError("no permissions to wipe")
        elif len(self.permissions) == 0:
            raise ValueError("no permissions to wipe")
        else:
            self.permissions = []
