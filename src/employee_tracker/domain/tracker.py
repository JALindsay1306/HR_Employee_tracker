from employee_tracker.domain.employee import Employee
from employee_tracker.domain.department import Department
from employee_tracker.domain.permission import Permission
from employee_tracker.domain.user import User
from employee_tracker.utils.ids import check_id
from employee_tracker.utils.filtering import filter_list
from employee_tracker.storage.storage import create_dataframe, read_csv, write_csv
from employee_tracker.utils.passwords import hash_password
from typing import Dict

class Tracker:
    def __init__(self):
        #No Arguments are passed in, but properties are made with clear expectations of what they will contain
        self.employees: Dict[str,Employee] = {}
        self.departments: Dict[str,Department] = {}
        self.permissions: Dict[str,Permission] = {}
        self.users: Dict[str,User] = {}

    # Method to call Employee constructor, types aren't enforced here as that happens in the constructor
    def create_employee(self,name,role, start_date,salary,address,permissions = None,password=None,password_hash=None,id=None):
        if permissions != None:
            if not isinstance(permissions,list):
                raise TypeError("permissions must be a list of permission names")
            else:
                for permission in permissions:
                    if not permission in self.permissions:
                        raise TypeError("permissions in list must be valid permission names")
        emp = Employee(name=name,role=role,start_date=start_date,salary=salary,address=address,permissions=permissions,password=password,id=id,password_hash=password_hash)
        self.employees[emp.id] = emp
        # A user profile is created for logging in
        user = User(emp.id,emp.password_hash)
        self.users[emp.id] = user
        return emp
    
    # This method had planned functionality for filtering searches that hasn't been implemented in the GUI yet, though it is tested and working
    def list_employees(self,name_search=None,role_search=None,min_date=None,max_date=None,min_salary=None,max_salary=None,permissions=None):
        employee_list = list(self.employees.values())
        for key,value in {name_search:["name","string"],role_search:["role","string"],min_date:["start_date","min"],max_date:["start_date","max"],min_salary:["salary","min"],max_salary:["salary","max"]}.items():
            if key !=None:
                # The filtering is done in a utilty function
                employee_list = filter_list(employee_list,value[0],key,value[1])   
        return employee_list
    
    # Altering parameters within an employee, with error handling for employee not found and attempting to change a field that doesn't exist
    def update_employee(self,emp_id,new_data):
        if emp_id not in self.employees:
            raise KeyError(f"Employee {emp_id} not found")

        emp = self.employees[emp_id]

        # Control of which parameters can be changed
        allowed = {"name", "role", "start_date", "salary", "address"}
        for key, value in new_data.items():
            if key == "id":
                continue
            if key not in allowed:
                raise ValueError(f"{key} is not a valid employee field")
            setattr(emp, key, value)

        return emp
    
    # Fairly straightforward removal of employee from list, with error handling for invalid ID and employee not existing
    def delete_employee(self,emp_id):
        if not check_id(emp_id,"emp"):
            raise TypeError("Invalid ID")
        if emp_id not in self.employees.keys():
            raise ValueError("Employee not found, cannot delete")
        del self.employees[emp_id]

    # Updating password (with password hashing) before passing to employee and associated user
    def update_employee_password(self,emp_id,new_password):
        hash = hash_password(new_password)
        self.employees[emp_id].password_hash = hash
        self.users[emp_id].password_hash = hash

    # Method to call department constructor, some error handling here, but most is inside Department
    def create_department(self,name,description,head_of_department,parent_department=None,members=None):
        if not check_id(head_of_department,"emp"):
            raise TypeError("head_of_department must be a valid employee id")
        if parent_department != None:
            if not check_id(parent_department,"dep"):
                raise TypeError("parent_department must be a valid department id")
        # Validation of any passed members list
        if members != None:
            if not isinstance(members,list):
                raise TypeError("members must be a list of employee ids")
            else:
                for employee in members:
                    if not check_id(employee,"emp"):
                        raise TypeError("members in list must be valid employee ids")
        dep = Department(name,description,head_of_department,parent_department,members)
        # Department is added to a list under its ID
        self.departments[dep.id] = dep
        return dep
    
    # As with employees, the tested filtering functionality here has not yet been implemented in the GUI
    def list_departments(self,name_search=None,description_search=None,head_of_department_search=None,parent_department_search=None):
        department_list = list(self.departments.values())
        for key,value in {name_search:["name","string"],description_search:["description","string"],head_of_department_search:["head_of_department","string"],parent_department_search:["parent_department","string"]}.items():
            if key !=None:
                department_list = filter_list(department_list,value[0],key,value[1]) 
        return department_list
    
    # Similar to update employee, this updates legitimate properties of valid IDs
    def update_department(self,dep_id,new_data):
        if dep_id not in self.departments:
            raise KeyError(f"Department {dep_id} not found")

        dep = self.departments[dep_id]

        allowed = {"name", "description", "head_of_department", "parent_department", "members"}
        for key, value in new_data.items():
            if key == "id":
                continue
            if key not in allowed:
                raise ValueError(f"{key} is not a valid department field")
            setattr(dep, key, value)

        return dep
    
    # Simple function to remove department from list with error handling
    def delete_department(self,dep_id):
        if not check_id(dep_id,"dep"):
            raise TypeError("Invalid ID")
        if dep_id not in self.departments.keys():
            raise ValueError("Department not found, cannot delete")
        del self.departments[dep_id]
    
    # Method to add employees to a department, with validation of IDs and ensuring that assets exist
    def add_employee_to_department(self,dep_id,emp_id):
        if not check_id(dep_id,"dep"):
            raise ValueError("Invalid Department ID")
        if not check_id(emp_id,"emp"):
            raise ValueError("Invalid Employee ID")
        if dep_id not in self.departments.keys():
            raise KeyError("Check Department ID, not found")
        if emp_id not in self.employees.keys():
            raise KeyError("Check Employee ID, not found")
        self.departments[dep_id].members.append(emp_id)

    # Permissions are currently hard coded, this method is part of a plan to have them be assignable and editable
    def create_permission(self,name,active = False):
        perm = Permission(name,active)
        self.permissions[perm.name] = perm
        return perm
    
    # This method checks the existence of each class before calling utility functions on each
    def save_to_storage(self):
        if self.employees:
            # First employees are prepared for storage
            emp_df = create_dataframe(self.employees.values())
            # Then stored in a csv
            write_csv("employees", emp_df)
            # This is repeated for departments, permissions and users
        if self.departments:
            dep_df = create_dataframe(self.departments.values())
            write_csv("departments", dep_df)
        if self.permissions:
            perm_df = create_dataframe(self.permissions.values())
            write_csv("permissions", perm_df)
        if self.users:
            perm_df = create_dataframe(self.users.values())
            write_csv("users", perm_df)

    # This method creates a new temporary tracker with information from saved csvs, then overwrites the active tracker with those details 
    def reload_from_storage(self):
        loaded = Tracker.load_from_storage()
        self.employees = loaded.employees
        self.departments = loaded.departments
        self.permissions = loaded.permissions
        self.users = loaded.users

    # To be used on initial startup, this class method can be called before a tracker exists in order to use presaved data
    ### AI DECLARATION - Usage of class methods was as a result of suggestions from an LLM 
    @classmethod
    def load_from_storage(cls):
        tracker = cls()

        # Each class is loaded, then each employee record is built into an Employee, before storing in tracker
        try:
            emp_df = read_csv("employees")
            for row in emp_df.to_dict(orient="records"):
                emp = Employee.from_row(row)
                tracker.employees[emp.id] = emp
        except FileNotFoundError:
            # Error handling for when csv does not exist
            raise FileNotFoundError("no employees file found, please check data folder")
        
        try:
            dep_df = read_csv("departments")
            for row in dep_df.to_dict(orient="records"):
                dep=Department.from_row(row)
                tracker.departments[dep.id] = dep
        except FileNotFoundError:
            raise FileNotFoundError("no departments file found, please check data folder")

        try:
            usr_df = read_csv("users")
            for row in usr_df.to_dict(orient="records"):
                usr=User.from_row(row)
                tracker.users[usr.id] = usr
        except FileNotFoundError:
            raise FileNotFoundError("no users file found, please check data folder")


        try:
            perm_df = read_csv("permissions")
            for row in perm_df.to_dict(orient="records"):
                perm = Permission.from_row(row)
                tracker.permissions[perm.name] = perm
        except FileNotFoundError:
            raise FileNotFoundError("no permissions file found, please check data folder")
        return tracker
    
    # This is a method that was added to be called before the previous one. In order to minimise errors, if any csv doesn't exist, a utility function is called to create and prepopulate it
    @classmethod
    def load_or_create_sample(cls):
        try:
            return cls.load_from_storage()
        except FileNotFoundError:
            # When file not found, generate_sample_data called
            from employee_tracker.utils.generate_sample_data import generate_sample_data
            return generate_sample_data()