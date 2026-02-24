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
        self.employees: Dict[str,Employee] = {}
        self.departments: Dict[str,Department] = {}
        self.permissions: Dict[str,Permission] = {}
        self.users: Dict[str,User] = {}

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
        user = User(emp.id,emp.password_hash)
        self.users[emp.id] = user
        return emp
    
    def list_employees(self,name_search=None,role_search=None,min_date=None,max_date=None,min_salary=None,max_salary=None,permissions=None):
        employee_list = list(self.employees.values())
        for key,value in {name_search:["name","string"],role_search:["role","string"],min_date:["start_date","min"],max_date:["start_date","max"],min_salary:["salary","min"],max_salary:["salary","max"]}.items():
            if key !=None:
                employee_list = filter_list(employee_list,value[0],key,value[1])   
        return employee_list
    
    def update_employee(self,emp_id,new_data):
        if emp_id not in self.employees:
            raise KeyError(f"Employee {emp_id} not found")

        emp = self.employees[emp_id]

        allowed = {"name", "role", "start_date", "salary", "address"}
        for key, value in new_data.items():
            if key == "id":
                continue
            if key not in allowed:
                raise ValueError(f"{key} is not a valid employee field")
            setattr(emp, key, value)

        return emp

    def delete_employee(self,emp_id):
        if not check_id(emp_id,"emp"):
            raise TypeError("Invalid ID")
        if emp_id not in self.employees.keys():
            raise ValueError("Employee not found, cannot delete")
        del self.employees[emp_id]

    def update_employee_password(self,emp_id,new_password):
        hash = hash_password(new_password)
        self.employees[emp_id].password_hash = hash
        self.users[emp_id].password_hash = hash

    def create_department(self,name,description,head_of_department,parent_department=None,members=None):
        if not check_id(head_of_department,"emp"):
            raise TypeError("head_of_department must be a valid employee id")
        if parent_department != None:
            if not check_id(parent_department,"dep"):
                raise TypeError("parent_department must be a valid department id")
        if members != None:
            if not isinstance(members,list):
                raise TypeError("members must be a list of employee ids")
            else:
                for employee in members:
                    if not check_id(employee,"emp"):
                        raise TypeError("members in list must be valid employee ids")
        dep = Department(name,description,head_of_department,parent_department,members)
        self.departments[dep.id] = dep
        return dep
    
    def list_departments(self,name_search=None,description_search=None,head_of_department_search=None,parent_department_search=None):
        department_list = list(self.departments.values())
        for key,value in {name_search:["name","string"],description_search:["description","string"],head_of_department_search:["head_of_department","string"],parent_department_search:["parent_department","string"]}.items():
            if key !=None:
                department_list = filter_list(department_list,value[0],key,value[1]) 
        return department_list
    
    def update_department(self,dep_id,new_data):
        if dep_id not in self.departments:
            raise KeyError(f"Department {dep_id} not found")

        dep = self.departments[dep_id]

        allowed = {"name", "description", "head_of_department", "parent_department", "members"}  # only these
        for key, value in new_data.items():
            if key == "id":
                continue
            if key not in allowed:
                raise ValueError(f"{key} is not a valid department field")
            setattr(dep, key, value)

        return dep
    
    def delete_department(self,dep_id):
        if not check_id(dep_id,"dep"):
            raise TypeError("Invalid ID")
        if dep_id not in self.departments.keys():
            raise ValueError("Department not found, cannot delete")
        del self.departments[dep_id]
    
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
    
    def create_permission(self,name,active = False):
        perm = Permission(name,active)
        self.permissions[perm.name] = perm
        return perm
    
    def save_to_storage(self):
        if self.employees:
            emp_df = create_dataframe(self.employees.values())
            write_csv("employees", emp_df)
        if self.departments:
            dep_df = create_dataframe(self.departments.values())
            write_csv("departments", dep_df)
        if self.permissions:
            perm_df = create_dataframe(self.permissions.values())
            write_csv("permissions", perm_df)
        if self.users:
            perm_df = create_dataframe(self.users.values())
            write_csv("users", perm_df)

    def reload_from_storage(self):
        loaded = Tracker.load_from_storage()
        self.employees = loaded.employees
        self.departments = loaded.departments
        self.permissions = loaded.permissions
        self.users = loaded.users

    @classmethod
    def load_from_storage(cls):
        tracker = cls()

        try:
            emp_df = read_csv("employees")
            for row in emp_df.to_dict(orient="records"):
                emp = Employee.from_row(row)
                tracker.employees[emp.id] = emp
        except FileNotFoundError:
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
    
    @classmethod
    def load_or_create_sample(cls):
        try:
            return cls.load_from_storage()
        except FileNotFoundError:
            from employee_tracker.utils.generate_sample_data import generate_sample_data
            return generate_sample_data()