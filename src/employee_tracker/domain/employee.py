from dataclasses import dataclass
from datetime import date
from employee_tracker.utils.ids import new_id
from employee_tracker.utils.value_checkers import check_new_value
from employee_tracker.utils.ids import check_id
from employee_tracker.utils.passwords import hash_password, is_valid_stored_password_hash
import pandas as pd

class Employee:
    # Class initilisation with type validations. Mostly strings except date for start_date and integer for salary
    # Optional arguments for password and password_hash (which then decides if new password hash should be made)
    # Optional argument for id, to aid in loading from storage
    def __init__(self,name:str,role:str, start_date:date,salary:int,address:str,password:str=None,permissions:list = None,id:str = None,password_hash:str=None ):
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
        # Creation of new ID if none exists. If one does exist, it's validated with a utility
        if id == None:
            self.id = new_id("emp")    
        else:
            if check_id(id,"emp"):
                self.id = id
            else:
                raise TypeError("Invalid ID")
        self._name = name
        self._role = role
        self._start_date = start_date
        # Assignment of permissions to an empty list if nothing is passed in
        self._permissions = permissions or []
        self._salary = salary
        self._address = address
        # Any passed hash is checked against the hashing method to validate that it was created by this program
        if password_hash:
            if is_valid_stored_password_hash(password_hash):
                self._password_hash = password_hash
        else:
            # If only a password is passed, then it is hashed before storing, the password itself is never stored
            self._password_hash = hash_password(password)
        self._enabled = True
    # These two methods were built with future functionality in mind. They are both tested but as yet not utilised
    def salary_bump(self,uplift_percentage):
        self.salary = round(self.salary * (1 + uplift_percentage/100))
    def enable_disable(self):
        self.enabled = not self.enabled
    # Properties are obfuscated to give opportunities to hide if necessary
    # This was originally planned to be part of permissions, but that functionality was moved the GUI level
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,new_name):
        #value setters validate as in init
        if check_new_value(new_name,"name",str,self._name):
            self._name = new_name
    @property
    def role(self):
        return self._role
    @role.setter
    def role(self,new_role):
        if check_new_value(new_role,"role",str,self._role):
            self._role = new_role
    @property
    def salary(self):
        return self._salary
    @salary.setter
    def salary(self,new_salary):
        if check_new_value(new_salary,"salary",int,self._salary):
            self._salary = new_salary
    @property
    def address(self):
        return self._address
    @address.setter
    def address(self,new_address):
        if check_new_value(new_address,"address",str,self._address):
            self._address = new_address
    @property
    def start_date(self):
        return self._start_date
    @start_date.setter
    def start_date(self,new_start_date):
        self._start_date = new_start_date
    @property
    def enabled(self):
        return self._enabled
    @enabled.setter
    def enabled(self,new_enabled):
        self._enabled = new_enabled
    @property
    def permissions(self):
        return self._permissions
    # Currently permissions are hard set, the initial plan was to utilise this method to add and remove them, but currently this isn't part of the GUI
    @permissions.setter
    def permissions(self,new_permissions):
        self._permissions = new_permissions
    def add_permission(self,permission):
        # Permission class is imported to aid in validation
        from employee_tracker.domain.permission import Permission
        if not isinstance(permission,Permission):
            raise TypeError("This value is not a permission, please check and try again")
        else:
            #Util to check for repeat values is called here
            if check_new_value(permission.name,"permission",str):
                if self.permissions == None:
                    self.permissions = [permission.name]
                elif permission.name in self.permissions:
                    raise ValueError(f"{self.name} already has the permission {permission.name}, cannot add again")
                else:
                    self.permissions.append(permission.name)
    @property
    def password_hash(self):
        return self._password_hash
    @password_hash.setter
    def password_hash(self,new_password):
        # New password setting calls hash_password
        self._password_hash = hash_password(new_password)
    def remove_permission(self,permission):
        # Again, Permissions is used for validation
        from employee_tracker.domain.permission import Permission
        if not isinstance(permission,Permission):
            raise TypeError("This value is not a permission, please check and try again")
        elif permission.name not in self.permissions:
            raise ValueError(f"{self.name} does not have the permission {permission.name} to remove")
        else:
            self.permissions.remove(permission.name)
    def wipe_permissions(self): 
        # This is a quick function to remove all permissions at once rather than one by one
        if self.permissions == None:
            raise ValueError("no permissions to wipe")
        elif len(self.permissions) == 0:
            raise ValueError("no permissions to wipe")
        else:
            self.permissions = []
    def to_row(self):
        # This function prepares the object for storage
        return {
            "id":self.id,
            "name":self.name,
            "role":self.role,
            "start_date":self.start_date,
            "salary":self.salary,
            "address":self.address,
            "password_hash":self.password_hash,
            #Permissions are joined by a space, to avoid being broken up in a csv
            "permissions":" ".join(self.permissions) 
        }
    #Class method to load from storage, so it can be called before the object exists
    @classmethod
    def from_row(cls, row: dict) -> "Employee":
        start_date = row["start_date"]
        if isinstance(start_date, pd.Timestamp):
            start_date = start_date.date()

        #Permissions are re-organised into a list
        perms = row.get("permissions", "")
        permissions = perms.split() if perms else []

        return cls(
            id=row["id"],
            name=row["name"],
            role=row["role"],
            start_date=start_date,
            salary=int(row["salary"]),
            address=row["address"],
            password_hash=row["password_hash"],
            permissions=permissions,
        )